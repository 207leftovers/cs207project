import aiohttp
import asyncio
import json
from tsdb import TSDB_REST_Client
import timeseries as ts



async def main():
    client = TSDB_REST_Client()
    #ppl = open('standardize.ppl').read()
    await client.add_trigger('junk', 'insert_ts', None, 23)
    #client.add_trigger('junk', 'select', None, 23)
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
        
    # Add Trigger
    await client.add_trigger(tid,'stats', 'insert_ts', ['mean', 'std'], None)
        
    # Insert
    await client.insert_ts(tid, 1, ats)
        
    # Select
    status, payload = await client.select(tid, {'pk':{'==':1}}, ['ts','mean','std'], None)
    assert(status == 0)

    assert(ts.TimeSeries(payload['1']['ts'][0], payload['1']['ts'][1]) == ats)
    assert(payload['1']['std'] == 1.4142135623730951)
    assert(payload['1']['mean'] == 2.0)




    #FINALLY WORKING!!! YAY!!!
    
    # Upsert
    await client.upsert_meta(tid, 1, {'order':1})
    status, payload = await client.select(tid, {'order':{'==':1}}, ['pk', 'order'], None)
    assert(status == 0)
    assert(payload['1']['order'] == 1)
    
    # Remove Trigger
    await client.remove_trigger(tid, 'stats', 'insert_ts')
    
    # Insert (No Trigger)
    await client.insert_ts(tid, 2, ats)
    status, payload = await client.select(tid, {'pk':{'==':2}}, ['ts','mean','std'], None)
    assert(ts.TimeSeries(payload['2']['ts'][0], payload['2']['ts'][1]) == ats)
    #assert('std' not in payload['2'])
    #assert('mean' not in payload['2'])
    
    # # Delete 
    # await client.delete_ts(tid, 1)
    # status, payload = await client.select(tid, {'pk':{'==':1}}, ['ts','mean','std'], None)
    # assert(status == 0)
    # assert(payload == {})
if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test2())
    loop.close()