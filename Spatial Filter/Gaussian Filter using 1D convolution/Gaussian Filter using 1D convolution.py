import numpy as np
import matplotlib.pyplot as plt

path = "C:/Users/USER/Desktop/交大在職專班/影像處理/HW/CH3/HW 3_2/N1.bmp"
s_image = plt.imread(path) # source image

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

s_image = rgb2gray(s_image)

def gaussian_filter(img,f,K,var):
    """
    Gaussian Spatial Filter
    img is image to be applied
    f is window size (fXf)
    K and var(variance) are constant
    """
    i_x, i_y = np.shape(img) # image size
    radi = f//2 # window radius

    # create gaussian kernel
    def gaussian_kernel(f,K,var):
        
        # create coordinate information 
        if f//2 == 0:
            x = np.linspace(-radi,radi,f+1)
            y = np.linspace(-radi,radi,f+1)
            x = np.delete(x, radi)
            y = np.delete(y, radi)
        else:
            x = np.linspace(-radi,radi,f)
            y = np.linspace(-radi,radi,f)

        m_x, m_y = np.meshgrid(x,y) # create coordinate
        r_gauss = m_x**2 + m_y**2  # distance to origin
        gauss = K*(np.exp(-r_gauss/(2*(var**2)))) # create kernel
        return gauss/gauss.sum()
    
    #mirror padding
    def mir_padding(img,f):
        img_p = np.zeros((i_x+2*radi,i_y+2*radi))  #create padding image
        img_p[radi:i_x+radi,radi:i_y+radi] =  img  #throw original image to padding image
        img_p[0:radi,radi:i_y+radi] = img[radi-1::-1,:] # padding top rows
        img_p[-radi::1,radi:i_y+radi] = img[-1:-radi-1:-1,:] # padding bottom rows
        img_p[radi:i_x+radi,0:radi] = img[:,radi-1::-1] # padding left column
        img_p[radi:i_x+radi,-radi::1] = img[:,-1:-radi-1:-1] # padding right column
        for i in range(f):
            img_p[0:radi,i] = img[radi-1-i,radi-1::-1] # padding upper-left corner
            img_p[0:radi,-i] = img[radi-1-i,-radi::1] # padding upper-righ corner
            img_p[-1:-radi-1:-1,i] = img[-radi+i,radi-1::-1] # padding lower-left corner
            img_p[-1:-radi-1:-1,-i] = img[-radi+i,-radi::1] # padding lower-right corner
        return img_p

    img_p = mir_padding(img,f) # create padding image
    g_kernel = gaussian_kernel(f,K,var) # create gaussian kernel

    #seperate kernel
    E = g_kernel[0,0]
    c = g_kernel[:,0]
    wT = np.reshape(g_kernel[0,:]/E,(f,1))

    gauss_image = np.zeros([i_x,i_y]) # create gauss image
    temp_image = np.zeros([i_x,i_y]) # create temp image for two 1D convolution
    old_c_sum = c.sum() # calculate sum of c before modification

    # if elements of kernel are located within area of padding, substitute value with 0
    # calculate new value base on ratio between sum before and after modification
    for j in range(i_y):
        y_bound = i_y - j
        mod_c = c.copy()
        if j < radi:
            mod_c[0:radi-j] = 0  
            new_c_sum = mod_c.sum()
            mod_c = mod_c*old_c_sum/new_c_sum 
        if j > i_y - radi - 1:
            mod_c[-1:-radi+y_bound-1:-1] = 0 
            new_c_sum = mod_c.sum()
            mod_c = mod_c*old_c_sum/new_c_sum  
        for i in range(i_x):
            temp_image[i,j] = np.sum(img_p[i+radi,j:j+f]*mod_c)

    temp_image = mir_padding(temp_image,f) # create padding temp image for next 1D convolution
    old_wT_sum = wT.sum() # calculate sum of wT before modification

    # if elements of kernel are located within area of padding, substitute value with 0
    # calculate new value base on ratio between sum before and after modification
    for i in range(i_x):
        x_bound = i_x - i
        mod_wT = wT.copy()
        if i < radi:
            mod_wT[0:radi-i] = 0   
            new_wT_sum = mod_wT.sum()
            mod_wT = mod_wT*old_wT_sum/new_wT_sum  
        if i > i_x - radi - 1:
            mod_wT[-1:-radi+x_bound-1:-1] = 0  
            new_wT_sum = mod_wT.sum()
            mod_wT = mod_wT*old_wT_sum/new_wT_sum  
        for j in range(i_y):
            gauss_image[i,j] = np.sum(temp_image[i:i+f,j+radi]*mod_wT.T)

    return gauss_image
    
gauss_image = gaussian_filter(s_image,240,1,60) # image using gauss filter
corr_image = s_image/gauss_image # correction image

plt.subplot(221)
plt.title("original image")
plt.xticks([]) #chancel x ticks
plt.yticks([]) #chancel y ticks
plt.imshow(s_image, cmap = 'gray') #indicate color map

plt.subplot(222)
plt.title("image using gaussian filter")
plt.xticks([]) #chancel x ticks
plt.yticks([]) #chancel y ticks
plt.imshow(gauss_image, cmap = 'gray') #indicate color map

plt.subplot(223)
plt.title("correction image")
plt.xticks([]) #chancel x ticks
plt.yticks([]) #chancel y ticks
plt.imshow(corr_image, cmap = 'gray') #indicate color map

plt.show()




