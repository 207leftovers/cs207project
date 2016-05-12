import numpy as np  
from numpy.fft import *

def _spread(y, yy, n, x, m):
    """
    Given an array yy, extirpolate  a value y into 
    m actual array elements that best approximate the array element number x.
    Need to call for every value in an array(In place operations)
    Input -
    y - Input value
    yy - Actual array to which value is to be extirpolated
    n - Maximum frequency
    x - Element number being approximated
    m - Number of points to be interpolated for 1/4th cycle.
    """
    nfac=[0,1,1,2,6,24,120,720,5040,40320,362880]  
    if m > 10. :  
        print('factorial table too small in spread')
        return  
  
    ix=int(x)  
    if x == float(ix):   
        yy[ix]=yy[ix]+y  
    else:  
        ilo = int(x-0.5*float(m)+1.0)  
        ilo = min( max( ilo , 1 ), n-m+1 )   
        ihi = ilo+m-1  
        nden = nfac[m]  
        fac=x-ilo  
        for j in range(ilo+1,ihi+1): 
            fac = fac*(x-j)  
        yy[ihi] = yy[ihi] + y*fac/(nden*(x-ihi))  
        for j in range(ihi-1,ilo-1,-1):  
            nden=(nden/(j+1-ilo))*(j-ihi)  
            yy[j] = yy[j] + y*fac/(nden*(x-j))


def _nfft(mag, time,ofac,hifac, MACC=4):
    """
    Input-
    mag - List of magnitudes
    time - List of time values corresponding to the magnitude
    ofac - Oversampling factor
    hifac - Highest frequency for which periodogram is to be constructed.

    Output- 
    Wk1 : An array of frequencies. 
    Wk2 : An array of corresponding values of the periodogram. 
    nout : Wk1 & Wk2 dimensions (number of calculated frequencies) 
    """
    n = len(time)
    #Arrays are to be of length if its possible to get the FFT
    assert n == len(mag)

    nout  = 0.5*ofac*hifac*n  
    nfreqt = ofac*hifac*n*MACC  #Size the FFT as next power  
    nfreq = 64             # of 2 above nfreqt.  
    
    while nfreq < nfreqt:   
        nfreq = 2*nfreq

    ndim = 2*nfreq
    #Compute the mean, variance  
    mean = np.mean(mag)  
    ##sample variance because the divisor is N-1  
    var = ((mag-mean)**2).sum()/(len(mag)-1) 
    # and range of the data.  
    xmin = time.min()  
    xmax = time.max()  
    xdif = xmax-xmin
    
    fac  = ndim/(xdif*ofac)  
    fndim = ndim  
    ck  = ((time-xmin)*fac) % fndim  
    ckk  = (2.0*ck) % fndim

    #extirpolate the data  
    wk1 = np.zeros(ndim, dtype='complex')  
    wk2 = np.zeros(ndim, dtype='complex') 

    #calling spread in order to compute FFT later
    for j in range(0, n):  
        _spread(mag[j]-mean,wk1,ndim,ck[j],MACC)  
        _spread(1.0,wk2,ndim,ckk[j],MACC)


    #Take the Fast Fourier Transforms  
    wk1 = ifft( wk1 )*len(wk1)  
    wk2 = ifft( wk2 )*len(wk1)  
  
    wk1 = wk1[1:nout+1]  
    wk2 = wk2[1:nout+1]  
    real_wk1 = wk1.real  
    imag_wk1 = wk1.imag  
    real_wk2 = wk2.real  
    imag_wk2 = wk2.imag

    #Diff factor
    df  = 1.0/(xdif*ofac)

    #Compute the Lomb value for each frequency  
    hypo = 2.0 * abs(wk2)
    #hc2wt - Represents half cos(2*w*t) term
    #hs2wt - Represents half sin(2*w*t) term
    hc2wt = real_wk2/hypo
    hs2wt = imag_wk2/hypo  
    #cwt - Represents cos(w*t) term
    #swt - Represents sin(w*t) term
    cwt  = np.sqrt(0.5+hc2wt)  
    swt  = np.sign(hs2wt)*(np.sqrt(0.5-hc2wt))
    #den - calculating denominator in order to compute the sin and cos term
    den  = 0.5*n+hc2wt*real_wk2+hs2wt*imag_wk2
    #cterm - cos term coefficients
    #sterm - sin term coefficients
    cterm = (cwt*real_wk1+swt*imag_wk1)**2./den  
    sterm = (cwt*imag_wk1-swt*real_wk1)**2./(n-den)  
    #Computing the final periodogram values and building the scale of frequencies 
    wk1 = df*(np.arange(nout, dtype='float')+1.)  
    wk2 = (cterm+sterm)/(2.0*var)

    return wk1, wk2, nout





  


