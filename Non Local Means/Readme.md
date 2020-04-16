# Non Local Means (非區域平均濾波)
## 1. 簡介
空間濾波器(Spatial Filter)主要的功能為降低影像噪音，常見的如Box filter, Gaussian filter等，多屬於<br>
局部平均("Local Means")的演算方法，以捲積(convolution)的概念，利用特定權重的"核"(kernel)，<br>
將影像中像素點的灰階，與鄰近的像素點平均，而達到降低噪音的目的。

Guassian filter 對點周圍像素值接近時的濾波效果非常好，但其近似熱流(heat flow)的性質，在灰階值有明顯<br>
躍遷的區塊，因灰階值"朝周圍擴散"而導致邊緣發生模糊(blurring)的狀況，大大降低甚至消除某些細節與紋理，<br>
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
當圖塊越相似，權重就越高。<br><br>
相比局部平均法，NLM利用比較全圖像素間的差異取權重平均，利用週期性出現的特徵如背景、紋理及邊緣等<br>
進行降躁，可以較佳的保留圖片細節，但由於對每個點都要搜尋整張圖片計算權重，其運算的複雜度比之局部<br>
平均要高上許多。

## 3.NLM 像素級實作(Pixelwise Implementation)
現考慮一彩色圖片 u = (u1,u2,u3)，圖片上 p 點降躁後的值可寫為<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Non%20Local%20Means/pic/Pixel%20wise.jpg)<br>
其中 i = 1,2,3 (RGB三通道)， w(p,q) 為權重， d^2 為歐基里德距離， B(p,f)表以 p 為中心寬度為 2f+1 的正方形，<br>
區域即 [px-f,px+f]X[py-f,py+f]區間。<br><br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Non%20Local%20Means/pic/Distance.jpg)<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Non%20Local%20Means/pic/Weight.jpg)<br><br>
上式 σ 為噪音的標準差， h 為衰減函式參數，皆是濾波器的相關參數。可以解釋為當圖塊近似程度較高時 (d<=2σ) ，<br>
權重為1； (d>2σ) 當近似程度較低時，權重以指數函式快速的衰減。 h 則是權重計算平坦程度的參數， h 值越小，<br>
代表衰減速度越快，相似程度低的區塊權重將更快遞減至0。

## 4.NLM 區塊級實作(Patchwise Implementation)
像素級實作需對整張影像進行搜索，考慮影像大小為 N X N，實作上複雜度為 N^4 ，隨影像解析度的提高，<br>
運行時間將大幅拉長。下圖 (256 X 256) 為以像素級實作的案例，降躁的效果非常顯著，然運算複雜度實在太<br>
高，即便計算了一個晚上(colab環境約 8 小時)也只完成一半，效率上難以使用。<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Non%20Local%20Means/pic/pixel%20base.jpg)<br>
為了降低NLM的計算需求，該論文[1]同時提出了區塊級實作的概念，如下表示<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Non%20Local%20Means/pic/patch%20wise.jpg)<br>
權重 w 的算法與前節相同， B(p,r) 則以半徑r限制了搜索區域，最後將 Bm(i,f)的值以下式平均後，即可<br>
求得降躁後的圖像<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Non%20Local%20Means/pic/patcj%20wise%20result.jpg)<br>
若影像大小為 M X M，搜尋視窗為 21X21 ，區塊大小為 7X7 ，整個算法的複雜度為 49 X 441 X M^2，<br>
大幅降低所需運算時間，另外因為最後總和平均的步驟，區塊級有較高的峰值信躁比 PSNR ，邊緣的噪音<br>
震盪也跟著下降，但在細節保存上，兩種算法無明顯的優劣。<br>

區塊級實作的結果可參考下圖，colab環境執行約270s，效率大大提升，且濾波效果良好
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Non%20Local%20Means/pic/patch%20base.jpg)
## 參考文獻:
1. A. Buades, B. Coll, J.M. Morel, “A non local algorithm for image denoising”, IEEE Computer
Vision and Pattern Recognition 2005, Vol 2, pp: 60-65, 2005.
2. Wikipedia, https://en.wikipedia.org/wiki/Non-local_means
