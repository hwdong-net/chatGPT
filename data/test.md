
为了更好地看清楚如何求$L(\pmb w)$关于$\pmb w  =(w_0,w_1,\cdots, w_K)^T$的偏导数，引入一些辅助记号$z^{(i)},f^{(i)}$：

$$z^{(i)} = \pmb w \odot \pmb x^{(i)}= w_1 * x_1^{(i)}+w_2*x_2^{(i)}+...+w_K*x_K^{(i)} $$

$$z^{(i)} = \pmb w \odot \pmb x^{(i)}= w_1 * x_1^{(i)}+w_2*x_2^{(i)} +...+w_K*x_K^{(i)}+w_0*x_0^{(i)}$$

$$f^{(i)} =\sigma(z^{(i)})$$

$$\mathcal L^{(i)} = -\bigl(y^i log(f^{(i)}) +(1-y^i) log(1-f^{(i)})\bigr)$$

$$\mathcal L(\pmb w) = \frac{1}{m}\sum_{i=1}^{m}{\mathcal L^{(i)}}$$ 

$\mathcal L(\pmb w)$可以看成m个${\mathcal L^{(i)}}$的和，而$\mathcal L^{(i)}$又是$f^{(i)}$的函数，$f^{(i)}$又是$z^{(i)}$的函数，$z^{(i)}$又是$\pmb w = (w_1,w_2, \cdots,w_k)^T$的函数，根据求导的四则运算法则（如和函数的导数每个函数的导数之和）和复合函数的链式求导法则：

$$\frac{\partial{\mathcal L(\pmb {w})}}{\partial{\mathcal L^{(i)}}} = \frac{1}{m}$$ 

$$\frac{\partial{\mathcal L^{(i)} }}{\partial{f^{(i)}}} = -\bigl( \frac{y^i}{f^{(i)}}- \frac{(1-y^i)}{(1-f^{(i)})} \bigr )= \frac{f^{(i)}-y^i}{f^{(i)}(1-f^{(i)})}$$

$$\frac{\partial{f^{(i)}}}{\partial{z^{(i)}}} = \sigma(z^{(i)})(1-\sigma(z^{(i)})) = f^{(i)}(1-f^{(i)})$$


$$\frac{\partial{z^{(i)}}}{\partial{w_j}} = x_j^{(i)}$$

因此有：

$$\begin{aligned}
\frac{\partial{L(\pmb {w})}}{\partial{w_j}} &= \sum_{i=1}^{m}{\frac{\partial{L(\pmb{w})}}{\partial{\mathcal L^{(i)}}} \times \frac{\partial{\mathcal L^{(i)} }}{\partial{f^{(i)}}} \times  \frac{\partial{f^{(i)}}}{\partial{z^{(i)}}} \times \frac{\partial{{z}^{(i)}}}{\partial{w_j}} }\\ &= \frac{1}{m}\sum_{i=1}^{m}{ \frac{f^{(i)}-y^i}{f^{(i)}(1-f^{(i)})} \times  f^{(i)}(1-f^{(i)})  \times x_j^{(i)} } \\
&=\frac{1}{m}\sum_{i=1}^{m}{ (f^{(i)} - {y}^{(i)}) x_j^{(i)} }\\
&=\frac{1}{m}\sum_{1=1}^{m}(f_{\pmb w}({\pmb x}^{(i)})-y^{(i)})x_j^{(i)}\\
&=\frac{1}{m}\sum_{1=1}^{m}x_j^{(i)}(f_{\pmb w}({\pmb x}^{(i)})-y^{(i)})
\end{aligned} \tag{3-35}$$

因为$f_{\pmb w}({\pmb x}^{(i)})-y^{(i)}$是一个数值，所以它和向量的数乘是可以交换次序的，即$(f_{\pmb w}({\pmb x}^{(i)})-y^{(i)})x_j^{(i)} = x_j^{(i)}(f_{\pmb w}({\pmb x}^{(i)})-y^{(i)})$。


可以观察到对于一个样本($\pmb x,y$)，$L(\pmb w)$关于累加和$z=\pmb x \pmb w$的梯度（导数）$\frac{\partial \mathcal L}{\partial z}$是：$f-y$。这和线性回归的方差 $\frac{1}{2}{(f-y)}^2$关于$f$的梯度（导数）形式是一样的。 使得逻辑回归和线性回归的梯度的计算公式是一样的。

如果将${\pmb x}^i$写成行向量形式，所有${\pmb x}^i$可以按行构成一个矩阵$\pmb X$，所有样本的目标值和预测值${y}^i,{f}^i$可写成对应的列向量形式：
