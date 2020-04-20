import numpy as np
import matplotlib.pyplot as plt

path = "C:/Users/USER/Desktop/Python/Image Processing/practice/practice pic2.jpg"
s_image = plt.imread(path)

def median_filter(s_image,f = 7):
    ix , iy = np.shape(s_image[:,:,0]) # image size
    new_image = np.zeros([ix,iy,3]) # create new image

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
    
    pad_image = mir_padding(s_image,f) # image padding

    # median calculate
    def median_kernel(block):
        seq = np.reshape(block,(f**2,3))
        seq = np.sort(seq,axis = 0)
        mid_point = (f**2)//2
        median = seq[mid_point,:]
        return median

    for i in range(ix):
        for j in range(iy):
            block = pad_image[i:i+f,j:j+f,:]
            median = median_kernel(block)
            new_image[i,j,:] = median
    
    return new_image

new_image = median_filter(s_image)
new_image = new_image.astype("uint8")

plt.subplot(221)
plt.title("original picture")
plt.xticks([]) #chancel x ticks
plt.yticks([]) #chancel y ticks
plt.imshow(s_image) #indicate color map

plt.subplot(222)
plt.title("median filter")
plt.xticks([]) #chancel x ticks
plt.yticks([]) #chancel y ticks
plt.imshow(new_image) #indicate color map

plt.show()


