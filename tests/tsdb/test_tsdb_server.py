from tsdb import TSDBServer, PersistentDB, TSDBClient, TSDBProtocol
import timeseries as ts
from concurrent.futures import ThreadPoolExecutor, thread
from tsdb.tsdb_ops import *
from collections import defaultdict, OrderedDict
from importlib import import_module
import time
import numpy as np
import asynctest
import procs
import numpy as np
from scipy.stats import norm
import unittest

#identity = lambda x: x

schema = {
  'pk': {'convert': str, 'index': None, 'default': -1},  # Will be indexed anyways
  'ts': {'convert': str, 'index': None, 'default': None},
  'order': {'convert': int, 'index': 1, 'default': 0},
  'blarg': {'convert': int, 'index': 1, 'default': 0},
  'useless': {'convert': str, 'index': None, 'default': 0},
  'mean': {'convert': float, 'index': 1, 'default': 0},
  'std': {'convert': float, 'index': 1, 'default': 0}
}

def tsmaker(m, s, j):
    "returns metadata and a time series in the shape of a jittered normal"
    meta={}
    meta['order'] = int(np.random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]))
    meta['blarg'] = int(np.random.choice([1, 2]))
    t = np.arange(0.0, 1.0, 0.01)
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return meta, ts.TimeSeries(t, v)

