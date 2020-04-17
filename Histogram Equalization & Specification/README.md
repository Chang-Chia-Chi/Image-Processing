# Histogram Equalization and Specification

## 1. Histogram Equalization
Histogram eqaulization 是影像處理中一個非常重要的工具，用於影像灰階的均勻化，對於曝光過高或過低，亮度集中(對比低)的影像非常有用。透過這種方法，影像灰階的全局分布變得較為平均，大幅提升局部的對比度，且不改變像素間的明暗關係，影像的細節就更好的被凸顯出來。<br>
Histogram eqaulization 是透過某種轉移函數的鏡射來達成，考慮原影像的灰階 r 及均勻化影像的灰階 s ，兩者之間的關係可以下式表達：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Histogram%20Equalization%20%26%20Specification/pic/8.jpg)<br>
該轉移函數必須符合以下兩種特性：<br>
(a). 為了確保轉移後的影像明暗關係不變，必須是單調上昇(Monotonic Increasing)函數。<br>
(b). 轉換前後的影像總灰階數不變，s=T(r) 與 r 的 bits 數必須相等。<br>
(a) 的最佳情況是 T(r) 為嚴格單調上昇函數，代表 r 與 s 之間能完全互相轉換，但影像處理是離散的世界，通常沒辦法達到嚴格遞增的要求。為了符合以上1. & 2.的條件，文獻中以機率密度函數的方式來處理，考慮已知圖片的灰階機率密度函數 p(r) 和均勻化後的灰階機率函數 p(s) 的關係如下：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Histogram%20Equalization%20%26%20Specification/pic/10.jpg)<br>
轉移函數為：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Histogram%20Equalization%20%26%20Specification/pic/11.jpg)<br>
因為機率密度必定大於或等於 0 ，又積分代表著函數在某區間內圍出的面積，隨著灰階數越高，面積一定越高或相等，所以滿足條件(a)。另外機率密度函數所圍成的總面積為 1 ，因此條件(b)也滿足。接著計算 dr/ds 並帶回第 2 個式子，可以得出 s 的機率密函數度為常數，等於總灰階值的倒數，這也間接證明兩張初始灰階分布不同的圖片，透過 Histogram Equalization 得到的結果相同， p(s) 與 p(r) 無關。當然這是理想性質，不過實際操作上，不同明暗的相片確實可以得到相近的輸出，離散化的公式如下。下圖為實作的結果。<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Histogram%20Equalization%20%26%20Specification/pic/12.jpg)<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Histogram%20Equalization%20%26%20Specification/pic/13.jpg)<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Histogram%20Equalization%20%26%20Specification/pic/15.jpg)<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Histogram%20Equalization%20%26%20Specification/pic/Histogram%20Equalization.jpg)
## 2. Histogram Specification
在某些情況下，均勻化的圖片仍無法觀察到想要的細節，此時可以使用 Histogram specification，顧名思義該方法是"指定"欲轉換的灰階分布 p(z) ，利用 histogram equalization 的結果與輸入圖片灰階分布無關之特性，p(r) 跟 p(z) 理論上經由轉換可得到相同的 p(s)，因此先將 r 及 z 映射到 s 後，藉由 s 與 r 及 z 之間的轉移函數，即可將 r 映射到 z。數學上的計算方式相同不再贅述，程式概念及實作結果如下二圖所示，實作圖左上角為結果與目標圖片的差異(為凸顯不同，有顏色的部分為差異)，左下角為來源圖片 r ，右上角為目標圖面 z ，右下角為利用來源圖片經過 specification 後求得的結果。
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Histogram%20Equalization%20%26%20Specification/pic/programm%20idea.jpg)<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Histogram%20Equalization%20%26%20Specification/pic/Histogram%20specification.jpg)<br>

## 參考文獻
1. Digital Image Processing 4th edition, Rafael C. Gonzalez, Richard E. Woods

