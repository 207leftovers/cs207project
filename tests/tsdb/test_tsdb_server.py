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

identity = lambda x: x

schema = {
  'pk': {'convert': identity, 'index': None, 'default': -1},  # Will be indexed anyways
  'ts': {'convert': identity, 'index': None, 'default': None},
  'order': {'convert': int, 'index': 1, 'default': 0},
  'blarg': {'convert': int, 'index': 1, 'default': 0},
  'useless': {'convert': identity, 'index': None, 'default': 0},
  'mean': {'convert': float, 'index': 1, 'default': 0},
  'std': {'convert': float, 'index': 1, 'default': 0},
  'vp': {'convert': bool, 'index': 1, 'default': False}
}

NUMVPS = 5
# we augment the schema by adding columns for 5 vantage points
for i in range(NUMVPS):
    schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1, 'default': 0}
    
class Test_TSDB_Protocol():

    def test_protocol(self):
        db = PersistentDB(schema, 'pk')
        server = TSDBServer(db)
        prot = TSDBProtocol(server)
    
        # Dumb server tests
        assert(server.db == db)
        assert(server.port == 9999)
    
        t1 = [0,1,2,3,4]
        v1 = [1.0,2.0,3.0,2.0,1.0]
        ats1 = ts.TimeSeries(t1, v1)
    
        t2 = [10,11,12,13,14]
        v2 = [-1.0,-2.0,-3.0,-2.0,-1.0]
        ats2 = ts.TimeSeries(t2, v2)
        
        # Test Begin Transaction
        begin_tx = TSDBOp_BeginTransaction()
        tid = prot._begin_transaction(begin_tx)['payload']
        assert(tid == 1)
    
        # Test TSDBOp_InsertTS
        insert_op = {}
        insert_op['tid'] = tid
        insert_op['pk'] = 1
        insert_op['ts'] = ats1
        insert_op['op'] = 'insert_ts'
        InsertedTS = TSDBOp_InsertTS(tid, 1, ats1)
        assert(insert_op == InsertedTS)
    
        # Test Protocol Insert
        insert_return = prot._insert_ts(insert_op)
        assert(insert_return['op'] == 'insert_ts')
        assert(insert_return['status'] == TSDBStatus.OK)
        assert(insert_return['payload'] == None)
        inserted_row = server.db.rows[1]
        assert(inserted_row['pk'] == 1)
        assert(inserted_row['ts'] == ats1)
        
        # Add some more data
        prot._insert_ts(TSDBOp_InsertTS(tid, 2, ats1))
        inserted_row = server.db.rows[2]
        assert(inserted_row['ts'] == ats1)
        
        # Test Protocol Upsert
        upserted_meta = TSDBOp_UpsertMeta(tid, 2, {'ts': ats2, 'order': 1})
        upsert_return = prot._upsert_meta(upserted_meta)
        assert(upsert_return['op'] == 'upsert_meta')
        assert(upsert_return['status'] == TSDBStatus.OK)
        assert(upsert_return['payload'] == None)
    
        # Test Protocol Select (None fields)
        metadata_dict = {'pk': {'>': 0}}
        fields = None
        additional = None
        select_op = TSDBOp_Select(tid, metadata_dict, fields, additional)
        select_return = prot._select(select_op)
        print("Here", select_return)
        assert(select_return['op'] == 'select')
        assert(select_return['status'] == TSDBStatus.OK)
        assert(select_return['payload'][1] == {})
        assert(select_return['payload'][2] == {})
        
        # Test Protocol Select
        metadata_dict = {'pk': {'>': 0}}
        fields = ['ts']
        additional = None
        select_op = TSDBOp_Select(tid, metadata_dict, fields, additional)
        select_return = prot._select(select_op)
        assert(select_return['op'] == 'select')
        assert(select_return['status'] == TSDBStatus.OK)
        assert(select_return['payload'][1]['ts'] == ats1)
        assert(select_return['payload'][2]['ts'] == ats2)
        
        # Test Add Trigger
        add_trigger_op = TSDBOp_AddTrigger(tid, 'stats', 'insert_ts', ['mean', 'std'], None)
        prot._add_trigger(add_trigger_op)
        
        mod = import_module('procs.stats')
        storedproc = getattr(mod,'main')
        
        assert(server.triggers['insert_ts'] ==  [('stats', storedproc, None, ['mean', 'std'])])
        
        
        #prot._insert_ts(TSDBOp_InsertTS(3, ats1))
        #time.sleep(1)
        #inserted_row = server.db.rows[3]
        #assert(inserted_row['mean'] == ats1)
        #assert(inserted_row['std'] == ats1)