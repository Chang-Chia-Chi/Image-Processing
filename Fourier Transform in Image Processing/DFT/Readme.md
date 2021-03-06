# Discrete Fourier Transform DFT

## 簡介
傅立葉轉換被廣泛利用在各種工程問題上，對影像處理也不例外，很多時候空間域無法處理的問題，在頻率域都可迎刃而解，以下將簡述離散形式的傅立葉轉換(DFT)，轉換後圖像的物理意義，以及一些基本的應用。

## 影像的離散傅立葉轉換
現考慮一時間(或空間)中的連續函數 f(x)，x 從正無窮大到負無窮大 ，若以dT的間隔取樣，可表示成連續函數與取樣序列的乘積如下式<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/DFT/pic/4-27.jpg)<br>
對上式做傅立葉轉換，由於捲與乘積在時域、頻域中為互換的運算，因此可表示如下<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/DFT/pic/4-31.jpg)<br>
由上式可以觀察到，取樣函數的傅立葉轉換，等於連續函數做傅立葉轉換後，以取樣頻率為週期無限複製 (連續函數的傅立葉轉換仍為連續函數)，現在我們直接對取樣函數進行傅立葉轉換，表示如下：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/DFT/pic/4-40.jpg)<br>
要注意雖然fn為離散的資料點，上式的結果仍為連續函數，又我們知道取樣函數的傅立葉轉換為連續函數的無限複製，但我們僅需要一個週期的資訊，即可做反傅立葉轉換還原圖面，假設在1/dT的區間內，我們希望取M個sample點，則 μ 可替換成下式，帶入上式整理後可得：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/DFT/pic/4-41.jpg)<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/DFT/pic/4-42.jpg)<br>
此即為一維的傅立葉轉換，其中m可視作頻率 μ ，n則為時間或空間變數 x 。因傅立葉轉換為線性的變換，因此亦可將訊號由頻率域轉換至時間或空間域，離散的反傅立葉轉換如下表示，特別注意因傅立葉轉換 fn 共加總M次，反轉回來時需除上M。<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/DFT/pic/4-43.jpg)<br>
將 m 及 n 以 μ 及 x 替換後得到下式：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/DFT/pic/4-44%2045.jpg)<br>
二維的傅立葉轉換是一維的延伸，其離散形式如下：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/DFT/pic/4-67%2068.jpg)<br>

## 影像於頻率域代表的物理意義與基本應用
傅立葉轉換可在不同觀察域相互轉換的性質，提供了很好的操作性。除了一般常見的濾波、降噪之外，傅立葉轉換在影象編碼、壓縮、數字水印至邊緣提取、影像辨識方面都有重要意義。我們知道無論是實數或虛數，皆可在複數平面以幅值與相角來表示，在影像中，幅值代表影像的強度；而相角則提供影像紋理、細節等編排，多數情況我們只對幅值進行處理，相角則保持不動，以免造成影像細節的混亂。<br><br>
若沒有對輸入影像作預處理，傅立葉轉換的強度資訊(低頻訊號)會在四個角落，對使用上並不方便，因此在傅立葉轉換前，需先對原始圖像先乘上(-1)^x，將強度資訊Shift到影像中心，中心周圍的低頻成分即代表影象的平均強度。<br><br>
頻率對應影象中灰階變化的程度，頻譜圖上看到的明暗不一的亮點，代表空間中灰階梯度的大小。此外我們可以從頻譜圖看出影像的能量分佈，如果整體顏色偏暗，表示實際影像灰階梯度較小，是比較柔和的；反之若整體偏亮，實際影象一定是邊界分明且邊界兩邊強度差異較大，代表影像的細節豐富或著是噪音較高。<br><br>
box、高斯等濾波器有模糊邊緣的效果，對於頻率域來說就是模糊細節，將高頻訊號濾掉，所以稱低通濾波器；而sobel、laplacian等會將邊緣等細節提取出來，對應頻率域就是將低頻的強度資訊濾掉，因此稱做高通濾波器，高通濾波器很常配合Thresholding方法進行邊緣辨識。有些時候需要濾除或加強特定頻率的訊號，則使用帶通或帶阻等指定頻寬的濾波器，通常可以透過高、低通濾波器的線性組合來達成。
