from google.colab.patches import cv2_imshow
import numpy as np
import cv2 
import matplotlib.pyplot as plt

!curl -o prac.jpg https://dainingtest.s3-ap-northeast-1.amazonaws.com/practice+pic2.jpg
image = cv2.imread("prac.jpg")

def rgb2gray(image, bits = 8):
  if type(bits) != int:
    print("bits should be integer")
    return 
  elif bits > 8:
    print("bits should be smaller than 8")
    return 
  elif bits <= 0:
    print("bits should be positive int")
    return 
  else:
    #將影像以numpy讀取灰階值
    imgO = np.copy(image)
    #cv2_imshow 讀取為uint8，可用astype做型態轉換，以利後續計算(如float64)
    imgO = imgO.astype(np.float64,copy=False) #copy=False --> 不產生新陣列

    #將R,G & B轉為256灰階(注意OpenCV讀入為BGR)，使用公式Gray = (R*299 + G*587 + B*114 + 500) / 1000
    #若不想使用除法，可參考http://atlaboratary.blogspot.com/2013/08/rgb-g-rey-l-gray-r0.html，改用2進位
    imgO[:,:,2] = imgO[:,:,2]*114  #(B)
    imgO[:,:,1] = imgO[:,:,1]*587  #(G)
    imgO[:,:,0] = imgO[:,:,0]*299  #(R)
    imgG = (imgO.sum(axis = 2)+500)/1000
    imgG = imgG.astype("uint8",copy=False)
    #不同bits灰階計算
    n = 8 - bits
    if n == 0:
      imgG
    elif 0 < n <= 6:
      imgG = ((imgG//(2**n))+0.5)*(2**n)
    else:
      filL = imgG <= 128
      filU = imgG > 128
      imgG[filL] = 0
      imgG[filU] = 255
    return imgG

imgO = rgb2gray(image, bits = 8)
img = imgO.copy()
ix , iy = np.shape(img) # image size

hr_lst = [np.sum(img == i) for i in range(255)] # histogram
pr_lst = [hr/(ix*iy) for hr in hr_lst] # possibility density of original picture


# calculate grey level after equalization
def s_cal(pr_lst,grey_level,bits=8):
    L = 2**bits
    return (L-1)*sum(pr_lst[:grey_level])

r_lst = [i for i in range(255)] # original grey level
s_lst = [int(round(s_cal(pr_lst,i))) for i in range(255)] # grey level after equaliztion

#substitute grey value
for r,s in zip(r_lst,s_lst):
    img[imgO == r] = s

hs_lst = [np.sum(img == i) for i in range(255)] # normalized histogram after equalization


def upper_limit(hr_lst):
  hrmax = max(hr_lst)
  digit_len = len(str(hrmax))-1
  f12 = hrmax/(10**(digit_len-1))
  if f12 % 10 < 5:
    upper = hrmax//(10**digit_len)*(10**digit_len) + 0.5*(10**(digit_len-1))
    space = upper/10
    return upper,space
  else:
    upper = hrmax//(10**(digit_len-1))*(10**(digit_len-1)) + 0.5*(10**(digit_len-2))
    space = upper/10
    return upper,space

upper,space = upper_limit(hr_lst)

plt.subplot(2,2,1)
plt.title("original picture")
plt.xticks([]) #chancel x ticks
plt.yticks([]) #chancel y ticks
plt.imshow(imgO,cmap="gray") #indicate color map

plt.subplot(2,2,2)
plt.title("equalized picture")
plt.xticks([]) #chancel x ticks
plt.yticks([]) #chancel y ticks
plt.imshow(img,cmap="gray") #indicate color map

ax = plt.subplot(2,2,3)
plt.title("original histogram plot")
plt.xlabel("grey level")
plt.ylabel("total number")
plt.xticks(np.arange(0,288,32))
plt.yticks(np.arange(0,upper+space,space))
plt.xlim(0,256)
plt.ylim(0,upper)
ax.set_aspect(256/upper*1) #adjust width ratio of histogram plot to 1
plt.bar(np.arange(255),hr_lst, facecolor='b', alpha= 1)

ax = plt.subplot(2,2,4)
plt.title("equalized histogram plot")
plt.xlabel("grey level")
plt.ylabel("total number")
plt.xticks(np.arange(0,288,32))
plt.yticks(np.arange(0,upper+space,space))
plt.xlim(0,256)
plt.ylim(0,upper)
ax.set_aspect(256/upper*1) #adjust width ratio of histogram plot to 1
plt.bar(np.arange(255),hs_lst, facecolor='b', alpha= 1)
plt.show()
