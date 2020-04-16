from google.colab.patches import cv2_imshow
import numpy as np
import cv2 

!curl -o prac.jpg https://dainingtest.s3-ap-northeast-1.amazonaws.com/practice+pic.jpg
image = cv2.imread("prac.jpg")

#以convolution(捲積)的方式進行平均化<https://dotblogs.com.tw/shaynling/2018/12/25/160934>
#mat為原影像矩陣，window為特定的kernel矩陣
def convole_2d(mat, window):
  mati,matj = np.shape(mat) #matrix shape
  wsi,wsj = np.shape(window)  #window shape
  coni = mati + wsi - 1  #捲積後擴展的矩陣列數
  conj = matj + wsj - 1  #捲積後擴展的矩陣欄數
  output = np.zeros((mati,matj))  #產生output矩陣
  expand_mat = np.zeros((coni,conj))  #產生捲積後擴展大小的矩陣
  expand_mat[int(wsi/2):-int((wsi-1)/2),int(wsj/2):-int((wsj-1)/2)] = mat  #將原矩陣的值丟進擴展矩陣

  #以迴圈方式，將捲積的值丟進output矩陣，最後輸出output
  for i in range(mati):
    for j in range(matj):
      output[i,j] = (expand_mat[i:i+wsi,j:j+wsj]*window).sum()
  return output

imgO = np.copy(image)

#平均化(模糊化)矩陣
window = np.ones((10,10))
window /= window.sum()

#將R,G,B三個channel依序捲積
for i in range(3):
  imgO[:,:,i] = convole_2d(imgO[:,:,i], window)

cv2_imshow(imgO)
