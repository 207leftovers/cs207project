from tsdb import TSDBClient, TSDB_REST_Client
import timeseries as ts
import numpy as np
import subprocess
import unittest
import asyncio
import asynctest
import time

    
class Test_TSDB_Kalman(asynctest.TestCase):

    def setUp(self):
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
    
    async def test_simple_run(self):

    	client = TSDBClient()

	    await client.add_trigger('KalmanFilter', 'insert_ts', ['sig_epsilon_estimate', 'sig_eta_estimate'], None)#['mean', 'std'], None)#

		sigeta_para = 1
		sigeps_para = 10 
	    sigeta = np.random.normal(0,sigeta_para,2000)
	    sigeps = np.random.normal(0,sigeps_para,2000)

	    mus = np.cumsum(sigeta)+20
	    y = mus + sigeps

	    ats = ts.TimeSeries(y,np.arange(2000))

	    await client.insert_ts(1,ats)
	    await client.upsert_meta(1, {'order': 1})

	    status, payload = await client.select({'order':{'==':1}}, ['sig_epsilon_estimate', 'sig_eta_estimate'], None)


	    assert(np.isclose(payload['1']['sig_epsilon_estimate'], sigeps_para, rtol=0.1))
        assert(np.isclose(payload['1']['sig_eta_estimate'], sigeta_para, rtol=0.1))

