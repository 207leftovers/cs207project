#!/usr/bin/env python3
from tsdb import TSDBClient
import timeseries as ts
import asyncio
import numpy as np

import pyximport
pyximport.install()

import timeseries.KF as KF

import matplotlib.pyplot as plt

from scipy.stats.stats import pearsonr


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

    tot = 600

    period = 6
    t = 10

    hbts = np.random.normal(0,5,tot)
    for i in range(0, 6):
        for j in range(-t, t):
            try:
                hbts[tot//period*i+j] += 200*np.sin(-j/t/3.1416)+np.random.normal(0,5)
            except:
                pass

    ats = ts.TimeSeries(np.arange(600), hbts)

        
    # Setup Client
    client = TSDBClient()
    
    # Begin Transaction
    status, tid = await client.begin_transaction()
    
    # Add Trigger
    await client.add_trigger(tid, 'corr', 'insert_ts', ['std'], None)
        
    # Insert
    await client.insert_ts(tid, 1, ats)

    x = np.arange(1,200)
    y = []
    for i in range(1,200):
        y += [pearsonr(hbts[:-i], hbts[i:])]
    y = np.array(y)

    plt.title('Simulated heartbeat')
    plt.plot(hbts, color = 'g')
    plt.show()
    plt.title('Autocorrelation')
    plt.plot(x, y[:, 0], color = 'b')
    plt.show()



if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
