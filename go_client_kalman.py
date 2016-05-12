#!/usr/bin/env python3
from tsdb import TSDBClient
import timeseries as ts
import asyncio
import numpy as np


async def main():
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    client = TSDBClient()

    # Begin Transaction
    status, tid = await client.begin_transaction()
    assert(tid == 1)

    await client.add_trigger(tid, 'KalmanFilter', 'insert_ts', ['sig_epsilon_estimate', 'sig_eta_estimate'], None)#(1, 'KalmanFilter', 'insert_ts', ['sig_epsilon_estimate', 'sig_eta_estimate'], None)

    sigeta = np.random.normal(0,1,2000)
    sigeps = np.random.normal(0,10,2000)

    mus = np.cumsum(sigeta)+20
    y = mus + sigeps

    await client.insert_ts(tid, 'one',ts.TimeSeries(y,np.arange(2000)))#(1, 'one',ts.TimeSeries(y,np.arange(2000)))
    await client.upsert_meta(tid, 'one', {'order': 1, 'blarg': 1})#(1, 'one', {'order': 1, 'blarg': 1})

    print('---------------------')
    await client.select(tid)

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
