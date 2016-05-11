from tsdb import TSDBClient
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
    
class Test_TSDB_Client(asynctest.TestCase):

    def setUp(self):
        #############
        ### SETUP ###
        #############
        # We'll use a subprocess to run our server script, according to:
        #     http://stackoverflow.com/questions/3781851/run-a-python-script-from-another-python-script-passing-in-args
        # We need this log file for some reason, it throws exceptions without it
        self.server_log_file = open('.tsdb_server1.log.test','w')
        self.server_proc = subprocess.Popen(['python', 'go_server.py'], 
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
    
    async def simple_run(self):
        # Data
        t = [0,1,2,3,4]
        v = [1.0,2.0,3.0,2.0,1.0]
        ats = ts.TimeSeries(t, v)
            
        # Setup Client
        client = TSDBClient()
        
        # Begin Transaction
        status, tid = await client.begin_transaction()
        assert(tid == 1)
            
        # Add Trigger
        await client.add_trigger(tid, 'stats', 'insert_ts', ['mean', 'std'], None)
            
        # Insert
        await client.insert_ts(tid, 1, ats)
            
        # Select
        status, payload = await client.select(tid, {'pk':{'==':1}}, ['ts','mean','std'], None)
        assert(status == 0)
        assert(ts.TimeSeries(payload['1']['ts'][0], payload['1']['ts'][1]) == ats)
        print(payload['1'])
        assert(payload['1']['std'] == 1.4142135623730951)
        assert(payload['1']['mean'] == 2.0)
        # FINALLY WORKING!!! YAY!!!
        
        # Upsert
        await client.upsert_meta(tid, 1, {'order':1})
        status, payload = await client.select(tid, {'order':{'==':1}}, ['pk', 'order'], None)
        assert(status == 0)
        assert(payload['1']['order'] == 1)
        
        # Remove Trigger
        await client.remove_trigger(tid, 'stats', 'insert_ts')
        
        # Insert (No Trigger)
        await client.insert_ts(tid, 2, ats)
        status, payload = await client.select(tid, {'pk':{'==':2}}, ['ts','mean','std'], None)
        assert(ts.TimeSeries(payload['2']['ts'][0], payload['2']['ts'][1]) == ats)
        assert('std' not in payload['2'])
        assert('mean' not in payload['2'])
        
        # Delete 
        await client.delete_ts(1)
        status, payload = await client.select(tid, {'pk':{'==':1}}, ['ts','mean','std'], None)
        assert(status == 0)
        assert(payload == {})
        
    # Modeled after go_client.py
    async def test_complex_run(self):
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        # Setup Client
        client = TSDBClient()
        
        # Begin Transaction
        status, tid = await client.begin_transaction()
        assert(tid == 1)

        # Add a trigger. notice the argument. It does not do anything here but
        # it could be used to save a shlep of data from client to server.
        await client.add_trigger(tid, 'junk', 'insert_ts', None, 'db:one:ts')
        # Our stats trigger
        await client.add_trigger(tid, 'stats', 'insert_ts', ['mean', 'std'], None)
        # Set up 50 time series
        mus = np.random.uniform(low=0.0, high=1.0, size=50)
        sigs = np.random.uniform(low=0.05, high=0.4, size=50)
        jits = np.random.uniform(low=0.05, high=0.2, size=50)

        # Dictionaries for time series and their metadata
        tsdict={}
        metadict={}
        for i, m, s, j in zip(range(50), mus, sigs, jits):
            meta, tsrs = tsmaker(m, s, j)
            # the primary key format is ts-1, ts-2, etc
            pk = "ts-{}".format(i)
            tsdict[pk] = tsrs
            meta['vp'] = False # augment metadata with a boolean asking if this is a  VP.
            metadict[pk] = meta
    
        # Choose 5 distinct vantage point time series
        vpkeys = ["ts-{}".format(i) for i in np.random.choice(range(50), size=5, replace=False)]
        for i in range(5):
            # add 5 triggers to upsert distances to these vantage points
            await client.add_trigger(tid, 'corr', 'insert_ts', ["d_vp-{}".format(i)], tsdict[vpkeys[i]])
            # change the metadata for the vantage points to have meta['vp']=True
            metadict[vpkeys[i]]['vp']=True
        # Having set up the triggers, now insert the time series, and upsert the metadata
        for k in tsdict:
            await client.insert_ts(tid, k, tsdict[k])
            await client.upsert_meta(tid, k, metadict[k])
    
        select = await client.select(tid)
        # Assert we received all pks
        assert(len(select[1]) == 50)
        # Assert the primary keys have empty dicts
        assert(select[1]['ts-1'] == {})
    
        # In this version, select has sprouted an additional keyword argument
        # to allow for sorting. Limits could also be enforced through this.
        select = await client.select(tid, fields=['order'], additional={'sort_by': '-order'})
        print(select)
        # TODO: DO NOT APPEAR TO BE IN ORDER
        for x in range(1, len(select[1])):
            assert(select[1][list(select[1].keys())[x]]['order'] <= select[1][list(select[1].keys())[x-1]]['order'])
    
        # print('----------ORDER FIELD-----------')
        # _, results = await client.select(fields=['order'])
        # for k in results:
        #     print(k, results[k])
    
        # print('---------ALL FILEDS------------')
        # await client.select(fields=[])
    
        # print('------------TS with order 1---------')
        # await client.select({'order': 1}, fields=['ts'])
    
        # print('------------All fields, blarg 1 ---------')
        # await client.select({'blarg': 1}, fields=[])
    
        # print('------------order 1 blarg 2 no fields---------')
        # _, bla = await client.select({'order': 1, 'blarg': 2})
        # print(bla)
    
        # print('------------order >= 4  order, blarg and mean sent back, also sorted---------')
        # _, results = await client.select({'order': {'>=': 4}}, fields=['order', 'blarg', 'mean'], additional={'sort_by': '-order'})
        # for k in results:
        #     print(k, results[k])

        # print('------------order 1 blarg >= 1 fields blarg and std---------')
        # _, results = await client.select({'blarg': {'>=': 1}, 'order': 1}, fields=['blarg', 'std'])
        # for k in results:
        #     print(k, results[k])

        # print('------now computing vantage point stuff---------------------')
        # print("VPS", vpkeys)
    
        # #we first create a query time series.
        # _, query = tsmaker(0.5, 0.2, 0.1)

        # your code here begins
    
        # Step 1: in the vpdist key, get  distances from query to vantage points
        # this is an augmented select
    
        #1b: choose the lowest distance vantage point
        # you can do this in local code
    
        # Step 2: find all time series within 2*d(query, nearest_vp_to_query)
        #this is an augmented select to the same proc in correlation
    
        #2b: find the smallest distance amongst this ( or k smallest)
        #you can do this in local code
        #your code here ends
        # plot the timeseries to see visually how we did.
        #import matplotlib.pyplot as plt
        #plt.plot(query)
        #plt.plot(tsdict[nearestwanted])
        #plt.show()