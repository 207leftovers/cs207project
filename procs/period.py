from ._nfft import _nfft
import numpy as np
import asyncio

def period(time_irr, data_irr, ofac=4):
    fx, fy, nout = _nfft(data_irr,time_irr, ofac, 100.)  
    max_idx = np.argmax(fy)
    period = fx[max_idx]
    T = 1.0 / period
    new_time = np.mod(time_irr, 2 * T) / (2 * T)
    return T


def proc_main(pk, row, arg):
    rowts = row['ts']
    time_irr = rowts._times
    mag_irr = rowts._values
    time_period = period(time_irr, mag_irr)
    return [time_period]

async def main(pk, row, arg):
    return proc_main(pk, row, arg)
