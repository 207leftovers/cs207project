import aiohttp
import asyncio
import json
from tsdb import TSDB_REST_Client
import timeseries as ts
import numpy as np
from scipy.stats import norm
import asyncio
import matplotlib.pyplot as plt

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
    
async def main():
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    client = TSDB_REST_Client()
    await client.add_trigger('junk', 'insert_ts', None, 23)
    await client.add_trigger('stats', 'insert_ts', ['mean', 'std'], None)

    await client.insert_ts('one',ts.TimeSeries([1, 2, 3],[1, 4, 9]))
    await client.insert_ts('two',ts.TimeSeries([2, 3, 4],[4, 9, 16]))
    await client.insert_ts('three',ts.TimeSeries([9,3,4],[4,0,16]))

    await client.remove_trigger('junk', 'insert_ts')
    await client.insert_ts('four',ts.TimeSeries([0,0,4],[1,0,4]))

    await client.upsert_meta('one', {'order': 1, 'blarg': 1})
    await client.upsert_meta('two', {'order': 2})
    await client.upsert_meta('three', {'order': 1, 'blarg': 2})
    await client.upsert_meta('four', {'order': 2, 'blarg': 2})
    print("UPSERTS FINISHED")
    print('---------------------')
    await client.select()
    print('---------------------')
    await client.select(fields=['order'])
    print('---------------------')
    await client.select(fields=[])
    print('---------------------')
    print('---------------------')
    await client.select({'order': 1}, fields=['ts'])
    print('{{{{{{{{{{{{{{}}}}}}}}}}}}}}')
    await client.select({'blarg': 1}, fields=[])
    print('{{{{{{{{{{{{{{}}}}}}}}}}}}}}')
    bla = client.select({'order': 1, 'blarg': 2})
    print("END", bla)
    await client.select({'blarg': {'>=': 2}}, fields=['blarg', 'mean'])
    await client.select({'blarg': {'>=': 2}, 'order': 1}, fields=['blarg', 'std'])
    await client.select({'order': {'>=': 2}}, fields=['order', 'blarg', 'mean'], additional={'sort_by': '-order'})
    await client.select({'order': {'>=': 2}}, fields=['order', 'blarg', 'mean'], additional={'sort_by': '-order', 'limit':2})

    select = await client.select(fields=['order'], additional={'sort_by': '-order'})

async def test2():
    # Data
    t = [0,1,2,3,4]
    v = [1.0,2.0,3.0,2.0,1.0]
    ats = ts.TimeSeries(t, v)
        
    # Setup Client
    client = TSDB_REST_Client()
        
    # Get Transaction ID
    status, tid = await client.begin_transaction()
    
    # Add a trigger. notice the argument. It does not do anything here but
    # could be used to save a shlep of data from client to server.
    await client.add_trigger(tid, 'junk', 'insert_ts', None, 'db:one:ts')
    # our stats trigger
    await client.add_trigger(tid, 'stats', 'insert_ts', ['mean', 'std'], None)
    #Set up 50 time series
    mus = np.random.uniform(low=0.0, high=1.0, size=50)
    sigs = np.random.uniform(low=0.05, high=0.4, size=50)
    jits = np.random.uniform(low=0.05, high=0.2, size=50)

    # dictionaries for time series and their metadata
    tsdict={}
    metadict={}
    for i, m, s, j in zip(range(50), mus, sigs, jits):
        meta, tsrs = tsmaker(m, s, j)
        # the primary key format is ts-1, ts-2, etc
        pk = "ts-{}".format(i)
        tsdict[pk] = tsrs
        meta['vp'] = False # augment metadata with a boolean asking if this is a  VP.
        metadict[pk] = meta

    # Having set up the triggers, now inser the time series, and upsert the metadata
    for k in tsdict:
        await client.insert_ts(tid, k, tsdict[k])
        await client.upsert_meta(tid, k, metadict[k])
        
    print("UPSERTS FINISHED")
    print('---------------------')
    
    print('CREATING VPs')
    # choose 5 distinct vantage point time series
    vpkeys = ["ts-{}".format(i) for i in np.random.choice(range(50), size=5, replace=False)]

    for vpkey in vpkeys:
        await client.create_vp(tid, vpkey)
        
    print('---------------------')
    print("STARTING SELECTS")

    print('---------DEFAULT------------')
    await client.select(tid)

    #in this version, select has sprouted an additional keyword argument
    # to allow for sorting. Limits could also be enforced through this.
    print('---------ADDITIONAL------------')
    await client.select(tid, additional={'sort_by': '-order'})

    print('----------ORDER FIELD-----------')
    _, results = await client.select(tid, fields=['order'])
    for k in results:
        print(k, results[k])

    print('---------ALL FILEDS------------')
    await client.select(tid, fields=[])

    print('------------TS with order 1---------')
    await client.select(tid, metadata_dict={'order': {'==': 1}}, fields=['ts'])

    print('------------All fields, blarg 1 ---------')
    await client.select(tid, {'blarg': 1}, fields=[])

    print('------------order 1 blarg 2 no fields---------')
    _, bla = await client.select(tid, {'order': 1, 'blarg': 2})
    print(bla)

    print('------------order >= 4  order, blarg and mean sent back, also sorted---------')
    _, results = await client.select(tid, {'order': {'>=': 4}}, fields=['order', 'blarg', 'mean'], additional={'sort_by': '-order'})
    for k in results:
        print(k, results[k])

    print('------------order 1 blarg >= 1 fields blarg and std---------')
    _, results = await client.select(tid, {'blarg': {'>=': 1}, 'order': 1}, fields=['blarg', 'std'])
    for k in results:
        print(k, results[k])

    print('------now computing vantage point stuff---------------------')
    print("VPS", vpkeys)

    # We first create a query time series.
    _, query = tsmaker(0.5, 0.2, 0.1)

    print("TS SIMILARITY SEARCH")
    _, tsss = await client.ts_similarity_search(tid, 5, query)

    print("SIMILARS", tsss)
    print(list(tsss.items())[0][0])

    plt.title('TimeSeries')
    plt.plot(query, linewidth=2.0)
    plt.plot(tsdict[list(tsss.items())[0][0]], linewidth=2.0)
    for i in tsdict.values():
        plt.plot(i, alpha = .2)
    plt.show()
    
    plt.title('TimeSeries')
    plt.plot(query, linewidth=2.0)
    for i in tsss.items():
        plt.plot(tsdict[i[0]], linewidth=2.0)
    for i in tsdict.values():
        plt.plot(i, alpha = .2)
    plt.show()

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()