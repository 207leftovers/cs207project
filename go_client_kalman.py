#!/usr/bin/env python3
from tsdb import TSDBClient
import timeseries as ts
import asyncio
import numpy as np

import pyximport
pyximport.install()

import timeseries.KF as KF

import matplotlib.pyplot as plt


async def main():
    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    # client = TSDBClient()

    # # Begin Transaction
    # status, tid = await client.begin_transaction()

    # await client.add_trigger(tid, 'KalmanFilter', 'insert_ts', ['sig_epsilon_estimate', 'sig_eta_estimate'], None)#(1, 'KalmanFilter', 'insert_ts', ['sig_epsilon_estimate', 'sig_eta_estimate'], None)

    # sigeta = np.random.normal(0,1,2000)
    # sigeps = np.random.normal(0,10,2000)

    # mus = np.cumsum(sigeta)+20
    # y = mus + sigeps

    # await client.insert_ts(tid, 'one',ts.TimeSeries(y,np.arange(2000)))#(1, 'one',ts.TimeSeries(y,np.arange(2000)))
    # await client.upsert_meta(tid, 'one', {'order': 1, 'blarg': 1})#(1, 'one', {'order': 1, 'blarg': 1})

    # status, payload = await client.select(tid)
    # print('---------------------')
    # print(payload)

    # sig_epsilon_estimate = payload['one']['sig_epsilon_estimate']
    # sig_eta_estimate = payload['one']['sig_eta_estimate']





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
    
    # Add Trigger
    await client.add_trigger(tid, 'KalmanFilter', 'insert_ts', ['sig_epsilon_estimate', 'sig_eta_estimate'], None)
        
    # Insert
    await client.insert_ts(tid, 1, ats)
        
    # Select
    status, payload = await client.select(tid, {'pk':{'==':1}}, ['sig_epsilon_estimate','sig_eta_estimate'], None)

    sig_epsilon_estimate = payload['1']['sig_epsilon_estimate']
    sig_eta_estimate = payload['1']['sig_eta_estimate']

    KFresult = KF.KF(v, sig_epsilon_estimate, sig_eta_estimate)
    filtered = KFresult['Predict']

    plt.title('Kalman Filtered')
    plt.plot(filtered)
    plt.show()



if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
