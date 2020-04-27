# Fast Fouriers Transform  FFT
## 簡介
由離散傅立葉轉換公式可以知道，若現在有 M X N 個訊號，時間複雜度為O(MN^2)，考慮一個常見解析度的影像(如 1024 * 1024 pixel)，
代表需要共 1 兆的加法及乘法，這還不包含指數的運算，實際應用上複雜度太高。1965年J. W. Cooley和J. W. Tukey發表了目前最廣為人
知的FFT演算法，利用分治法(將問題拆分為2的方法)及遞迴的策略，將 N 個DFT拆成 N/2 個子集的DFT如此遞迴下去，FFT算法的複雜度可大
幅縮減為O(MNlog(MN))，考慮同樣 1024 * 1024大小的圖片，運算數大幅降低至 2 千萬。這一種FFT演算法(Radix-2 Decimation in Time)
將序列以 2 的倍數拆分，因此 N 必須為2的冪次，現已有許多其他演算法可符合任意長度的輸入訊號長度，不在本文章討論範圍內。由於二維的傅立葉轉換僅是一維的延伸，對FFT來說亦是如此，以下將利用一維的快速傅立葉轉換作說明。

## 快速傅立葉轉換
考慮一維的DFT，並定義旋轉因子(twiddle factor) W ，其公式如下：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/FFT/pic/1D%20DFT.jpg)<br><br>
仔細觀察可以發現，旋轉因子其實就是在複數平面上切 N 等分，並以順時鐘由 0 度依序旋轉所得，如下所示(以8個點為例)：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/FFT/pic/twiddle%20factor.jpg)<br><br>
有了此一特性，我們可以將上式再改寫如下：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/FFT/pic/DFT%20rewrite.jpg)<br><br>
由上式可以發現，離散傅立葉轉換，可以拆成偶數時點的傅立葉轉換，加上奇數時點的傅立葉轉換乘上旋轉因子。此外，因為 N 個傅立葉轉換被拆成
兩個 N/2 的傅立葉轉換，代表Xeven 和 Xodd的周期也為 N/2 ，又 N/2 對旋轉因子而言為半個週期，多轉了 180 度要加上負號：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/FFT/pic/symmetry.jpg)<br><br>
利用奇偶時點傅立葉轉換的週期性以及旋轉因子的特性，N 個傅立葉轉換可以拆成上下兩半，而且可以利用 N/2 個傅立葉轉換配合旋轉因子一次算出，如下所示：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/FFT/pic/Formula.jpg)<br><br>
現考慮一 8 個點的傅立葉轉換，第一次拆分如下：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/FFT/pic/first%20divide.jpg)<br><br>
對兩個 4 點的傅立葉轉換做第二次拆分如下(僅以上半部說明)：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/FFT/pic/2nd%20divide.jpg)<br><br>
N/4 的 傅立葉轉換架構如下圖所示：<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/FFT/pic/third%20divide.jpg)<br><br>
最終可以下圖表示完整的 8 點快速傅立葉轉換架構，由圖可以發現，每一拆分階段，需要 N 次加法，共需拆分 log(N) 次，所以複雜度為 O(Nlog(N))。<br>
![image](https://github.com/Chang-Chia-Chi/Image-Processing/blob/master/Fourier%20Transform%20in%20Image%20Processing/FFT/pic/Final%20Structure.jpg)<br>

## 參考資料
1. 維基百科 -- 庫利－圖基快速傅立葉變換演算法 https://zh.wikipedia.org/wiki/%E5%BA%93%E5%88%A9%EF%BC%8D%E5%9B%BE%E5%9F%BA%E5%BF%AB%E9%80%9F%E5%82%85%E9%87%8C%E5%8F%B6%E5%8F%98%E6%8D%A2%E7%AE%97%E6%B3%95
2. 從傅立葉轉換到數位訊號處理<br> https://alan23273850.gitbook.io/signals-and-systems/di-wu-zhang-li-san-fu-li-ye-zhuan-huan-dft/di-san-jie-dft-de-jia-su-yun-suan-kuai-su-fu-li-ye-zhuan-huan-fft
3. https://www.researchgate.net/figure/8-point-FFT-twiddle-factor_fig1_325892908
