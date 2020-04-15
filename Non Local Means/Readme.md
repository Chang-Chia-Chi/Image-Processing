# Non Local Means (非區域平均濾波)
## 1. 簡介
空間濾波器(Spatial Filter)主要的功能為降低影像噪音，常見的如Box filter, Gaussian filter等，多屬於<br>
局部平均("Local Means")的演算方法，以捲積(convolution)的概念，利用特定權重的"核"(kernel)，<br>
將影像中像素點的灰階，與鄰近的像素點平均，而達到降低噪音的目的。

Guassian filter 對於周圍像素點接近時的濾波效果非常好，但其近似熱流(heat flow)的性質，在灰階值有明顯<br>
躍遷的區塊，因灰階值"朝周圍擴散"而導致邊緣有模糊(blurring)的狀況，大大降低甚至消除某些細節與紋理，<br>
為了改善區域算法造成的影像模糊，2005年由A. Buades, B. Coll, J.M. Morel等人提出了一種基於全域的權重<br>
平均方法，稱為Non Local Means [1]。

## 2.NLM演算法
非區域局部演算法的定義如下：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Non%20Local%20Means/pic/NLM%20Algorithm.jpg)<br>
其中 u(q) 為影像 u 在像素 q 的灰階值， C(p) 為正規化參數，B(p)表以p為中心的某個區域，d(B(p),B(q))為兩者的<br>
歐基里德距離，實際物理意義為兩區塊像素值的差異，f則為衰減函數，常見為<br><br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Non%20Local%20Means/pic/Decreasing%20Function.jpg)<br><br>
上式的概念可理解成，經過降噪後的值，為整張圖片上所有點的加權平均，其中每個點的權重為 p 附近區塊與<br>
q 附近區塊的相似度，利用向量化概念計算歐基里德距離，再透過指數衰減函數，使得權重落在 [0,1] 的區間，<br>
當圖塊越相似，權重就越高。<br>
相比局部平均法，NLM利用比較全圖像素間的差異取權重平均，利用週期性出現的特徵如背景、紋理及邊緣等進行降躁，<br>
可以較佳的保留圖片細節，但由於對每個點都要搜尋整張圖片計算權重，其運算的複雜度比之局部平均要高上許多。

## 3.NLM實作



## 參考文獻:
1. A. Buades, B. Coll, J.M. Morel, “A non local algorithm for image denoising”, IEEE Computer
Vision and Pattern Recognition 2005, Vol 2, pp: 60-65, 2005.
