cimport cython
import numpy as np
@cython.boundscheck(False)
@cython.wraparound(False)

cpdef KF(double[:] X, double sigma_epsilon, double sigma_eta):
    cdef int T = len(X)
    cdef double s_eps2 = sigma_epsilon**2
    cdef double s_eta2 = sigma_eta**2

    cdef double [:] mMstore = np.zeros(T)
    cdef double [:] mM_Lstore = np.zeros(T)
    cdef double [:] mPstore = np.zeros(T)
    cdef double [:] mP_Lstore = np.zeros(T)
    cdef double [:] mVstore = np.zeros(T)
    cdef double [:] mFstore = np.zeros(T)

    cdef double m = 0.
    cdef double P = 100000.
    
    cdef:
        double m_L, P_L, aF, v, K
    
    for i in range(T):
        m_L = m # m_t|t-1
        P_L = P + s_eta2 # P_t|t-1
        aF = P_L + s_eps2
        v = X[i] - m_L
        K = P_L/aF
        P = P_L*(1.0-K) #P_t|t
        m = m_L + K*v # m_t|t
        mMstore[i] = m
        mM_Lstore[i] = m_L
        mPstore[i] = P
        mP_Lstore[i] = P_L
        mVstore[i] = v
        mFstore[i] = aF
    
    return {'mFilter': mMstore,
            'Predict': mM_Lstore,
            'PFilter': mPstore,
            'PPredict': mP_Lstore,
            'mErrors': mVstore,
            'mErrVar': mFstore}

cpdef logL(double [:] mErr, double [:] mVar):
    return np.sum(-0.5*np.log(mVar) -0.5*(np.array(mErr)*np.array(mErr)/np.array(mVar)))

cpdef logL_LL(double sigma_epsilon, double sigma_eta, double [:] Y):
    output = KF(Y, sigma_epsilon, sigma_eta)
    cdef double logL1 = logL(output['mErrors'],output['mErrVar'])
    return -logL1