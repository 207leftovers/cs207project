from tsdb import TSDBClient
import timeseries as ts
import numpy as np
import subprocess
import unittest
import asynctest
import time
    
class Test_TSDB_Client(asynctest.TestCase):

    def test_run(self):
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
        
        # Insert
        client = TSDBClient()
        client.insert_ts(1, ats)
        
        # Select
        status, payload = client.select({'pk':{'==':1}}, ['ts'], None)
        assert(status == 0)
        assert(ts.TimeSeries(payload['1']['ts'][0], payload['1']['ts'][1]) == ats)
        
        
        ################
        ### SHUTDOWN ###
        ################
        # Shuts down the server
        self.server_proc.terminate()
        self.server_log_file.close()
        time.sleep(1)
