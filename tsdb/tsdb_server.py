import asyncio
from .persistentdb import PersistentDB
from importlib import import_module
from collections import defaultdict, OrderedDict
from .tsdb_serialization import Deserializer, serialize
from .tsdb_error import *
from .tsdb_ops import *
import procs
import json
import ast
from aiohttp import web
import numpy as np

def trigger_callback_maker(tid, pk, target, calltomake):
    def callback_(future):
        print('CALLBACK_')
        result = future.result()
        if target is not None:
            print('CALLBACKS', pk, target, result)
            calltomake(tid, pk, dict(zip(target, result)))
        return result
    return callback_

class TSDBProtocol(asyncio.Protocol):

    def __init__(self, server):
        self.server = server
        self.deserializer = Deserializer()
        self.futures = []

    def _begin_transaction(self, op):
        tid = self.server.db.begin_transaction() 
        print("S> Begin Transaction")
        if tid > 0:
            return TSDBOp_Return(TSDBStatus.OK, op['op'], payload=tid)
        else:
            raise ValueError("TID", tid)
            
    def _commit(self, op):
        try:
            print("S> Commit", op['tid'])
            self.server.db.commit(op['tid'])
            return TSDBOp_Return(TSDBStatus.OK, op['op'], payload=op['tid'])
        except ValueError as e:
            return TSDBOp_Return(TSDBStatus.INVALID_KEY, op['op'])
        
    def _rollback(self, op):
        try:
            print("S> Rollback ", op['tid'])
            self.server.db.rollback(op['tid'])
            return TSDBOp_Return(TSDBStatus.OK, op['op'], payload=op['tid'])
        except ValueError as e:
            return TSDBOp_Return(TSDBStatus.INVALID_KEY, op['op'])
        
    def _insert_ts(self, op):
        try:
            print("S> Insert TS: ", op['pk'])
            self.server.db.insert_ts(op['tid'], op['pk'], op['ts'])
        except ValueError as e:
            return TSDBOp_Return(TSDBStatus.INVALID_KEY, op['op'])
        self._run_trigger('insert_ts', [op['pk']], op['tid'])
        return TSDBOp_Return(TSDBStatus.OK, op['op'])
    
    def _delete_ts(self, op):
        try:
            self.server.db.delete_ts(op['tid'], op['pk'])
        except ValueError as e:
            return TSDBOp_Return(TSDBStatus.INVALID_KEY, op['op'])
        self._run_trigger('delete_ts', [op['pk']], op['tid'])
        return TSDBOp_Return(TSDBStatus.OK, op['op'])

    def _upsert_meta(self, op):
        self.server.db.upsert_meta(op['tid'], op['pk'], op['md'])
        self._run_trigger('upsert_meta', [op['pk']], op['tid'])
        return TSDBOp_Return(TSDBStatus.OK, op['op'])

    def _select(self, op):
        try:
            loids, fields = self.server.db.select(op['tid'], op['md'], op['fields'], op['additional'])
        except ValueError as e:
            return TSDBOp_Return(TSDBStatus.INVALID_KEY, op['op'])
        
        self._run_trigger('select', loids, op['tid'])
        if fields is not None:
            d = OrderedDict(zip(loids, fields))
            return TSDBOp_Return(TSDBStatus.OK, op['op'], d)
        else:
            d = OrderedDict((k,{}) for k in loids)
            return TSDBOp_Return(TSDBStatus.OK, op['op'], d)

    def _augmented_select(self, op):
        "run a select and then synchronously run some computation on it"
        loids, fields = self.server.db.select(op['tid'], op['md'], ['ts'], op['additional'])
        proc = op['proc']  # The module in procs
        arg = op['arg']  # An additional argument, could be a constant
        target = op['target'] # Not used to upsert any more, but rather to
        # return results in a dictionary with the targets mapped to the return
        # values from proc_main
        mod = import_module('procs.' + proc)
        storedproc = getattr(mod,'proc_main')
        results=[]
        
        for i, pk in enumerate(loids):
            #row = self.server.db.rows[pk]
            #result = storedproc(pk, row, arg)
            result = storedproc(pk, fields[i], arg)
            results.append(dict(zip(target, result)))
        return TSDBOp_Return(TSDBStatus.OK, op['op'], dict(zip(loids, results)))

    def _add_trigger(self, op):
        #print('S> Adding triggers')
        trigger_proc = op['proc']  # the module in procs
        trigger_onwhat = op['onwhat']  # on what? eg `insert_ts`
        trigger_target = op['target']  # if provided, this meta will be upserted
        trigger_arg = op['arg']  # an additional argument, could be a constant
        # FIXME: this import should have error handling
        mod = import_module('procs.'+trigger_proc)
        storedproc = getattr(mod,'main')
        self.server.triggers[trigger_onwhat].append((trigger_proc, storedproc, trigger_arg, trigger_target))
        return TSDBOp_Return(TSDBStatus.OK, op['op'])

    def _remove_trigger(self, op):
        trigger_proc = op['proc']
        trigger_onwhat = op['onwhat']
        trigs = self.server.triggers[trigger_onwhat]
        for t in trigs:
            if t[0]==trigger_proc:
                trigs.remove(t)
        return TSDBOp_Return(TSDBStatus.OK, op['op'])

    def _run_trigger(self, opname, rowmatch, tid):
        lot = self.server.triggers[opname]
        tnames = []
        for tname, t, arg, target in lot:
            tnames.append(tname)
        
        print("S> Running triggers for rows: ", rowmatch, tnames, opname)
        for tname, t, arg, target in lot:
            for pk in rowmatch:
                a_row = self.server.db._trees['pk'].get_as_row(pk)

                row = a_row.row.copy()
                row['pk'] = a_row.pk
                row['ts'] = a_row.ts
                
                task = asyncio.ensure_future(t(pk, row, arg))
                task.add_done_callback(trigger_callback_maker(tid, pk, target, self.server.db.upsert_meta))

    def _create_vp(self, op):
        tid = op['tid']
        pk = op['pk']
        
        # Set this TimeSeries as a Vantage Point
        try:
            field, ts = self.server.db.create_vp(tid, pk)
        except ValueError:
            return TSDBOp_Return(TSDBStatus.INVALID_KEY, op['op'])
        
        # Add a trigger so all new TimeSeries will have the corr with this VP
        trigger = self._add_trigger(TSDBOp_AddTrigger(tid, 'corr', 'insert_ts', [field], ts))
        
        if trigger['status'] is not TSDBStatus.OK:
            return TSDBOp_Return(TSDBStatus.INVALID_KEY, op['op'])
        
        # Update all existing TimeSeries with the corr with this new VP
        augment_op = TSDBOp_AugmentedSelect(tid, 'corr', [field], ts, {}, None)
        
        augment = self._augmented_select(augment_op)
        if augment['status'] is not TSDBStatus.OK:
            return TSDBOp_Return(TSDBStatus.INVALID_KEY, op['op'])
        
        for pk, metadata in augment['payload'].items():
            upsert = self._upsert_meta(TSDBOp_UpsertMeta(tid, pk, metadata))

            if upsert['status'] != TSDBStatus.OK:
                return TSDBOp_Return(TSDBStatus.INVALID_OPERATION, op['op'])

        return TSDBOp_Return(TSDBStatus.OK, op['op'])
        # choose 5 distinct vantage point time series
        #vpkeys = ["ts-{}".format(i) for i in np.random.choice(range(50), size=5, replace=False)]
        
    def _ts_similarity_search(self, op):
        if len(self.server.db.vps) == 0:
            # No Vantage Points! Can't run Similarity Search
            return TSDBOp_Return(TSDBStatus.INVALID_OPERATION, op['op'])

        tid = op['tid']
        limit = op['limit']
        ts = op['ts']
        
        # Get the closest VP
        a_select = self._augmented_select(TSDBOp_AugmentedSelect(tid, 'corr', ['vpd'], ts, {'vp': {'==': True}}, None))
        if a_select['status'] != TSDBStatus.OK:
            return TSDBOp_Return(TSDBStatus.UNKNOWN_ERROR, op['op'])

        payload = a_select['payload']
        pks = payload.keys()
        
        min_vp_dist = None
        
        for pk in pks:
            dist = payload[pk]['vpd']
            if min_vp_dist == None or dist < min_vp_dist:
                closest_vp = pk
                min_vp_dist = dist

        # The radius is 2 times the distance to the nearest vp
        radius = 2 * min_vp_dist
        if radius == 0:
            # Give radius a boost if has found the exact ts to get other ts's other than the exact one
            radius = 8.0
        
        vp_id = self.server.db.vps.index(closest_vp)
        
        a_select = self._augmented_select(TSDBOp_AugmentedSelect(tid, 'corr', ['dist'], ts, {'d_vp-{}'.format(vp_id): {'<=': radius}}, None))
        if a_select['status'] != TSDBStatus.OK:
            return TSDBOp_Return(TSDBStatus.UNKNOWN_ERROR, op['op'])
        
        payload = a_select['payload']

        closest_ts = [(d, payload[d]['dist']) for d in payload.keys()]
        closest_ts.sort(key=lambda x: x[1])
        closest_ts = closest_ts[:limit]
        closest = OrderedDict()
        for key, value in closest_ts:
            closest[key] = value

        return TSDBOp_Return(TSDBStatus.OK, op['op'], closest)
                
    def connection_made(self, conn):
        print('S> connection made')
        self.conn = conn

    def data_received(self, data):
        print('S> data received ['+str(len(data))+']: '+str(data))
        self.deserializer.append(data)
        if self.deserializer.ready():
            msg = self.deserializer.deserialize()
            status = TSDBStatus.OK  # until proven otherwise.
            response = TSDBOp_Return(status, None)  # until proven otherwise.
            try:
                op = TSDBOp.from_json(msg)
            except TypeError as e:
                print('S> invalid operation')
                response = TSDBOp_Return(TSDBStatus.INVALID_OPERATION, None)
            try:
                if status is TSDBStatus.OK:
                    if isinstance(op, TSDBOp_BeginTransaction):
                        response = self._begin_transaction(op)
                    elif isinstance(op, TSDBOp_Commit):
                        response = self._commit(op)    
                    elif isinstance(op, TSDBOp_Rollback):
                        response = self._rollback(op)
                    elif isinstance(op, TSDBOp_CreateVP):
                        response = self._create_vp(op)
                    elif isinstance(op, TSDBOp_TSSimilaritySearch):
                        response = self._ts_similarity_search(op)
                    elif isinstance(op, TSDBOp_InsertTS):
                        response = self._insert_ts(op)
                    elif isinstance(op, TSDBOp_DeleteTS):
                        response = self._delete_ts(op)
                    elif isinstance(op, TSDBOp_UpsertMeta):
                        response = self._upsert_meta(op)
                    elif isinstance(op, TSDBOp_Select):
                        response = self._select(op)
                    elif isinstance(op, TSDBOp_AugmentedSelect):
                        response = self._augmented_select(op)
                    elif isinstance(op, TSDBOp_AddTrigger):
                        response = self._add_trigger(op)
                    elif isinstance(op, TSDBOp_RemoveTrigger):
                        response = self._remove_trigger(op)
                    else:
                        response = TSDBOp_Return(TSDBStatus.UNKNOWN_ERROR, op['op'])          
            except Exception as e:
                response = TSDBOp_Return(TSDBStatus.UNKNOWN_ERROR, "", str(e))

            try:
                self.conn.write(serialize(response.to_json()))
            except Exception as e:
                response = TSDBOp_Return(TSDBStatus.UNKNOWN_ERROR, "", str(e))
                self.conn.write(serialize(response.to_json()))
            self.conn.close()
                
    def connection_lost(self, transport):
        print('S> connection lost')

    def rest_hello_world(self, request):
        return web.Response(body=b"Hello world")

    #@rest_handler
    @asyncio.coroutine
    def post_handler(self, request):
        data = yield from request.json()
        status = TSDBStatus.OK  # until proven otherwise.
        response = TSDBOp_Return(status, None)  # until proven otherwise.

        msg = data
        try:
            op = TSDBOp.from_json(msg)
        except TypeError as e:
            response = TSDBOp_Return(TSDBStatus.INVALID_OPERATION, None)

        try:
            if status is TSDBStatus.OK:
                if isinstance(op, TSDBOp_BeginTransaction):
                    response = self._begin_transaction(op)
                elif isinstance(op, TSDBOp_Commit):
                    response = self._commit(op)    
                elif isinstance(op, TSDBOp_Rollback):
                    response = self._rollback(op)
                elif isinstance(op, TSDBOp_CreateVP):
                    response = self._create_vp(op)
                elif isinstance(op, TSDBOp_TSSimilaritySearch):
                    response = self._ts_similarity_search(op)
                elif isinstance(op, TSDBOp_InsertTS):
                    response = self._insert_ts(op)
                elif isinstance(op, TSDBOp_DeleteTS):
                    response = self._delete_ts(op)
                elif isinstance(op, TSDBOp_UpsertMeta):
                    response = self._upsert_meta(op)
                elif isinstance(op, TSDBOp_Select):
                    response = self._select(op)
                elif isinstance(op, TSDBOp_AugmentedSelect):
                    response = self._augmented_select(op)
                elif isinstance(op, TSDBOp_AddTrigger):
                    response = self._add_trigger(op)
                elif isinstance(op, TSDBOp_RemoveTrigger):
                    response = self._remove_trigger(op)
                else:
                    response = TSDBOp_Return(TSDBStatus.UNKNOWN_ERROR, op['op'])
        except Exception as e:
            response = TSDBOp_Return(TSDBStatus.UNKNOWN_ERROR,"", str(e))
        return web.json_response(response.to_json())

