from tsdb import TSDBClient
import timeseries as ts
import numpy as np
import subprocess
import unittest
import asyncio
import asynctest
import time
from scipy.stats import norm

#import timeseries.set_compiler as set_compiler
#set_compiler.install()

import pyximport
pyximport.install()

import numpy as np

import timeseries.KF as KF

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
    
class Test_TSDB_KF(asynctest.TestCase):

    def setUp(self):
        #############
        ### SETUP ###
        #############
        # We'll use a subprocess to run our server script, according to:
        #     http://stackoverflow.com/questions/3781851/run-a-python-script-from-another-python-script-passing-in-args
        # We need this log file for some reason, it throws exceptions without it
        self.server_log_file = open('.tsdb_server1.log.test','w')
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
    
    async def test_KF(self):



        sigeta = np.random.normal(0,1,2000)#scipy.stats.norm.rvs(0, 1, 2000)
        sigeps = np.random.normal(0,10,2000)#scipy.stats.norm.rvs(0, 10, 2000)

        mus = np.cumsum(sigeta)+20
        v = mus + sigeps

        t = np.arange(2000)
        ats = ts.TimeSeries(v,t)
            
        # Setup Client
        client = TSDBClient()
        
        # Begin Transaction
        status, tid = await client.begin_transaction()
        assert(tid == 1)
        
        # Add Trigger
        await client.add_trigger(tid, 'KalmanFilter', 'insert_ts', ['sig_epsilon_estimate', 'sig_eta_estimate'], None)
            
        # Insert
        await client.insert_ts(tid, 1, ats)
            
        # Select
        status, payload = await client.select(tid, {'pk':{'==':1}}, ['sig_epsilon_estimate','sig_eta_estimate'], None)
        assert(np.isclose(payload['1']['sig_epsilon_estimate'], 10, rtol = 0.2))
        assert(np.isclose(payload['1']['sig_eta_estimate'], 1, rtol = 0.2))
        
