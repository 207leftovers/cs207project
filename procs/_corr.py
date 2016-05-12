import numpy.fft as nfft
import numpy as np
import timeseries as ts
from scipy.stats import norm

def tsmaker(m, s, j):
    meta={}
    meta['order'] = int(np.random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]))
    meta['blarg'] = int(np.random.choice([1, 2]))
    t = np.arange(0.0, 1.0, 0.01)
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return meta, ts.TimeSeries(t, v)

def random_ts(a):
    t = np.arange(0.0, 1.0, 0.01)
    v = a*np.random.random(100)
    return ts.TimeSeries(t, v)

# Standardizes the variable x, using the mean m, and standard deviation s
def stand(x, m, s):
    return (x-m)/s

# Given two standardized time series, compute their cross-correlation using FFT
def ccor(ts1, ts2):
    return ((1 / (1. * len(ts1))) * nfft.ifft(nfft.fft(ts1) * np.conjugate(nfft.fft(ts2))).real)
    #return nfft.ifft(nfft.fft(ts1) * np.conj(nfft.fft(ts2)))

def max_corr_at_phase(ts1, ts2):
    ccorts = ccor(ts1, ts2)
    idx = np.argmax(ccorts)
    maxcorr = ccorts[idx]
    return idx, maxcorr

#The equation for the kernelized cross correlation is given at
#http://www.cs.tufts.edu/~roni/PUB/ecml09-tskernels.pdf
#normalize the kernel there by np.sqrt(K(x,x)K(y,y)) so that the correlation
#of a time series with itself is 1.

"""
#Incase multiplier was not being used for generating correlation
def K_function(ts1, ts2):
    ts1_val = ts1.values()
    ts2_val = ts2.values()
    k = 0
    for i in range(len(ts1_val)):
        #Shifting the time series
        ts2_appended = np.concatenate((np.zeros(i), ts2_val[i:]))
        k += np.exp(np.dot(ts1_val, ts2_appended))
    return k
"""
def K_function_mult(ts1, ts2, mult):
    ts1_val = ts1.values()
    ts2_val = ts2.values()
    k = 0
    for i in range(len(ts1_val)):
        #Shifting the time series and computing the dot product for every shift
        ts2_appended = np.concatenate((np.zeros(i), ts2_val[i:]))
        k += np.exp(mult*np.dot(ts1_val, ts2_appended))
    return k

# Compute a kernelized correlation so that we can get a real distance
def kernel_corr(ts1, ts2, mult=1):
    
    # Numerator
    numerator = np.sum(np.exp(mult * ccor(ts1, ts2)))

    # Denominator
    denominator = np.sqrt(np.sum(np.exp(mult * ccor(ts1, ts1))) * np.sum(np.exp(mult * ccor(ts2, ts2))))
    
    if denominator == 0:
        return 0
    else:
        return numerator/denominator


# This is for a quick and dirty test of these functions
# You might need to add procs to pythonpath for this to work
# Commenting this since its not needed anymore
"""
if __name__ == "__main__":
    print("HI")
    _, t1 = tsmaker(0.5, 0.1, 0.01)
    _, t2 = tsmaker(0.5, 0.1, 0.01)
    print(t1.mean(), t1.std(), t2.mean(), t2.std())
    import matplotlib.pyplot as plt
    plt.plot(t1)
    plt.plot(t2)
    plt.show()
    standts1 = stand(t1, t1.mean(), t1.std())
    standts2 = stand(t2, t2.mean(), t2.std())

    idx, mcorr = max_corr_at_phase(standts1, standts2)
    print(idx, mcorr)
    sumcorr = kernel_corr(standts1, standts2, mult=10)
    print(sumcorr)
    t3 = random_ts(2)
    t4 = random_ts(3)
    plt.plot(t3)
    plt.plot(t4)
    plt.show()
    standts3 = stand(t3, t3.mean(), t3.std())
    standts4 = stand(t4, t4.mean(), t4.std())
    idx, mcorr = max_corr_at_phase(standts3, standts4)
    print(idx, mcorr)
    sumcorr = kernel_corr(standts3, standts4, mult=10)
    print(sumcorr)
"""