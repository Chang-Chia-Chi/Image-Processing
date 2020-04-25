import numpy as np

def DFT(data):
    """
    important concept learned here is if a number Nmn is a function of two variables
    create m (N X 1) and n (1 X N) array then apply function using these two array
    to obtain vectorized result.
    
    data could be list or array type object
    """
    data = np.asarray(data, dtype = float)  # time or space input
    N = np.shape(data)[0]  # compute input size
    x = np.arange(N)  # space sample index
    u = np.reshape(x,(N,1))  # freq. sample index
    twiddle = np.exp(-1j*2*np.pi*u*x/N)  # exponetial coefficient
    return np.dot(twiddle,data)
