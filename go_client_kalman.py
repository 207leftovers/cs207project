#!/usr/bin/env python3
from tsdb import TSDBClient
import timeseries as ts
import asyncio
import numpy as np


async def main():
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    client = TSDBClient()

    await client.add_trigger('KalmanFilter', 'insert_ts', ['sig_epsilon_estimate', 'sig_eta_estimate'], None)#['mean', 'std'], None)#

    sigeta = np.random.normal(0,1,2000)
    sigeps = np.random.normal(0,10,2000)

    mus = np.cumsum(sigeta)+20
    y = mus + sigeps

    await client.insert_ts('one',ts.TimeSeries(y,np.arange(2000)))
    await client.upsert_meta('one', {'order': 1, 'blarg': 1})

    print('---------------------')
    await client.select(fields=[])

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()