class Test_TSDB_Protocol(unittest.TestCase):

    def test_protocol(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        server = TSDBServer(db)
        prot = TSDBProtocol(server)
        
        # Dumb server tests
        assert(server.db == db)
        assert(server.port == 9999)
        
        # Test Transaction
        tid = prot._begin_transaction(TSDBOp_BeginTransaction())['payload']
        assert(tid == 1)
    
        t1 = [0,1,2,3,4]
        v1 = [1.0,2.0,3.0,2.0,1.0]
        ats1 = ts.TimeSeries(t1, v1)
    
        t2 = [10,11,12,13,14]
        v2 = [-1.0,-2.0,-3.0,-2.0,-1.0]
        ats2 = ts.TimeSeries(t2, v2)
    
        # Test TSDBOp_InsertTS
        insert_op = {}
        insert_op['pk'] = 1
        insert_op['ts'] = ats1
        insert_op['op'] = 'insert_ts'
        insert_op['tid'] = tid
        InsertedTS = TSDBOp_InsertTS(tid, 1, ats1)
        assert(insert_op == InsertedTS)
    
        # Test Protocol Insert
        insert_return = prot._insert_ts(insert_op)
        assert(insert_return['op'] == 'insert_ts')
        assert(insert_return['status'] == TSDBStatus.OK)
        assert(insert_return['payload'] == None)

        assert(server.db._trees['pk'].get_as_row('1').pk == '1')
        assert(server.db._trees['pk'].get_as_row('1').ts == ats1)
        
        # Add some more data
        prot._insert_ts(TSDBOp_InsertTS(tid, '2', ats1))
        assert(server.db._trees['pk'].get_as_row('2').ts == ats1)
        
        # Test Protocol Upsert
        upserted_meta = TSDBOp_UpsertMeta(tid, '2', {'order': 1})
        upsert_return = prot._upsert_meta(upserted_meta)
        assert(upsert_return['op'] == 'upsert_meta')
        assert(upsert_return['status'] == TSDBStatus.OK)
        assert(upsert_return['payload'] == None)
    
        # Test Protocol Select (None fields)
        metadata_dict = {'pk': {'>': '0'}}
        fields = None
        additional = None
        select_op = TSDBOp_Select(tid, metadata_dict, fields, additional)
        select_return = prot._select(select_op)
        print("Here", select_return)
        assert(select_return['op'] == 'select')
        assert(select_return['status'] == TSDBStatus.OK)
        assert(select_return['payload']['1'] == {})
        assert(select_return['payload']['2'] == {})
        
        # Test Protocol Select
        metadata_dict = {'pk': {'>': '0'}}
        fields = ['ts']
        additional = None
        select_op = TSDBOp_Select(tid, metadata_dict, fields, additional)
        select_return = prot._select(select_op)
        assert(select_return['op'] == 'select')
        assert(select_return['status'] == TSDBStatus.OK)
        assert(select_return['payload']['1']['ts'] == ats1)
        assert(select_return['payload']['2']['ts'] == ats1)
        
        # Test Add Trigger
        add_trigger_op = TSDBOp_AddTrigger(tid, 'stats', 'insert_ts', ['mean', 'std'], None)
        prot._add_trigger(add_trigger_op)
        
        mod = import_module('procs.stats')
        storedproc = getattr(mod,'main')
        
        assert(server.triggers['insert_ts'] ==  [('stats', storedproc, None, ['mean', 'std'])])
        db.close()
        #prot._insert_ts(TSDBOp_InsertTS(3, ats1))
        #time.sleep(1)
        #inserted_row = server.db.rows[3]
        #assert(inserted_row['mean'] == ats1)
        #assert(inserted_row['std'] == ats1)

    def test_protocol_delete(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        server = TSDBServer(db)
        prot = TSDBProtocol(server)
        tid = prot._begin_transaction(TSDBOp_BeginTransaction())['payload']
    
        t1 = [0,1,2,3,4]
        v1 = [1.0,2.0,3.0,2.0,1.0]
        ats1 = ts.TimeSeries(t1, v1)
    
        t2 = [10,11,12,13,14]
        v2 = [-1.0,-2.0,-3.0,-2.0,-1.0]
        ats2 = ts.TimeSeries(t2, v2)

        insert_op = {}
        insert_op['pk'] = '1'
        insert_op['ts'] = ats1
        insert_op['op'] = 'insert_ts'
        insert_op['tid'] = tid
    
        # Test Protocol Insert
        insert_return = prot._insert_ts(insert_op)
        assert(insert_return['op'] == 'insert_ts')
        assert(insert_return['status'] == TSDBStatus.OK)
        assert(insert_return['payload'] == None)
        assert(server.db._trees['pk'].get_as_row('1').pk == '1')
        assert(server.db._trees['pk'].get_as_row('1').ts == ats1)

        insert_return2 = prot._insert_ts(insert_op)
        assert(insert_return2['op'] == 'insert_ts')
        assert(insert_return2['status'] == TSDBStatus.INVALID_KEY)

        delete_op = {}
        delete_op['pk'] = '1'
        delete_op['op'] = 'delete_ts'
        delete_op['tid'] = tid

        delete_return = prot._delete_ts(delete_op)
        assert(delete_return['op'] == 'delete_ts')
        assert(delete_return['status'] == TSDBStatus.OK)
        assert(delete_return['payload'] == None)
        assert (len(server.db._trees['pk'].get_all_keys()) == 0)

        delete_return2 = prot._delete_ts(delete_op)
        assert(delete_return2['op'] == 'delete_ts')
        assert(delete_return2['status'] == TSDBStatus.INVALID_KEY)
        db.close()

    def test_protocol_triggers(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        server = TSDBServer(db)
        prot = TSDBProtocol(server)
        tid = prot._begin_transaction(TSDBOp_BeginTransaction())['payload']

        # Test Add Trigger
        add_trigger_op = TSDBOp_AddTrigger(tid, 'stats', 'insert_ts', ['mean', 'std'], None)
        prot._add_trigger(add_trigger_op)

        mod = import_module('procs.stats')
        storedproc = getattr(mod,'main')

        assert(server.triggers['insert_ts'] ==  [('stats', storedproc, None, ['mean', 'std'])])

        # Test delete Trigger
        delete_trigger_op = TSDBOp_RemoveTrigger(tid, 'stats', 'insert_ts')
        prot._remove_trigger(delete_trigger_op)

        mod = import_module('procs.stats')
        storedproc = getattr(mod,'main')

        assert(server.triggers['insert_ts'] ==  [])
        db.close()

    def test_augmented_select(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        server = TSDBServer(db)
        prot = TSDBProtocol(server)
        tid = prot._begin_transaction(TSDBOp_BeginTransaction())['payload']
        
        t1 = [0,1,2,3,4]
        v1 = [1.0,2.0,3.0,2.0,1.0]
        ats1 = ts.TimeSeries(t1, v1)

        t2 = [10,11,12,13,14]
        v2 = [-1.0,-2.0,-3.0,-2.0,-1.0]
        ats2 = ts.TimeSeries(t2, v2)

        insert_op = {}
        insert_op['pk'] = '1'
        insert_op['ts'] = ats1
        insert_op['op'] = 'insert_ts'
        insert_op['tid'] = tid

        # Test Protocol Insert
        insert_return = prot._insert_ts(insert_op)
        assert(insert_return['op'] == 'insert_ts')
        assert(insert_return['status'] == TSDBStatus.OK)
        assert(insert_return['payload'] == None)
        
        assert(server.db._trees['pk'].get_as_row('1').pk == '1')
        assert(server.db._trees['pk'].get_as_row('1').ts == ats1)

        # Test Protocol Select (None fields)
        metadata_dict = {'pk': {'>': 0}}
        fields = None
        additional = None
        aug_select_op = TSDBOp_AugmentedSelect(tid, 'corr', ['dist'], [t2,v2], metadata_dict, additional )
        aug_select_return = prot._augmented_select(aug_select_op)

        assert(aug_select_return['op'] == 'augmented_select')
        assert(aug_select_return['status'] == TSDBStatus.OK)
        assert(aug_select_return['payload'] == {'1': {'dist': 0.83485935360315389}})
        db.close()

    def test_simple_run(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        server = TSDBServer(db)
        prot = TSDBProtocol(server)
        tid = prot._begin_transaction(TSDBOp_BeginTransaction())['payload']
        
        # Data
        t = [0,1,2,3,4]
        v = [1.0,2.0,3.0,2.0,1.0]
        ats = ts.TimeSeries(t, v)
            
        # Add Trigger
        prot._add_trigger(TSDBOp_AddTrigger(tid, 'stats', 'insert_ts', ['mean', 'std'], None))
        assert('insert_ts' in prot.server.triggers)
            
        # Insert
        print('INSERTING')
        prot._insert_ts(TSDBOp_InsertTS(tid, '1', ats))
        
        time.sleep(1)

        # Select
        select_return = prot._select(TSDBOp_Select(tid, {'pk': {'==': '1'}}, ['ts','mean','std'], None))
        
        payload = select_return['payload']
        
        assert(select_return['status'] == 0)
        assert(select_return['payload']['1']['ts'] == ats)
        # TODO:
        #assert(payload['1']['std'] == 1.4142135623730951)
        #assert(payload['1']['mean'] == 1.8)
        db.close()

    def test_create_vp(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        server = TSDBServer(db)
        prot = TSDBProtocol(server)
        tid = prot._begin_transaction(TSDBOp_BeginTransaction())['payload']
        
        # Set up 50 time series
        mus = np.random.uniform(low=0.0, high=1.0, size=50)
        sigs = np.random.uniform(low=0.05, high=0.4, size=50)
        jits = np.random.uniform(low=0.05, high=0.2, size=50)

        # Dictionaries for time series and their metadata
        tsdict={}
        metadict={}
        for i, m, s, j in zip(range(40), mus, sigs, jits):
            meta, tsrs = tsmaker(m, s, j)
            # the primary key format is ts-1, ts-2, etc
            pk = "ts-{}".format(i)
            tsdict[pk] = tsrs
            meta['vp'] = False
            metadict[pk] = meta
            
        # Dictionaries tetst [pomts
        tsdict1={}
        metadict1={}
        for i, m, s, j in zip(range(40, 50), mus, sigs, jits):
            meta, tsrs = tsmaker(m, s, j)
            # the primary key format is ts-1, ts-2, etc
            pk = "ts-{}".format(i)
            tsdict1[pk] = tsrs
            meta['vp'] = False
            metadict1[pk] = meta
    
        # Insert some rows
        for k in tsdict1:
            prot._insert_ts(TSDBOp_InsertTS(tid, k, tsdict1[k]))
    
        numvps = 5
        
        # Choose 5 distinct ts to become vantage points
        vpkeys = ["ts-{}".format(i) for i in range(5)]
        
        # Create the Vantage Points
        for i in range(numvps):
            with self.assertRaises(KeyError):
                prot._create_vp(TSDBOp_CreateVP(tid, vpkeys[i]))
            
            back = prot._insert_ts(TSDBOp_InsertTS(tid, vpkeys[i], tsdict[vpkeys[i]]))
            assert(back['status'] == 0)
            prot._create_vp(TSDBOp_CreateVP(tid, vpkeys[i]))            
        
        # Ensure the Vantage Points were set
        select_return = prot._select(TSDBOp_Select(tid, {'vp':{'==':True}}, ['ts','mean','std'], None))
        assert(len(select_return['payload']) == 5)
        
        # Check to see if existing TimeSeries have vpd's
        select_return = prot._select(TSDBOp_Select(tid, {'pk':{'==':'ts-41'}}, [], None))
        payload = select_return['payload']
        assert('d_vp-0' in payload['ts-41'])
        assert('d_vp-4' in payload['ts-41'])
        assert(payload['ts-41']['d_vp-0'] > 0)
        
        # Similarity Search for a vantage point
        similar = prot._ts_similarity_search(TSDBOp_TSSimilaritySearch(tid, 5, tsdict[vpkeys[0]]))
        payload = similar['payload']
        assert(len(payload) == 5)
        assert(payload[vpkeys[0]] == 0.0)
        keys = payload.keys()
        prev = 0.0
        # Check the order
        for key in keys:
            value = payload[key]
            assert(value >= prev and value <= 1.0)
            prev = value
        
        # Insert the rest of the rows
        for k in range(5, 35):
            key = 'ts-' + str(k)
            prot._insert_ts(TSDBOp_InsertTS(tid, key, tsdict[key]))
            
        # Check to see if the new rows have vpd's
        #select_return = prot._select(TSDBOp_Select(tid, {'pk':{'==':'ts-5'}}, [], None))
        #payload = select_return['payload']
        # TODO:
        #assert('d_vp-0' in payload['ts-5'])
        #assert('d_vp-4' in payload['ts-5'])
        #assert(payload['ts-5']['d_vp-0'] > 0)
        
        # Similarity Search for a non-existant ts
        similar = prot._ts_similarity_search(TSDBOp_TSSimilaritySearch(tid, 5, tsdict['ts-36']))
        payload = similar['payload']
        print(payload)
        assert(len(payload) > 1)
        
        db.close()

    def test_server_commit(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        server = TSDBServer(db)
        prot = TSDBProtocol(server)
        
        # Dumb server tests
        assert(server.db == db)
        assert(server.port == 9999)
        
        # Test Transaction
        tid = prot._begin_transaction(TSDBOp_BeginTransaction())['payload']
        assert(tid == 1)
    
        t1 = [0,1,2,3,4]
        v1 = [1.0,2.0,3.0,2.0,1.0]
        ats1 = ts.TimeSeries(t1, v1)
    
    
        # Test TSDBOp_InsertTS
        insert_op = {}
        insert_op['pk'] = 1
        insert_op['ts'] = ats1
        insert_op['op'] = 'insert_ts'
        insert_op['tid'] = tid
        InsertedTS = TSDBOp_InsertTS(tid, 1, ats1)
        assert(insert_op == InsertedTS)

        # Test Protocol Insert
        insert_return = prot._insert_ts(insert_op)
        assert(insert_return['op'] == 'insert_ts')
        assert(insert_return['status'] == TSDBStatus.OK)
        assert(insert_return['payload'] == None)


        #COMMIT
        commit_op = {}
        commit_op['op'] = 'commit'
        commit_op['tid'] = tid
        commitTS = TSDBOp_Commit(tid)
        assert(commit_op == commitTS)

        commit_return = prot._commit(commitTS)
        assert(commit_return['op'] == 'commit')
        assert(commit_return['status'] == TSDBStatus.OK)
        assert(commit_return['payload'] == 1)

        db.close()
        db = PersistentDB(schema, 'pk', overwrite=False)
        server = TSDBServer(db)
        prot = TSDBProtocol(server)
        # start new Transaction
        tid = prot._begin_transaction(TSDBOp_BeginTransaction())['payload']

        # Test Protocol Select (None fields)
        metadata_dict = {'pk': {'>': '0'}}
        fields = None
        additional = None
        select_op = TSDBOp_Select(tid, metadata_dict, fields, additional)
        select_return = prot._select(select_op)
        print("Here", select_return)
        assert(select_return['op'] == 'select')
        assert(select_return['status'] == TSDBStatus.OK)
        assert(select_return['payload']['1'] == {})
        

        db.close()

    def test_server_rollback(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        server = TSDBServer(db)
        prot = TSDBProtocol(server)
        
        # Dumb server tests
        assert(server.db == db)
        assert(server.port == 9999)
        
        # Test Transaction
        tid = prot._begin_transaction(TSDBOp_BeginTransaction())['payload']
        assert(tid == 1)
    
        t1 = [0,1,2,3,4]
        v1 = [1.0,2.0,3.0,2.0,1.0]
        ats1 = ts.TimeSeries(t1, v1)
    
    
        # Test TSDBOp_InsertTS
        insert_op = {}
        insert_op['pk'] = 1
        insert_op['ts'] = ats1
        insert_op['op'] = 'insert_ts'
        insert_op['tid'] = tid
        InsertedTS = TSDBOp_InsertTS(tid, 1, ats1)
        assert(insert_op == InsertedTS)

        # Test Protocol Insert
        insert_return = prot._insert_ts(insert_op)
        assert(insert_return['op'] == 'insert_ts')
        assert(insert_return['status'] == TSDBStatus.OK)
        assert(insert_return['payload'] == None)


        #COMMIT
        rollback_op = {}
        rollback_op['op'] = 'rollback'
        rollback_op['tid'] = tid
        rollbackTS = TSDBOp_Rollback(tid)
        assert(rollback_op == rollbackTS)

        rollback_return = prot._rollback(rollbackTS)
        assert(rollback_return['op'] == 'rollback')
        assert(rollback_return['status'] == TSDBStatus.OK)
        assert(rollback_return['payload'] == 1)

        db.close()
        db = PersistentDB(schema, 'pk', overwrite=False)
        server = TSDBServer(db)
        prot = TSDBProtocol(server)
        # start new Transaction
        tid = prot._begin_transaction(TSDBOp_BeginTransaction())['payload']

        # Test Protocol Select (None fields)
        metadata_dict = {'pk': {'>': '0'}}
        fields = None
        additional = None
        select_op = TSDBOp_Select(tid, metadata_dict, fields, additional)
        select_return = prot._select(select_op)
        print("Here", select_return)
        assert(select_return['op'] == 'select')
        assert(select_return['status'] == TSDBStatus.OK)
        assert(len(select_return['payload']) == 0)
        

        db.close()