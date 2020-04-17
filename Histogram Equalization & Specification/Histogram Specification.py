import numpy as np
import matplotlib.pyplot as plt
import cv2

s_image = cv2.imread("C:/Users/USER/Desktop/Python/Image Processing/practice/Histogram Specification_source.jpg") # source image
d_image = cv2.imread("C:/Users/USER/Desktop/Python/Image Processing/practice/Histogram Specification_destination.jpg") # destination image
ix , iy = np.shape(s_image[:,:,0]) # image size
new_image = np.zeros([ix,iy,3]) # create new image which will be construct by histogram specification using source image
bits =8 
L = 2**bits

s_pdf_array = np.zeros([256,3]) # create possibility density function of s_image 
d_pdf_array = np.zeros([256,3]) # create possibility density function of d_image histogram 
tran_s_array = np.zeros([256,3]) # create transfer function of s_image
tran_d_array = np.zeros([256,3]) # create transfer function of d_image

# calculate possibility density function and transfer function of source and destination image
for i in range(3):
    s_pdf_array[:,i] = [np.sum(s_image[:,:,i] == g_lev)/(ix*iy) for g_lev in range(256) ]
    d_pdf_array[:,i] = [np.sum(d_image[:,:,i] == g_lev)/(ix*iy) for g_lev in range(256) ]

    tran_s_array[:,i] = [(L-1)*np.sum(s_pdf_array[:g_lev,i], axis = 0) for g_lev in range(256)]
    tran_d_array[:,i] = [(L-1)*np.sum(d_pdf_array[:g_lev,i], axis = 0) for g_lev in range(256)]

tran_s_array = tran_s_array.astype("int") # transfer value type to int
tran_d_array = tran_d_array.astype("int") # transfer value type to int


# compute corresponding zq 
zq_array = np.zeros([256,3])
for i in range(3):
    for pos, tran_s_glev in enumerate(tran_s_array[:,i]):
        zq = int(np.argmin(abs(tran_d_array[:,i]-tran_s_glev))) 
        zq_array[pos,i] = zq

# construct new_image
new_his_array = np.zeros([256,3])
for i in range(3):
    temp_image = new_image[:,:,i]
    for pos, new_glev in enumerate(zq_array[:,i]):
        temp_image[s_image[:,:,i] == pos] = new_glev
        new_image[:,:,i] = temp_image

    new_his_array[:,i] = [np.sum(new_image[:,:,i] == g_lev) for g_lev in range(256)]

new_image = new_image.astype("uint8")

#cv2.imshow("new image",new_image)
#cv2.waitKey(0)
plt.subplot(221)
plt.title("destination image")
plt.xticks([]) #chancel x ticks
plt.yticks([]) #chancel y ticks
plt.imshow(d_image,cmap="gray") #indicate color map

plt.subplot(222)
plt.title("image constructed by histogram specification ")
plt.xticks([]) #chancel x ticks
plt.yticks([]) #chancel y ticks
plt.imshow(new_image,cmap="gray") #indicate color map

plt.show()