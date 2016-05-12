import numpy as np
np.random.seed(0)
from procs import _corr
from timeseries import TimeSeries


def test_tsmaker():
    # Setting seed to equate the two timeseries
    _,t1 = _corr.tsmaker(0.5, 0.1, 0.01)
    assert(len(t1.values()) == 100)

def test_randomts():
    t1 = _corr.random_ts(0.5)
    assert(len(t1.values()) == 100)

def test_stand():
    t1 = TimeSeries([1, 2, 3, 4], [40, 50, 60, 70])
    val = _corr.stand(np.array(t1.values()), 55.0, 10)
    assert(list(val) == [-1.5, -0.5, 0.5, 1.5])

def test_ccor():
    # Testing the corr function independently
    t1 = TimeSeries([1, 2, 3, 4], [40, 50, 60, 70])
    t2 = TimeSeries([1, 2, 3, 4], [40, 50, 60, 70])
    val = _corr.ccor(t1, t2)
    assert(list(np.real(val)) == [3150.0, 3000.0, 2950.0, 3000.0])
    assert(list(np.imag(val)) == [0, 0, 0, 0])

def test_maxcorr():
    t1 = TimeSeries([1, 2, 3, 4], [40, 50, 60, 70])
    t2 = TimeSeries([1, 2, 3, 4], [50, 60, 70, 40])
    standts1 = _corr.stand(t1, t1.mean(), t1.std())
    standts2 = _corr.stand(t2, t2.mean(), t2.std())
    idx, mcorr = _corr.max_corr_at_phase(standts1, standts2)
    #idx should be equal to one since the second ts is shifted by 1
    assert(idx == 1)
    assert(np.real(mcorr) == 1)

def test_kernelcorr():
    t1 = TimeSeries([1, 2, 3, 4], [40, 50, 60, 70])
    t2 = TimeSeries([1, 2, 3, 4], [40, 50, 60, 70])
    standts1 = _corr.stand(t1, t1.mean(), t1.std())
    standts2 = _corr.stand(t2, t2.mean(), t2.std())
    # Kernel_corr should return a correlation of 1.0 since we use similar timeseries
    assert(_corr.kernel_corr(standts1, standts2, mult=1) == 1.0)