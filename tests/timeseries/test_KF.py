import timeseries.set_compiler
timeseries.set_compiler.install()

import scipy.optimize

import pyximport
pyximport.install()

import numpy as np

import KF

import timeseries as ts
import numpy as np




def test_KF():
    sigeta = np.random.normal(0,1,2000)#scipy.stats.norm.rvs(0, 1, 2000)
    sigeps = np.random.normal(0,10,2000)#scipy.stats.norm.rvs(0, 10, 2000)

    mus = np.cumsum(sigeta)+20
    v = mus + sigeps

    t = np.arange(2000)
    ats = ts.TimeSeries(t, v)

    v2 = np.array(ats.values()).astype(np.double)

    logL_LLy = lambda x: KF.logL_LL(x[0], x[1], v2)
    sigma_epsilon, sigma_eta = scipy.optimize.fmin(logL_LLy,[v2.std()/2,v2.std()/2])
    assert(np.isclose(sigma_epsilon, 10, rtol = 0.1))
    assert(np.isclose(sigma_eta, 1, rtol = 0.1))