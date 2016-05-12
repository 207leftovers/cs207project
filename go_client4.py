import aiohttp
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
    

async def test2():
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
    
if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test2())
    loop.close()