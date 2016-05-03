from tsdb import TSDBClient
import timeseries as ts
import numpy as np
import subprocess
import unittest
import asynctest
import time
from procs import corr, stats
    
def test_corr2():
    t = [1, 2, 3, 4]
    v = [40, 50, 60, 70]
    t2 = [1, 2, 3, 4]
    v2 = [40, 50, 60, 70]
    row = {}
    row['ts'] = ts.TimeSeries(t,v)
    #Since its the same time series, the correlation here should be zero
    assert(corr.proc_main(1, row, (t2, v2))[0] == 0)







