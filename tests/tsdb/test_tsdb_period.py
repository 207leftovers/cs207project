from tsdb import TSDBClient
import timeseries as ts
import numpy as np
import subprocess
import unittest
import asyncio
import asynctest
import time


def basic_irregular(stopTime, numPoints, numSelPoints):
    meta={}
    meta['order'] = int(np.random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]))
    meta['blarg'] = int(np.random.choice([1, 2]))
    time = np.linspace(0, stopTime, numPoints)
    data = np.sin(time)
    index = np.sort(np.random.choice(range(numPoints), size=numSelPoints, replace=False))
    time_irr = time[index]
    data_irr = data[index]
    return meta, ts.TimeSeries(time_irr, data_irr)

class Test_TSDB_Period(asynctest.TestCase):

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

    def tearDown(self):
        ################
        ### SHUTDOWN ###
        ################
        # Shuts down the server
        self.server_proc.terminate()
        self.server_log_file.close()
        time.sleep(1)
    
    async def test_period_ts(self):


        stopTime = 20
        numPoints = 200
        numSelPoints = 60
        meta, ats = basic_irregular(stopTime, numPoints, numSelPoints)
            
        # Setup Client
        client = TSDBClient()
        
        # Begin Transaction
        status, tid = await client.begin_transaction() 
        
        # Add Trigger
        await client.add_trigger(tid, 'period', 'insert_ts', ['period'], None)
            
        # Insert
        await client.insert_ts(tid, 1, ats)
            
        # Select
        status, payload = await client.select(tid, {'pk':{'==':1}}, ['period'], None)
        print(payload['1'])
        assert(np.abs(payload['1']['period'] - 6.28) < 0.5)
        

