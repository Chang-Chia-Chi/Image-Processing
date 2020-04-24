import numpy as np

def gaussian_filter(img,f=5,K=1,var=1):
    """
    Gaussian Spatial Filter
    img is image to be applied
    f is window size (fXf)
    K and var(variance) are constant
    """
    i_x, i_y = np.shape(img[:,:,0]) # image size
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
        gauss /= gauss.sum()
        gauss_3d = np.repeat(gauss[:,:,np.newaxis],3,axis = 2)
        return gauss_3d
    
    #mirror padding
    def mir_padding(img,f):
        img_p = np.zeros((i_x+2*radi,i_y+2*radi,3))  #create padding image
        img_p[radi:i_x+radi,radi:i_y+radi,:] = img  #throw original image to padding image
        img_p[0:radi,radi:i_y+radi,:] = img[radi-1::-1,:,:] # padding upper rows
        img_p[-radi::1,radi:i_y+radi,:] = img[-1:-radi-1:-1,:,:] # padding bottom rows
        img_p[radi:i_x+radi,0:radi,:] = img[:,radi-1::-1,:] # padding left column
        img_p[radi:i_x+radi,-radi::1,:] = img[:,-1:-radi-1:-1,:] # padding right column
        for i in range(f):
            img_p[0:radi,i,:] = img[radi-1-i,radi-1::-1,:] # padding upper-left corner
            img_p[0:radi,-i,:] = img[radi-1-i,-radi::1,:] # padding upper-righ corner
            img_p[-1:-radi-1:-1,i,:] = img[-radi+i,radi-1::-1,:] # padding lower-left corner
            img_p[-1:-radi-1:-1,-i,:] = img[-radi+i,-radi::1,:] # padding lower-right corner
        return img_p

    img_p = mir_padding(img,f) # create padding image
    g_kernel = gaussian_kernel(f,K,var) # create gaussian kernel

    #seperate kernel
    E = g_kernel[0,0,0]
    c = g_kernel[:,0,:]
    wT = np.reshape(g_kernel[0,:,:]/E,(f,3))

    gauss_image = np.zeros([i_x,i_y,3]) # create gauss image
    temp_image = np.zeros([i_x,i_y,3]) # create temp image for two 1D convolution
    old_c_sum = c.sum(axis = 0) # calculate sum of c before modification

    # if elements of kernel are located within area of padding, substitute value with 0
    # calculate new value base on ratio between sum before and after modification
    for j in range(i_y):
        y_bound = i_y - j
        mod_c = c.copy()
        if j < radi:
            mod_c[0:radi-j,:] = 0  
            new_c_sum = mod_c.sum(axis= 0)
            mod_c = mod_c*old_c_sum/new_c_sum 
        if j > i_y - radi - 1:
            mod_c[-1:-radi+y_bound-1:-1,:] = 0 
            new_c_sum = mod_c.sum(axis= 0)
            mod_c = mod_c*old_c_sum/new_c_sum  
        for i in range(i_x):
            temp_image[i,j,:] = np.sum(img_p[i+radi,j:j+f,:]*mod_c,axis= 0)

    temp_image = mir_padding(temp_image,f) # create padding temp image for next 1D convolution
    old_wT_sum = wT.sum(axis = 0) # calculate sum of wT before modification

    # if elements of kernel are located within area of padding, substitute value with 0
    # calculate new value base on ratio between sum before and after modification
    for i in range(i_x):
        x_bound = i_x - i
        mod_wT = wT.copy()
        if i < radi:
            mod_wT[0:radi-i,:] = 0   
            new_wT_sum = mod_wT.sum(axis = 0)
            mod_wT = mod_wT*old_wT_sum/new_wT_sum  
        if i > i_x - radi - 1:
            mod_wT[-1:-radi+x_bound-1:-1,:] = 0  
            new_wT_sum = mod_wT.sum(axis = 0)
            mod_wT = mod_wT*old_wT_sum/new_wT_sum  
        for j in range(i_y):
            gauss_image[i,j,:] = np.sum(temp_image[i:i+f,j+radi,:]*mod_wT,axis = 0)
    return gauss_image