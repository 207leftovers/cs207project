from tsdb import TSDBClient, TSDB_REST_Client
import timeseries as ts
import numpy as np
import subprocess
import unittest
import asyncio
import asynctest
import time
from scipy.stats import norm

# m is the mean, s is the standard deviation, and j is the jitter
# the meta just fills in values for order and blarg from the schema
def tsmaker(m, s, j):
    "returns metadata and a time series in the shape of a jittered normal"
    meta={}
    meta['order'] = int(np.random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]))
    meta['blarg'] = int(np.random.choice([1, 2]))
    t = np.arange(0.0, 1.0, 0.01)
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return meta, ts.TimeSeries(t, v)
    
class Test_TSDB_Errors(asynctest.TestCase):

    def setUp(self):
        #############
        ### SETUP ###
        #############
        # We'll use a subprocess to run our server script, according to:
        #     http://stackoverflow.com/questions/3781851/run-a-python-script-from-another-python-script-passing-in-args
        # We need this log file for some reason, it throws exceptions without it
        self.server_log_file = open('.tsdb_server.log.test','w')
        self.server_proc = subprocess.Popen(['python', 'go_server_overwrite.py'], 
            stdout=self.server_log_file, stderr=subprocess.STDOUT)
        time.sleep(1)
    
    # This needs to be separate in case the test 
    # fails and then the server will never be shut down
    def tearDown(self):
        ################
        ### SHUTDOWN ###
        ################
        # Shuts down the server
        self.server_proc.terminate()
        self.server_log_file.close()
        time.sleep(1)
    
    async def test_wrong_meta(self):
        # Data
        t = [0,1,2,3,4]
        v = [1.0,2.0,3.0,2.0,1.0]
        ats = ts.TimeSeries(t, v)
            
        # Setup Client
        client = TSDBClient()
        
        # Get Transaction ID
        status, tid = await client.begin_transaction()
            
        # Add Trigger
        await client.add_trigger(tid, 'stats', 'insert_ts', ['mean', 'std'], None)
            
        # Insert
        await client.insert_ts(tid, "1", ats)
            
        # Select
        status, payload = await client.select(tid, {'pk':{'=':"1"}}, ['ts','mean','std'], None)
        assert(status == 1)

    async def test_wrong_field(self):
        # Data
        t = [0,1,2,3,4]
        v = [1.0,2.0,3.0,2.0,1.0]
        ats = ts.TimeSeries(t, v)
            
        # Setup Client
        client = TSDBClient()

        # Get Transaction ID
        status, tid = await client.begin_transaction()
            
        # Add Trigger
        await client.add_trigger(tid, 'stats', 'insert_ts', ['mean', 'std'], None)
            
        # Insert
        await client.insert_ts(tid, "1", ats)
            
        # Select
        status, payload = await client.select(tid, {'pk':{'==':1}}, ['ts','meaen','std'], None)
        assert(status == 0)

    async def test_wrong_meta2(self):
        # Data
        t = [0,1,2,3,4]
        v = [1.0,2.0,3.0,2.0,1.0]
        ats = ts.TimeSeries(t, v)
            
        # Setup Client
        client = TSDBClient()

        # Get Transaction ID
        status, tid = await client.begin_transaction()
            
        # Add Trigger
        await client.add_trigger(tid, 'stats', 'insert_ts', ['mean', 'std'], None)
            
        # Insert
        await client.insert_ts(tid, "1", ats)
            
        # Select
        status, payload = await client.select(tid, {'pk':{'==':5}}, ['ts','meaen','std'], None)
        assert(status == 0)
        assert(len(payload) == 0)

    async def test_default_order(self):
        # Data
        t = [0,1,2,3,4]
        v = [1.0,2.0,3.0,2.0,1.0]
        ats = ts.TimeSeries(t, v)
            
        # Setup Client
        client = TSDBClient()

        # Get Transaction ID
        status, tid = await client.begin_transaction()
            
        # Add Trigger
        await client.add_trigger(tid, 'stats', 'insert_ts', ['mean', 'std'], None)
            
        # Insert
        await client.insert_ts(tid, "1", ats)
            
        # Select
        status, payload = await client.select(tid, {'order':{'==':0}}, ['ts','meaen','std'], None)
        assert(status == 0)
        assert(len(payload) == 1)

    async def test_bad_TS(self):
        # Setup Client
        client = TSDBClient()

        # Get Transaction ID
        status, tid = await client.begin_transaction()
             
        # Add Trigger
        await client.add_trigger(tid, 'stats', 'insert_ts', ['mean', 'std'], None)
        t = [0,1,2,3,4]
        # Insert
        status, payload = await client.insert_ts(tid, "1", t)
        assert (status == 1)

        # Select
        status, payload = await client.select(tid, {'order':{'==':0}}, ['ts','meaen','std'], None)
        assert(status == 0)
        assert(len(payload) == 0)

        # # Select
        # status, payload = await client.select(tid, {'order':{'==':0}}, ['ts','meaen','std'], None)
        # assert(status == 0)
        # assert(len(payload) == 0)
        
    # async def test_simple_run(self):
    #     # Data
    #     t = [0,1,2,3,4]
    #     v = [1.0,2.0,3.0,2.0,1.0]
    #     ats = ts.TimeSeries(t, v)
            
    #     # Setup Client
    #     client = TSDBClient()
        
    #     # Get Transaction ID
    #     status, tid = await client.begin_transaction()
            
    #     # Add Trigger
    #     await client.add_trigger(tid, 'stats', 'insert_ts', ['mean', 'std'], None)
            
    #     # Insert
    #     await client.insert_ts(tid, "1", ats)
            
    #     # Select
    #     status, payload = await client.select(tid, {'pk':{'==':'1'}}, ['ts','mean','std'], None)
    #     assert(status == 0)

    #     assert(ts.TimeSeries(payload['1']['ts'][0], payload['1']['ts'][1]) == ats)
    #     assert(payload['1']['std'] == 1.4142135623730951)
    #     assert(payload['1']['mean'] == 2.0)
        
    #     # Upsert
    #     await client.upsert_meta(tid, "1", {'order':1})
    #     status, payload = await client.select(tid, {'order':{'==':1}}, ['pk', 'order'], None)
    #     assert(status == 0)
    #     assert(payload['1']['order'] == 1)
        
    #     # Remove Trigger
    #     await client.remove_trigger(tid, 'stats', 'insert_ts')
        
    #     # Insert (No Trigger)
    #     await client.insert_ts(tid, "2", ats)
    #     status, payload = await client.select(tid, {'pk':{'==':"2"}}, ['ts','mean','std'], None)
    #     assert(ts.TimeSeries(payload['2']['ts'][0], payload['2']['ts'][1]) == ats)
    #     assert(payload['2']['std'] == 0)
    #     #assert('mean' not in payload['2'])
        
    #     # Delete 
    #     await client.delete_ts(tid, "1")
    #     status, payload = await client.select(tid, {'pk':{'==':"1"}}, ['ts','mean','std'], None)
    #     assert(status == 0)