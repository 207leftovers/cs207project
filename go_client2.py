#!/usr/bin/env python3
from tsdb import TSDBClient
import timeseries as ts
import asyncio


async def main():
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    client = TSDBClient()

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

    for x in range(1, len(select[1])):
        print (list(select[1].keys())[x])
        assert(select[1][list(select[1].keys())[x]]['order'] <= select[1][list(select[1].keys())[x-1]]['order'])
if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()