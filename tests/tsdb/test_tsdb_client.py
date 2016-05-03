from tsdb import TSDBClient
import timeseries as ts
import numpy as np
import subprocess
import unittest
import asyncio
import asynctest
import time
    
class Test_TSDB_Client(asynctest.TestCase):

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
    
    async def test_run(self):
        #############
        ### SETUP ###
        #############
        # We'll use a subprocess to run our server script, according to:
        #     http://stackoverflow.com/questions/3781851/run-a-python-script-from-another-python-script-passing-in-args
        # We need this log file for some reason, it throws exceptions without it
        self.server_log_file = open('.tsdb_server.log.test','w')
        self.server_proc = subprocess.Popen(['python', 'go_server.py']
            ,stdout=self.server_log_file,stderr=subprocess.STDOUT)
        time.sleep(1)

        # Data
        t = [0,1,2,3,4]
        v = [1.0,2.0,3.0,2.0,1.0]
        ats = ts.TimeSeries(t, v)
            
        # Setup Client
        client = TSDBClient()
            
        # Add Trigger
        await client.add_trigger('stats', 'insert_ts', ['mean', 'std'], None)
            
        # Insert
        await client.insert_ts(1, ats)
        #time.sleep(3)
            
        # Select
        status, payload = await client.select({'pk':{'==':1}}, ['ts','mean','std'], None)
        assert(status == 0)
        assert(ts.TimeSeries(payload['1']['ts'][0], payload['1']['ts'][1]) == ats)
        assert(payload['1']['std'] == 1.4142135623730951)
        assert(payload['1']['mean'] == 2.0)
