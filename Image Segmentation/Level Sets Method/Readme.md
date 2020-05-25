# Level sets with Geodesic Active Contours
## 實作結果
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/single.gif)<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/shapes.gif)<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/single_phi.jpg)<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/multi_phi.jpg)<br>
## 1. Basic properties of curve (曲線基本性質)
在講水平集方法之前，必須先談談曲線的基本性質，假設現有一函式：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/1.jpg)<br>
來表達平面中的某一曲線，我們以圓為例子，則上式可寫為：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/2.jpg)<br>
是否覺得表達起來不夠簡潔 ? 為了更容易理解及清楚的表達曲線，我們將曲線僅以單個變數表達，而該變數亦為平面中座標的變數，如下所示：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/3.jpg)<br>
若還不太理解，我們再以圓當例子：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/4.jpg)<br>
如此一來是不是非常整潔且清楚?<br>

我們知道若要求得曲線某點的切線，必須做一次微分：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/5.jpg)<br>
一個向量的大小，等於該向量對自身的內積：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/6.jpg)<br>
若對上式做偏微分：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/7.jpg)<br>
由上式我們發現一個有趣的性質，曲線的一次微分與二次微分的內積為0 ! 若一次微分為切線，這不就代表二次微分為法線向量嗎。因此一個曲線的法線向量，可以利用下式表達：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/8.jpg)<br>
κ為曲率，n為單位法向量。有了以上的基本知識，接著我們可以進入曲線演變的PDE表達方法。<br>

## 2. Curve Evolution (曲線演化)
將曲線對時間做微分，代表曲線隨時間的變化，也就是速度。若我們使曲線對時間的微分與曲線對空間的二次微分搭上關係，那問題就變成我們熟悉的熱擴散方程式(heat equation)：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/9.jpg)<br>
另外對於曲線演化，一般來說只考慮法線方向的變化(切線方向可以想像成點沿著曲線移動，對形狀沒有影響)，常見的方程如下所示：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/10.jpg)<br>
那曲線演化跟影像分割的關係在哪 ? 其實我們可以想像，影像分割就是要找到包圍目標的特定曲線。若設定初始曲線，並讓曲線逐漸擴張或縮小，當曲線最終停在目標的邊緣時，即完成影像分割。<br>
然由於熱傳微分方程的特性，以上的曲線演化會無限擴張或縮小，這並非我們所希望的性質，因此必須考慮額外的"力量"，進一步限制曲線在邊緣附近的速度。<br>

## 3. Geodesic Active Contours
為了大幅降低曲線演化在邊緣附近的速度，我們引入一個外力項 g(x,y)。此外，再引入外力的梯度，進一步加強對邊緣的敏感度：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/11.jpg)<br>
回想影像分割的目標，即找到特定的圖像邊緣，也就是說，曲線的演化必須停在影像中高梯度的位置，依照此概念， g(x,y) 可以寫成與梯度倒數相關的函式 g(x,y)≅1/∇Image，使 g(x,y)κ 在邊緣趨近於0，考慮邊緣偵測方程式：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/12.jpg)<br>
其中 G_a*I 為利用高斯(或其他)低通濾波器降噪後的影像，下面利用圖像的表達使整個概念更為清楚[2]：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/13.jpg)<br>

## 4. Level Sets Method (水平集方法)
講完曲線演化方程的基本概念，終於可以進入本篇文章的主題：水平集方法。
在談水平集方法前，先想想如何利用上一小節提供的式子進行影像分割 ? 
最直覺的想法是，給定一個包覆目標物的任意初始封閉曲線，"顯式"地追蹤影像邊緣，當曲線停止收縮時，曲線圍成的形狀即為帶分割物。但這樣的做法有一些不可避免的問題存在：<br>
(1)	當曲線持續變化，曲線上某些區段的長度勢必會改變，造成得以更少或更多的點來表達，在迭代過程中需考慮內、外插問題。<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/14.jpg)<br>
(2)	曲線的拓樸結構可能改變，尤其當曲線合併時，兩個點的重合難以表達。<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/15.jpg)<br>
(3)	當某段曲線的曲率很大，且逐漸收縮時，圓弧可能會崩塌變成尖點，曲率為無窮大，且點的運動難以描述。<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/16.jpg)<br>
<br>
Level Sets Method，由字面來看，其實這是一種集合的概念，我們先簡化問題，考慮一拋物線：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/17.jpg)<br>
若寫成集合的形式：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/18.jpg)<br>
若我們在 y=1 畫上一條線，那此時集合C為{-1, 1}，也就是在 level = 1所有符合該平面曲線的點 x。<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/19.jpg)<br>
同樣的概念，可以延伸到三維的曲面，考慮曲面與level 0平面所圍成的曲線，其通式為：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/20.jpg)<br>
也就是說，現在我們的目標為求出平面上的座標點，使得 ϕ(x,y)=0 ，所有符合的點集合，即為影像分割的目標 !<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/21.jpg)<br>
因為曲線的演進一定朝向法線方向，為了求出法向量，我們對 ϕ(x,y)=0 進行空間微分：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/22.jpg)<br>
由上式可以發現，∇ϕ與切向量的內積為0，代表∇ϕ的物理意義即為某點影像的法向量，將之正規化並取負號確保一定指向曲線內部，則可表示為：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/23.jpg)<br>
曲線隨時間的變化即為速度，水平集的PDE可寫成：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/27.jpg)<br>
然到目前為止，我們一直在連續空間中，對曲線進行處理，但實際的影像是離散空間，為了更容易以離散形式表達，我們對上式進行處理：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/24.jpg)<br>
上式的物理意義為，空間中的曲面將持續擴張，每一時刻與level 0相交所圍成的曲線，即為該時刻下的水平集；當曲面無法再擴張時，當下的水平集即為目標影像。
將Geodesic 的方程代入，可以求得 [1]：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/25.jpg)<br>
上式為Level sets with Geodesic Active Contours的離散表達式。最後我們以中央差分法將 ∂ϕ/∂t 離散化：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Image%20Segmentation/Level%20Sets%20Method/pic/26.jpg)<br>
藉由水平集方法，我們不再需要顯式地追蹤曲線，而是建立平面，隱式地等待曲面擴張，避免一般active contour可能產生的問題。

## 參考文獻:
1.Level Set Method Part II: Image Segmentationhttps://wiseodd.github.io/techblog/2016/11/20/levelset-segmentation/<br>
2.https://www.youtube.com/watch?v=jrA-r4BOn0c<br>
## 圖片來源:
1. https://mathematica.stackexchange.com/questions/94802/how-to-imageidentify-multiple-objects-in-a-single-image<br>
2. https://www.dhgate.com/product/belt-men-hand-made-top-cowhide-genuine-leather/441152373.html#seo=WAP<br>


