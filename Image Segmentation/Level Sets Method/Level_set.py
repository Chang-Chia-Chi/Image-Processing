import numpy as np
import matplotlib.pyplot as plt
import cv2

def Level_Set(image, v=1, dt=1, iter_n=170, edge_factor = 5, window = (15,15),sigma = 5):
    """
    Level Sets Method with Geodesic Active Contours

    image: src image
    v: factor for ballon (second) term
    dt: time increment
    iter_n: iteration times
    edge_factor: factor of edge_indication function
    window: gaussian_filter kernal size
    sigma: gaussian_filter variance
    """

    def phi_initialize(image):
        """
        Defined default surface phi, phi = -1 is inside of curve and 
        phi = 1 is outside of curve.
        If src image is in color space, it'll transform to gray automatically.
        """
        # convert to gray image if in color space
        if len(np.shape(image))==3:
            image = cv2.cvtColor(image,CV_RGB2GRAY)

        s_x, s_y = np.shape(image) # size of image

        phi = np.ones((s_x, s_y))
        phi[5:-5,5:-5] = -1. # create border of phi

        return phi

    def edge_indicator(image):
        grad_y, grad_x = np.gradient(image)
        return 1./(1.+ edge_factor * (grad_x**2 + grad_y**2))

    def normal_vector(phi):
        grad_y, grad_x = np.gradient(phi)
        norm = np.sqrt(grad_x**2+grad_y**2)
        N_x = grad_x/(norm + 1e-8)
        N_y = grad_y/(norm + 1e-8)
        return N_x, N_y

    def divergence(fx,fy):
        fxy, fxx = np.gradient(fx)
        fyx, fyy = np.gradient(fy)
        return fxx + fyy

    def abs_vector(fx, fy):
        return np.sqrt(fx**2+fy**2)

    def dot(x, y, axis = 0):
        return np.sum( x * y, axis = axis)

    gray_image = cv2.cvtColor(s_image,cv2.COLOR_RGB2GRAY)
    gray_image = gray_image - np.mean(gray_image)
    gauss_image = cv2.GaussianBlur(gray_image,(15,15),5)
    edge_indicator = edge_indicator(gauss_image)

    phi = phi_initialize(gauss_image)
    edgeIndi_grad = np.array(np.gradient(edge_indicator))
    edgeIndi_grad_y, edgeIndi_grad_x = edgeIndi_grad[0], edgeIndi_grad[1]

    for i in range(iter_n):
        phi_grad = np.array(np.gradient(phi))
        phi_grad_y, phi_grad_x = phi_grad[0],phi_grad[1] 
        phi_grad_abs = abs_vector(phi_grad_x, phi_grad_y)
        phi_norm_y, phi_norm_x = normal_vector(phi)
        phi_normal_div = divergence(phi_norm_x, phi_norm_y)
        
        first_term = edge_indicator * phi_grad_abs * phi_normal_div
        second_term = edge_indicator * phi_grad_abs * v
        third_term = dot(phi_grad, edgeIndi_grad)

        phi = phi + dt*(first_term + second_term + third_term)
    return phi

path = "C:/Users/USER/Desktop/Python/Image Processing/Image Segmentation/single.jpg"
s_image = cv2.imread(path) # source image
phi = Level_Set(s_image)

cv2.imshow("edge",phi)
cv2.waitKey(0)