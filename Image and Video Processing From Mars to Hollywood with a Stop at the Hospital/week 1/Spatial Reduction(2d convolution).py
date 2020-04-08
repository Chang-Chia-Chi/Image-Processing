from google.colab.patches import cv2_imshow
import numpy as np
import cv2 

!curl -o prac.jpg https://dainingtest.s3-ap-northeast-1.amazonaws.com/practice+pic2.jpg
image = cv2.imread("prac.jpg")

def convole_2d(mat, window):
  mati,matj = np.shape(mat) #matrix shape
  wsi,wsj = np.shape(window)  #window shape
  output = np.zeros((mati,matj))  #產生output矩陣

  #以迴圈方式，將捲積的值丟進output矩陣，最後輸出output(每n為一單位)
  for i in range(0,(mati//wsi)*wsi,wsi):
    for j in range(0,(matj//wsj)*wsj,wsj):
      output[i:i+wsi,j:j+wsj] = (mat[i:i+wsi,j:j+wsj]*window).sum()
  return output

imgO = np.copy(image)

#模糊化矩陣
n = 15
window = np.ones((n,n))
window /= window.sum()

#將R,G,B三個channel依序捲積
for i in range(3):
  imgO[:,:,i] = convole_2d(imgO[:,:,i], window)

cv2_imshow(imgO)
