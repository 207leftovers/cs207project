#!/usr/bin/env python3
from tsdb import TSDBClient
import timeseries as ts
import asyncio


async def main():
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    client = TSDBClient()

    await client.add_trigger('junk', 'insert_ts', None, 23)


    await client.insert_ts('one',ts.TimeSeries([1, 2, 3],[1, 4, 9]))


    await client.select()
    print('---------------------')
    await client.select(fields=[])

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()