class TSDBServer(object):

    def __init__(self, db, port=9999):
        self.port = port
        self.db = db
        self.triggers = defaultdict(list)
        self.autokeys = {}
        print('S> Starting Server on port:', port)

    def exception_handler(self, loop, context):
        print('S> EXCEPTION:', str(context))
        loop.stop()

    def run(self, testing=False):
        loop = asyncio.get_event_loop()
        # NOTE: enable this if you'd rather have the server stop on an error
        #       currently it dumps the protocol and keeps going; new connections
        #       are unaffected. Rather nice, actually.
        #loop.set_exception_handler(self.exception_handler)
        self.listener = loop.create_server(lambda: TSDBProtocol(self), '127.0.0.1', self.port)
        print('S> Starting TSDB server on port',self.port)
        listener = loop.run_until_complete(self.listener)
            
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print('S> Exiting.')
        except Exception as e:
            print('S> Exception:',e)
        finally:
            listener.close()
            loop.close()

            #closing server db 
            self.db.close()

    def rest_run(self):
        loop = asyncio.get_event_loop()
        app = web.Application()
        tsdbproc = TSDBProtocol(self)
        app.router.add_route('GET', '/', tsdbproc.rest_hello_world)
        app.router.add_route('POST', '/', tsdbproc.post_handler)
        self.listener = loop.create_server(app.make_handler(), '127.0.0.1', self.port)
        print('S> Starting REST TSDB server on port',self.port)
        listener = loop.run_until_complete(self.listener)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print('S> Exiting.')
        except Exception as e:
            print('S> Exception:',e)
        finally:
            listener.close()
            loop.close()

            #closing server db 
            self.db.close()

if __name__=='__main__':
    empty_schema = {'pk': {'convert': lambda x: x, 'index': None}}
    db = DictDB(empty_schema, 'pk')
    TSDBServer(db).run()