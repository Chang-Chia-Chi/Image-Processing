import numpy as np

def DFT(data):
    data = np.asarray(data, dtype = float)  # time or space input
    N = np.shape(data)[0]  # compute input size
    x = np.arange(N)  # space sample index
    u = np.reshape(x,(N,1))  # freq. sample index
    twiddle = np.exp(-1j*2*np.pi*u*x/N)  # exponetial coefficient
    return np.dot(twiddle,data)

def FFT(data):
    data = np.asarray(data, dtype = float)  # time or space input
    N = np.shape(data)[0]  # compute input size
    if N % 2 != 0:
        raise ValueError("size of input data must be a power of 2")
    elif N <= 32:  # optimum number not to divide further
        return DFT(data)
    else:
        Xeven = FFT(data[::2])  # divided even part
        Xodd = FFT(data[1::2])  # divided odd part
        k = np.arange(N)   # freq. index
        twiddle = np.exp(-1j*2*np.pi*k/N)  # twiddle factor
        Xk_up = Xeven + twiddle[:int(N/2)] * Xodd  # upper half of FFT
        Xk_low = Xeven + twiddle[int(N/2):] * Xodd # lower half of FFT
        Xk = np.concatenate([Xk_up,Xk_low])  # combine two half of FFT
        return Xk

if __name__ == "__main__":
    x = np.random.random(1024)
    print(np.allclose(FFT(x), np.fft.fft(x)))