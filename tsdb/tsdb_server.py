import asyncio
from .dictdb import DictDB
from importlib import import_module
from collections import defaultdict, OrderedDict
from .tsdb_serialization import Deserializer, serialize
from .tsdb_error import *
from .tsdb_ops import *
import procs
import json
import ast
from aiohttp import web

def trigger_callback_maker(pk, target, calltomake):
    def callback_(future):
        result = future.result()
        if target is not None:
            calltomake(pk, dict(zip(target, result)))
        return result
    return callback_

class TSDBProtocol(asyncio.Protocol):

    def __init__(self, server):
        self.server = server
        self.deserializer = Deserializer()
        self.futures = []

    def _insert_ts(self, op):
        try:
            self.server.db.insert_ts(op['pk'], op['ts'])
        except ValueError as e:
            return TSDBOp_Return(TSDBStatus.INVALID_KEY, op['op'])
        self._run_trigger('insert_ts', [op['pk']])
        return TSDBOp_Return(TSDBStatus.OK, op['op'])
    
    def _delete_ts(self, op):
        try:
            self.server.db.delete_ts(op['pk'])
        except ValueError as e:
            return TSDBOp_Return(TSDBStatus.INVALID_KEY, op['op'])
        self._run_trigger('delete_ts', [op['pk']])
        return TSDBOp_Return(TSDBStatus.OK, op['op'])

    def _upsert_meta(self, op):
        self.server.db.upsert_meta(op['pk'], op['md'])
        self._run_trigger('upsert_meta', [op['pk']])
        return TSDBOp_Return(TSDBStatus.OK, op['op'])

    def _select(self, op):
        loids, fields = self.server.db.select(op['md'], op['fields'], op['additional'])
        self._run_trigger('select', loids)
        if fields is not None:
            d = OrderedDict(zip(loids, fields))
            return TSDBOp_Return(TSDBStatus.OK, op['op'], d)
        else:
            d = OrderedDict((k,{}) for k in loids)
            return TSDBOp_Return(TSDBStatus.OK, op['op'], d)

    def _augmented_select(self, op):
        "run a select and then synchronously run some computation on it"
        loids, fields = self.server.db.select(op['md'], None, op['additional'])
        proc = op['proc']  # the module in procs
        arg = op['arg']  # an additional argument, could be a constant
        target = op['target'] #not used to upsert any more, but rather to
        # return results in a dictionary with the targets mapped to the return
        # values from proc_main
        mod = import_module('procs.'+proc)
        storedproc = getattr(mod,'proc_main')
        results=[]
        for pk in loids:
            row = self.server.db.rows[pk]
            result = storedproc(pk, row, arg)
            results.append(dict(zip(target, result)))
        return TSDBOp_Return(TSDBStatus.OK, op['op'], dict(zip(loids, results)))

    def _add_trigger(self, op):
        print('Adding triggers')
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

    def _run_trigger(self, opname, rowmatch):
        lot = self.server.triggers[opname]
        print("S> list of triggers to run", lot)
        for tname, t, arg, target in lot:
            for pk in rowmatch:
                row = self.server.db.rows[pk]
                task = asyncio.ensure_future(t(pk, row, arg))
                task.add_done_callback(trigger_callback_maker(pk, target, self.server.db.upsert_meta))

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
                response = TSDBOp_Return(TSDBStatus.INVALID_OPERATION, None)

            if status is TSDBStatus.OK:
                if isinstance(op, TSDBOp_InsertTS):
                    response = self._insert_ts(op)
                elif isinstance(op, TSDBOp_DeleteTS):
                    response = self._delete_ts(op)
                elif isinstance(op, TSDBOp_UpsertMeta):
                    response = self._upsert_meta(op)
                elif isinstance(op, TSDBOp_Select):
                    response = self._select(op)
                elif isinstance(op, TSDBOp_AddTrigger):
                    response = self._add_trigger(op)
                elif isinstance(op, TSDBOp_RemoveTrigger):
                    response = self._remove_trigger(op)
                else:
                    response = TSDBOp_Return(TSDBStatus.UNKNOWN_ERROR, op['op'])

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

        if status is TSDBStatus.OK:
            if isinstance(op, TSDBOp_InsertTS):
                response = self._insert_ts(op)
            elif isinstance(op, TSDBOp_DeleteTS):
                response = self._delete_ts(op)
            elif isinstance(op, TSDBOp_UpsertMeta):
                response = self._upsert_meta(op)
            elif isinstance(op, TSDBOp_Select):
                response = self._select(op)
            elif isinstance(op, TSDBOp_AddTrigger):
                response = self._add_trigger(op)
            elif isinstance(op, TSDBOp_RemoveTrigger):
                response = self._remove_trigger(op)
            else:
                response = TSDBOp_Return(TSDBStatus.UNKNOWN_ERROR, op['op'])
        return web.json_response(response.to_json())

class TSDBServer(object):

    def __init__(self, db, port=9999):
        self.port = port
        self.db = db
        self.triggers = defaultdict(list)
        self.autokeys = {}

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

if __name__=='__main__':
    empty_schema = {'pk': {'convert': lambda x: x, 'index': None}}
    db = DictDB(empty_schema, 'pk')
    TSDBServer(db).run()