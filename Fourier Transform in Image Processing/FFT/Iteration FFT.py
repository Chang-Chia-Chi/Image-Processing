import numpy as np

def FFT(data):
    data = np.asarray(data, dtype = float) 
    N = np.shape(data)[0]
    if N % 2 != 0:
         raise ValueError("size of input data must be a power of 2")
    
    N_min = min(N,32)  #  ptimum number not to divide further
    x = np.arange(N_min)   # space or time index
    u = np.arange(N_min).reshape((N_min,-1))  # freq. index
    data = np.reshape(data,(N_min,-1))  # reshape input data to compute FFT at once
    twiddle = np.exp(-2j*np.pi*x*u/N_min)
    X = np.dot(twiddle,data)

    while X.shape[0] < N:
        col = X.shape[1]
        Xeven = X[:,:int(col/2)]
        Xodd = X[:,int(col/2):]  
        k = np.arange(X.shape[0])  # freq. index
        W_Nk = np.exp(-1j*np.pi*k/X.shape[0])[:,None]  # twiddle factor and reshape
        Xk_up = Xeven + W_Nk * Xodd  # upper half of FFT
        Xk_low = Xeven - W_Nk * Xodd # lower half of FFT
        X = np.vstack([Xk_up,Xk_low])  # combine two half of FFT
    return X.ravel()

if __name__ == "__main__":
    x = np.random.random(1024)
    print(np.allclose(FFT(x), np.fft.fft(x)))