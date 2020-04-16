# Rotation of Image (影像旋轉)
## 1. 簡介
旋轉是影像幾何變換中常見的應用，概念上非常簡單，將原影像(source)上每個像素點 (x,y)，以旋轉矩陣計算旋轉後在<br>
新圖片(destination)上的位置，將所有像素點掃過一遍後，即可得到旋轉後的影像。旋轉矩陣表示如下[1]<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Rotation/pic/Rotation%20Matrix.jpg)<br>

## 2. Forward Mapping
以來源圖片經由轉換取得目標圖片的方法，稱為 forward mapping ，概念及數學式表示如下[2][3]<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Rotation/pic/forwad%20mapping.jpg)<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Rotation/pic/concept%20of%20forwad%20mapping.jpg)<br>

forward mapping算法直觀易懂，非常容易使用，但一般卻不會直接套用，原因如下：<br><br>
1. 有可能不同的來源像素點 mapping 到相同的目標像素點位置，如何計算灰階值是個問題。<br>
2. 有可能某些目標像素點根本沒有被 mapping到。<br>

## 3. Inverse Mapping
基於以上理由，實作上大多使用 inverse mapping 方法，概念與forward mapping類似，但變成以目標像素點，計算來源像素點<br>
的位置。若計算結果超出來源圖範圍，則以 0 、 255 或任何你想要的值帶入；若結果落入原圖範圍，則利用內插來源像素點的灰階，<br>
求出目標像素點的灰階值。
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Rotation/pic/concept%20of%20inverse%20mapping.jpg)<br>

inverse mapping的計算步驟如下:<br>
1. 以 forward mapping 計算圖片旋轉後的尺寸，並以該尺寸創建空矩陣。
2. 以 inverse mapping 計算每個目標像素點對應的來源像素點。這邊有一個重點，因旋轉矩陣是對"原點"旋轉，若沒有調<br>
整目標圖片座標，得到的結果將有部分超出影像範圍，所以在計算 inverse mapping 時，需位移至目標圖片的原點再做旋轉<br>
可參考下圖。<br>
3. 若 inverse mapping 的座標點坐落於原圖尺寸外，目標像素點代入你所希望的灰階值；；若結果落入原圖範圍，則利用<br>
特定的內插方法，計算目標像素點的灰階。<br>
4. 輸出旋轉後影像<br>

![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Rotation/pic/rotate%20about%20old%20original.jpg)


## 參考文獻
1. wekipedia:https://zh.wikipedia.org/wiki/%E6%97%8B%E8%BD%AC%E7%9F%A9%E9%98%B5
2. https://www.cs.auckland.ac.nz/courses/compsci773s1c/lectures/ImageProcessing-html/topic2.htm
3. https://blogs.mathworks.com/steve/2006/04/28/spatial-transforms-forward-mapping/
4. https://blogs.mathworks.com/steve/2006/05/05/spatial-transformations-inverse-mapping/
