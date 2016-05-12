import numpy as np
from procs import KalmanFilter
from timeseries import TimeSeries

def test_locallevelmodel():
    sigeta = np.random.normal(0,1,2000)
    sigeps = np.random.normal(0,10,2000)

    mus = np.cumsum(sigeta)+20
    v = mus + sigeps

    t = np.arange(2000)
    ats = TimeSeries(t, v)

    #v2 = np.array(ats.values()).astype(np.double)

    sigma_epsilon, sigma_eta = KalmanFilter.proc_main(1,{'ts':ats},None)
    assert(np.isclose(sigma_epsilon, 10, rtol = 0.1))
    assert(np.isclose(sigma_eta, 1, rtol = 0.1))
