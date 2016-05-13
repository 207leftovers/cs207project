from ._nfft import period
import numpy as np
import asyncio


def proc_main(pk, row, arg):
    rowts = row['ts']
    time_irr = rowts._times
    mag_irr = rowts._values
    time_period = period(mag_irr, time_irr)
    return [time_period]

async def main(pk, row, arg):
    return proc_main(pk, row, arg)
