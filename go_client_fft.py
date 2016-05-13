#!/usr/bin/env python3
from tsdb import TSDBClient
import timeseries as ts
import asyncio
import numpy as np
import matplotlib.pyplot as plt

def basic_irregular(stopTime, numPoints, numSelPoints, num):
    """
    Input - 
    stopTime - Maximum time of the signal
    numPoints - Number of points in the signal
    numSelPoints - Number of points to be randomly selected
    num - multiplier inside the sine function

    Output - 
    data_irr - irregular magnitude arrays
    time_irr - irregular time arrays
    Also a timeseries object is returned
    """
    meta={}
    meta['order'] = int(np.random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]))
    meta['blarg'] = int(np.random.choice([1, 2]))
    time = np.linspace(0, stopTime, numPoints)
    data = np.sin(num*time)
    index = np.sort(np.random.choice(range(numPoints), size=numSelPoints, replace=False))
    time_irr = time[index]
    data_irr = data[index]
    return data_irr, time_irr, ts.TimeSeries(data_irr, time_irr)


async def main():
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    client = TSDBClient()
    
    # Begin Transaction
    status, tid = await client.begin_transaction() 

    await client.add_trigger(tid, 'period', 'insert_ts', ['period'], None)#['mean', 'std'], None)#
   
    stopTime = 20
    numPoints = 200
    numSelPoints = 60
    num = 2
    data_irr, time_irr, ats = basic_irregular(stopTime, numPoints, numSelPoints, num)
    await client.insert_ts(tid, 3, ats) 

    print('---------------------')
    status, payload = await client.select(tid, {'pk':{'==':3}}, ['period'], None)
    print("The period of the signal is:", payload['3']['period'])
    
    plt.title('Irregular Time Series')
    plt.plot(time_irr, data_irr, color = 'b')
    plt.show()

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
