import numpy as np
import math
import matplotlib.pyplot as plt

path = "C:/Users/USER/Desktop/Python/影像處理/練習/practice pic2.jpg"
image = plt.imread(path)
img = image.copy()
f = 5 #window size of simlular area
f_r = f//2 #radius of simlular area
s = 21 #window size of search area
s_r = s//2 #radius of search area
h = 8 #degree of filting
variance = 20 #variance of noise in image

def eu_distance(Bi,Bj):
    """
    calculate Euclidean distance between two image region
    Bi & Bj is two image areas in same array size
    """
    f = np.shape(Bi)[0]
    eu_dis = ((Bi - Bj)**2).sum()/(3*(f**2))
    return eu_dis

def weight_func(eu_dis,varian,h):
    var = max(eu_dis-2*varian,0)
    return math.exp(-var/(h**2))

#mirror padding
def mir_padding(img,f):
    imgi , imgj = np.shape(img[:,:,0])
    add_n = f//2
    img_p = np.zeros((imgi+2*add_n,imgj+2*add_n,3))  #create padding image
    img_p[add_n:imgi+add_n,add_n:imgj+add_n,:] = img  #throw original image to padding image
    img_p[0:add_n,add_n:imgj+add_n,:] = img[add_n-1::-1,:,:] # padding upper rows
    img_p[-add_n::1,add_n:imgj+add_n,:] = img[-1:-add_n-1:-1,:,:] # padding bottom rows
    img_p[add_n:imgi+add_n,0:add_n,:] = img[:,add_n-1::-1,:] # padding left column
    img_p[add_n:imgi+add_n,-add_n::1,:] = img[:,-1:-add_n-1:-1,:] # padding right column
    for i in range(f):
        img_p[0:add_n,i,:] = img[add_n-1-i,add_n-1::-1,:] # padding upper-left corner
        img_p[0:add_n,-i,:] = img[add_n-1-i,-add_n::1,:] # padding upper-righ corner
        img_p[-1:-add_n-1:-1,i,:] = img[-add_n+i,add_n-1::-1,:] # padding lower-left corner
        img_p[-1:-add_n-1:-1,-i,:] = img[-add_n+i,-add_n::1,:] # padding lower-right corner
    return img_p

img_p = mir_padding(img,f) #mirror padding
ix , iy = np.shape(img[:,:,0]) # image size

NLu = np.zeros([ix,iy,3]) # create new image
for k in range(ix):
  for m in range(iy):
    Bp = img_p[k:k+f,m:m+f,:]
    Cp = 0
    wuj = np.zeros([f,f,3])

    #find points meet size of search area
    mod_numx = abs(min(k - s_r + f_r,0))
    upper_search = max(k - s_r + f_r,0)
    lower_search = min(k + s_r - f_r + mod_numx,ix)
    mod_numy = abs(min(m - s_r + f_r,0))
    left_search = max(m - s_r + f_r,0)
    right_search = min(m + s_r - f_r + mod_numy,iy)
    for i in range(upper_search,lower_search):
        for j in range(left_search,right_search):
            Bq = img_p[i:i+f,j:j+f,:]
            eu_dis = eu_distance(Bp,Bq)
            weight = weight_func(eu_dis,variance,h)
            Cp += weight
            wuj += weight*Bq
    Bi = wuj/Cp
    NLu[k,m,:] = Bi.sum(axis = (0,1))/(f**2)

NLu = np.rint(NLu)
plt.imshow(NLu)