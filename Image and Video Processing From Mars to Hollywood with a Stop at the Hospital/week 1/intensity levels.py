from google.colab.patches import cv2_imshow
import numpy as np
import cv2 

!curl -o prac.jpg https://dainingtest.s3-ap-northeast-1.amazonaws.com/practice+pic.jpg
image = cv2.imread("prac.jpg")
#cv2_imshow(image)

def rgb2gray(image, bits = 8):
  #將影像以numpy讀取灰階值
  imgO = np.copy(image)
  #cv2_imshow 讀取為uint8，可用astype做型態轉換，以利後續計算(如float64)
  imgO = imgO.astype(np.float64,copy=False) #copy=False --> 不產生新陣列

  #將R,G & B轉為256灰階(注意OpenCV讀入為BGR)，使用公式Gray = (R*299 + G*587 + B*114 + 500) / 1000
  #若不想使用除法，可參考http://atlaboratary.blogspot.com/2013/08/rgb-g-rey-l-gray-r0.html，改用2進位
  imgO[:,:,2] = imgO[:,:,2]*299  #(B)
  imgO[:,:,1] = imgO[:,:,1]*587  #(G)
  imgO[:,:,0] = imgO[:,:,0]*114  #(R)
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

cv2_imshow(rgb2gray(image,2))
