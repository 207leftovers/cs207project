#!/usr/bin/env python3
from tsdb import TSDBClient
import timeseries as ts
import asyncio
import numpy as np
import os
import matplotlib.pyplot as plt
import pyximport
pyximport.install()

import timeseries.KF as KF

#only visible files
def listdir_nohidden(path):
    list_files = []
    for f in os.listdir(path):
        if not f.startswith('.'):
            list_files.append(f)
    return list_files


def gen_data(filename, datapath):
    filepath = os.path.join(datapath, filename)
    data = []
    with open(filepath) as f:
        lines = f.readlines()
        header = [str(val) for val in lines[2].split(' ')]
        for line in lines[3:]:
            data.append([float(val) for val in line.split(' ')])
    data = np.array(data)
    data_irr = data[:,1]
    time_irr = data[:,0]
    return data_irr, time_irr, ts.TimeSeries(data_irr, time_irr)


async def main():
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    client = TSDBClient()
    
    # Begin Transaction
    status, tid = await client.begin_transaction() 

    await client.add_trigger(tid, 'period', 'insert_ts', ['period'], None)
    await client.add_trigger(tid, 'KalmanFilter', 'insert_ts', ['sig_epsilon_estimate', 'sig_eta_estimate'], None)
    
    #data manupulation
    datapath = os.path.join(os.getcwd(), 'data/ML/')
    fileList = listdir_nohidden(datapath)
    filename = fileList[0]
    data_irr, time_irr, ats = gen_data(filename, datapath)

    await client.insert_ts(tid, 1, ats)
    print('---------------------')
    status, payload = await client.select(tid, {'pk':{'==':1}}, ['period','sig_epsilon_estimate','sig_eta_estimate'], None)
    print("The period of the signal is:", payload['1']['period'])
    
    sig_epsilon_estimate = payload['1']['sig_epsilon_estimate']
    sig_eta_estimate = payload['1']['sig_eta_estimate']

    KFresult = KF.KF(data_irr, sig_epsilon_estimate, sig_eta_estimate)
    filtered = KFresult['Predict']

    plt.title('Micro-lensing')
    plt.plot(time_irr[1:], data_irr[1:], color = 'b',alpha = 0.4, label='original')
    plt.plot(time_irr[1:], filtered[1:], color = 'g', label='kalman-filtered')
    plt.legend()
    plt.show()

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
