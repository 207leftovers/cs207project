import aiohttp
import asyncio
import json
from tsdb import TSDB_REST_Client
import timeseries as ts



def main():
    client = TSDB_REST_Client()
    client.insert_ts('one',ts.TimeSeries([1, 2, 3],[1, 4, 9]))
    client.insert_ts('two',ts.TimeSeries([2, 3, 4],[4, 9, 16]))
    client.insert_ts('three',ts.TimeSeries([9,3,4],[4,0,16]))

    client.insert_ts('four',ts.TimeSeries([0,0,4],[1,0,4]))

    client.upsert_meta('one', {'order': 1, 'blarg': 1})
    client.upsert_meta('two', {'order': 2})
    client.upsert_meta('three', {'order': 1, 'blarg': 2})
    client.upsert_meta('four', {'order': 2, 'blarg': 2})

    print('---------------------')
    client.select()
    print('---------------------')
    client.select(fields=['order'])
    print('---------------------')
    client.select(fields=[])
    print('---------------------')
    print('---------------------')
    client.select({'order': 1}, fields=['ts'])
    print('{{{{{{{{{{{{{{}}}}}}}}}}}}}}')
    client.select({'blarg': 1}, fields=[])
    print('{{{{{{{{{{{{{{}}}}}}}}}}}}}}')
    bla = client.select({'order': 1, 'blarg': 2})
    print("END", bla)
    client.select({'blarg': {'>=': 2}}, fields=['blarg', 'mean'])
    client.select({'blarg': {'>=': 2}, 'order': 1}, fields=['blarg', 'std'])
    client.select({'order': {'>=': 2}}, fields=['order', 'blarg', 'mean'], additional={'sort_by': '-order'})
    client.select({'order': {'>=': 2}}, fields=['order', 'blarg', 'mean'], additional={'sort_by': '-order', 'limit':2})


if __name__=='__main__':
    main()