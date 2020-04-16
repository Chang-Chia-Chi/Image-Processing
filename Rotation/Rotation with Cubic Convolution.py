from google.colab.patches import cv2_imshow
import numpy as np
import cv2 
import math

!curl -o prac.jpg https://dainingtest.s3-ap-northeast-1.amazonaws.com/practice+pic2.jpg
image = cv2.imread("prac.jpg")

#padding of original image
def pad_cubic(mat):
  mati , matj = np.shape(mat[:,:,0])
  mat_p = np.zeros((mati+4,matj+4,3))  #創建擴張矩陣
  for i in range(3):
    mat_p[2:mati+2,2:matj+2,i] = mat[:,:,i]  #將原矩陣值丟入擴張矩陣
    mat_p[0:2,2:matj+2,i] = mat[0:2,:,i]   #上方擴張列賦值
    mat_p[-1:-3,2:matj+2,i] = mat[-1:-3,:,i]  #下方擴張列賦值
    mat_p[2:mati+2,0:2,i] = mat[:,0:2,i]  #左方擴張欄賦值
    mat_p[2:mati+2,-1:-3,i] = mat[:,-1:-3,i]  #右方擴張欄賦值
    mat_p[0:2,0:2,i] = mat[0,0,i]  #左上角賦值
    mat_p[-1:-3,0:2,i] = mat[-1,0,i] #左下角賦值
    mat_p[0:2,-1:-3,i] = mat[0,-1,i] #右上角賦值
    mat_p[-1:-3,-1:-3,i] = mat[-1,-1,i] #右下角賦值
  return mat_p

#cubic kernal cal.
def bck(x,a):
  if abs(x)<=1:
    return (a+2)*abs(x**3)-(a+3)*abs(x**2)+1
  elif  1<abs(x)<2:
    return a*abs(x**3)-5*a*abs(x**2)+8*a*abs(x)-4*a
  else:
    return 0

#Bicubic convolution algorithm(a is kernal factor)
#ref.: https://github.com/rootpine/Bicubic-interpolation#Requirement
def Bicubic_convol(mat,x,y, a = 0.5):
  """
  雙三次內插函式
  """
  gx = 0
  fxs = np.zeros((4,4))
  x1 = x+1-np.floor(x)  #距上方一格的x距離
  x2 = x - np.floor(x)  #距自己最近格點的x距離
  x3 = np.floor(x) + 1 - x  #距下方一格的x距離
  x4 = np.floor(x) + 2 - x  #距下方二格的x距離

  y1 = y+1-np.floor(y) #距左方一格的y距離
  y2 = y - np.floor(y) #距自己最近格點的y距離
  y3 = np.floor(y) + 1 - y #距右方一格的y距離
  y4 = np.floor(y) + 2 - y #距右方二格的y距離  

  #kernel array
  ux = np.asarray([bck(x1,a),bck(x2,a),bck(x3,a),bck(x4,a)])
  uy = np.asarray([bck(y1,a),bck(y2,a),bck(y3,a),bck(y4,a)])

  #fx's array，int將浮點數轉為整數
  fxs = np.asarray([[mat[int(x-x1),int(y-y1)],mat[int(x-x1),int(y-y2)],mat[int(x-x1),int(y+y3)],mat[int(x-x1),int(y+y4)]],
                    [mat[int(x-x2),int(y-y1)],mat[int(x-x2),int(y-y2)],mat[int(x-x2),int(y+y3)],mat[int(x-x2),int(y+y4)]],
                    [mat[int(x+x3),int(y-y1)],mat[int(x+x3),int(y-y2)],mat[int(x+x3),int(y+y3)],mat[int(x+x3),int(y+y4)]],
                    [mat[int(x+x4),int(y-y1)],mat[int(x+x4),int(y-y2)],mat[int(x+x4),int(y+y3)],mat[int(x+x4),int(y+y4)]]])
  
  gx = np.dot(np.dot(ux,fxs),uy).astype("uint8")
  return gx

#ref.: http://eeweb.poly.edu/~yao/EL5123/lecture12_ImageWarping.pdf
def back_revol(x,y,angle,ox,oy):
  """
  Rotate of coordinates x and y by angle about (ox, oy).
  對非原點旋轉的概念為，先將圖形移到旋轉中心，對圓心旋轉，再位移一個偏心量
  """
  s = math.sin(angle/360*2*math.pi)
  c = math.cos(angle/360*2*math.pi)
  x = x - ox 
  y = y - oy
  return x * c + y * s + ox, -x * s + y * c + oy

angle = 45 #定義旋轉角度
ox = 0 #定義旋轉中心
oy = 0 #定義旋轉中心
srci, srcj = np.shape(image[:,:,0]) #原圖片尺寸
corx = [0,srci,srci,0]
cory = [0,0,srcj,srcj]
cor_newx=[]
cor_newy=[]

#計算新圖片四個角落尺寸(注意是source --> dst，所以角度要帶負號)
for x,y in zip(corx,cory):
  newx , newy = back_revol(x,y,-angle, ox, oy)
  cor_newx.append(newx)
  cor_newy.append(newy)

#產生新圖片
newi = int(max(cor_newx) - min(cor_newx))+1   #新圖片尺寸
newj = int(max(cor_newy) - min(cor_newy))+1
new_img = np.zeros((newi,newj,3)) 

#pad原圖，供之後雙三次內插用
pad_img = pad_cubic(image) 

#若ix,iy(dst-->source)落在pad_image範圍內，則使用雙三次內插，將值賦予新圖片
for k in range(3):
  for j in range(newj):
    for i in range(newi):
      ix,iy = back_revol(i+min(cor_newx),j+min(cor_newy),angle,ox,oy) #backfoward mapping
      if (0<=ix) & (ix<srci) & (0<=iy) & (iy<srci):
        new_img[i,j,k] = Bicubic_convol(pad_img[:,:,k],ix,iy)

cv2_imshow(new_img)
