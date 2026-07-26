# LA212final（Obsidian 精校版）

_Source: LA212final.pdf_

## 第 1 页：试题

北京大学工学院课程试卷

课程名称：高等代数

2021-2022 学年第（2）学期期末。本试卷共 3 道大题，满分 100 分。

（考试结束后请将试卷、答题本一起交给监考老师）

以下各题中，数域均为 $\mathbb{R}$。

### 1.（15 分）

用最小二乘法近似求解方程组

$$
\begin{cases}
x_1+2x_2=6,\\
2x_1+3x_2=6,\\
3x_1+4x_2=8.
\end{cases}
$$

### 2.（20 分）

若 $n$ 阶对称方阵 $A,B$ 满足

$$
B=LAL^T,
$$

其中 $L$ 为对角元素均为 $1$ 的下三角矩阵。证明：

a) $A$ 与 $B$ 的 $r$ 阶顺序主子式相等，$1\le r\le n$；

b) 若 $A$ 的各阶顺序主子式均非 $0$，则必存在对角元素均为 $1$ 的下三角矩阵 $L$，使得

$$
B=LAL^T
$$

为对角阵。

### 3.（65 分）

在线性空间 $V=P_2[x]$ 上，选定一组基

$$
e_1=1,\qquad e_2=x,\qquad e_3=x^2,
$$

定义

$$
(f,g)=\int_0^1 f(x)g(x)\,dx.
$$

a)（10 分）证明 $(\cdot,\cdot)$ 定义了 $V$ 上的内积；

b)（10 分）求 $(e_1,e_2,e_3)$ 下的度量阵；

c)（10 分）由 $(e_1,e_2,e_3)$ 出发，通过 Gram-Schmidt 正交化求出一组单位正交基 $(\varepsilon_1,\varepsilon_2,\varepsilon_3)$，写出这组基下的度量阵；

d)（15 分）对任意

$$
f(x)=f_0+f_1x+f_2x^2\in V,
$$

定义

$$
I(f)=f_0+f_1+f_2.
$$

证明 $I(\cdot)$ 为线性泛函；求出 Riesz 表示定理中满足

$$
I(f)=(f,h),\qquad \forall f\in V
$$

的 $h\in V$；求 $(e_1,e_2,e_3)$ 的一组对偶基；

e)（10 分）对任意

$$
f(x)=f_0+f_1x+f_2x^2\in V,
$$

定义

$$
\mathcal A f=f'(x)=f_1+2f_2x.
$$

求其共轭算子 $\mathcal A^*$，即满足

$$
(\mathcal A f,g)=(f,\mathcal A^*g),\qquad \forall f,g\in V
$$

的算子；

f)（10 分）对任意

$$
f(x)=f_0+f_1x+f_2x^2,\qquad g(x)=g_0+g_1x+g_2x^2\in V,
$$

定义

$$
II(f,g)=f_0g_0+f_1g_1+f_2g_2.
$$

证明 $II(\cdot,\cdot)$ 为对称双线性型；求该双线性型在 $(\varepsilon_1,\varepsilon_2,\varepsilon_3)$ 下的系数方阵，并求该方阵的相合标准形。

---

## 第 2 页：参考解答

### 1. 解

原方程组为

$$
\begin{bmatrix}
1&2\\
2&3\\
3&4
\end{bmatrix}
\begin{bmatrix}
x_1\\
x_2
\end{bmatrix}
=
\begin{bmatrix}
6\\
6\\
8
\end{bmatrix}.
$$

最小二乘法给出正规方程

$$
\begin{bmatrix}
1&2&3\\
2&3&4
\end{bmatrix}
\begin{bmatrix}
1&2\\
2&3\\
3&4
\end{bmatrix}
\begin{bmatrix}
x_1\\
x_2
\end{bmatrix}
=
\begin{bmatrix}
1&2&3\\
2&3&4
\end{bmatrix}
\begin{bmatrix}
6\\
6\\
8
\end{bmatrix}.
$$

即

$$
\begin{bmatrix}
14&20\\
20&29
\end{bmatrix}
\begin{bmatrix}
x_1\\
x_2
\end{bmatrix}
=
\begin{bmatrix}
42\\
62
\end{bmatrix}.
$$

解得

$$
\begin{bmatrix}
x_1\\
x_2
\end{bmatrix}
=
\begin{bmatrix}
-\dfrac{11}{3}\\[4pt]
\dfrac{14}{3}
\end{bmatrix}.
$$

### 2. 证明

#### a)

对 $L,A,B$ 作分块：

$$
\begin{bmatrix}
L_{11}&O\\
L_{12}&L_{22}
\end{bmatrix}
\begin{bmatrix}
A_{11}&A_{12}\\
A_{12}^T&A_{22}
\end{bmatrix}
\begin{bmatrix}
L_{11}^T&L_{12}^T\\
O&L_{22}^T
\end{bmatrix}
=
\begin{bmatrix}
B_{11}&B_{12}\\
B_{12}^T&B_{22}
\end{bmatrix}.
$$

于是其左上角方块给出

$$
L_{11}A_{11}L_{11}^T=B_{11}.
$$

这里 $L_{11}$ 为对角元素均为 $1$ 的 $r$ 阶下三角矩阵，故

$$
\det L_{11}=1.
$$

由行列式性质知

$$
|B_{11}|=\det(L_{11}A_{11}L_{11}^T)=|A_{11}|.
$$

即 $A,B$ 的任意 $r$ 阶顺序主子式相等。

#### b)

对 $A$ 的阶数 $n$ 作归纳。$n=1$ 时显然成立。设 $n=p$ 时成立，考虑 $p+1$ 阶对称阵

$$
A=
\begin{bmatrix}
A_1&\alpha^T\\
\alpha&a_2
\end{bmatrix}.
$$

其各阶顺序主子式非 $0$。于是其中 $p$ 阶对称方阵 $A_1$ 的各阶顺序主子式非 $0$。由归纳假设，存在对角元均为 $1$ 的下三角矩阵 $L_1$，使得 $L_1A_1L_1^T$ 为对角阵。特别地，$A_1$ 非奇异。

取

$$
\ell_1=-\alpha A_1^{-1}.
$$

直接验证：

$$
\begin{bmatrix}
L_1&O\\
\ell_1&1
\end{bmatrix}
\begin{bmatrix}
A_1&\alpha^T\\
\alpha&a_2
\end{bmatrix}
\begin{bmatrix}
L_1^T&\ell_1^T\\
O&1
\end{bmatrix}
=
\begin{bmatrix}
L_1A_1L_1^T&O\\
O&a_2-\alpha A_1^{-1}\alpha^T
\end{bmatrix}.
$$

右端为对角阵，归纳完成。

---

## 第 3 页：参考解答（续）

### 3. 解

#### a)

略。正定性中，若

$$
\int_0^1 f^2(x)\,dx=0,
$$

由于 $f^2(x)\ge 0$ 且连续，可推出 $f(x)\equiv 0$。

#### b)

直接计算得度量阵

$$
G=
\begin{bmatrix}
(e_1,e_1)&(e_1,e_2)&(e_1,e_3)\\
(e_2,e_1)&(e_2,e_2)&(e_2,e_3)\\
(e_3,e_1)&(e_3,e_2)&(e_3,e_3)
\end{bmatrix}
=
\begin{bmatrix}
1&\dfrac12&\dfrac13\\[4pt]
\dfrac12&\dfrac13&\dfrac14\\[4pt]
\dfrac13&\dfrac14&\dfrac15
\end{bmatrix}.
$$

#### c)

$$
\varepsilon_1=e_1=1.
$$

又

$$
\eta_2=e_2-(e_2,\varepsilon_1)\varepsilon_1
=x-\frac12.
$$

单位化得

$$
\varepsilon_2=\sqrt{3}(2x-1).
$$

接着

$$
\eta_3=e_3-(e_3,\varepsilon_1)\varepsilon_1-(e_3,\varepsilon_2)\varepsilon_2
=x^2-x+\frac16.
$$

单位化得

$$
\varepsilon_3=\sqrt{5}(6x^2-6x+1).
$$

这是单位正交基，故该基下的度量阵为

$$
I_3.
$$

#### d)

线性性证明略。

令对偶基

$$
e_i^*=a_i+b_ix+c_ix^2,\qquad i=1,2,3,
$$

满足

$$
(e_j,e_i^*)=\delta_{ji}.
$$

计算可得

$$
G
\begin{bmatrix}
a_1&a_2&a_3\\
b_1&b_2&b_3\\
c_1&c_2&c_3
\end{bmatrix}
=
\begin{bmatrix}
1&0&0\\
0&1&0\\
0&0&1
\end{bmatrix}.
$$

于是

$$
\begin{bmatrix}
a_1&a_2&a_3\\
b_1&b_2&b_3\\
c_1&c_2&c_3
\end{bmatrix}
=
G^{-1}
=
\begin{bmatrix}
9&-36&30\\
-36&192&-180\\
30&-180&180
\end{bmatrix}.
$$

即对偶基为

$$
\begin{aligned}
e_1^*&=9-36x+30x^2,\\
e_2^*&=-36+192x-180x^2,\\
e_3^*&=30-180x+180x^2.
\end{aligned}
$$

容易看出

$$
I(f)=(e_1^*,f)+(e_2^*,f)+(e_3^*,f).
$$

因此

$$
h=e_1^*+e_2^*+e_3^*=3-24x+30x^2.
$$

---

## 第 4 页：参考解答（续）

#### e)

设 $\mathcal A^*$ 在基 $(e_1,e_2,e_3)$ 下的变换阵为 $A^*$。由共轭算子定义，对任意

$$
f(x)=f_0+f_1x+f_2x^2,\qquad g(x)=g_0+g_1x+g_2x^2\in V,
$$

成立

$$
(f_0,f_1,f_2)
\begin{bmatrix}
0&0&0\\
1&0&0\\
0&2&0
\end{bmatrix}
G
\begin{bmatrix}
g_0\\
g_1\\
g_2
\end{bmatrix}
=
(f_0,f_1,f_2)\,G A^*
\begin{bmatrix}
g_0\\
g_1\\
g_2
\end{bmatrix}.
$$

因此

$$
A^*
=
G^{-1}
\begin{bmatrix}
0&0&0\\
1&0&0\\
0&2&0
\end{bmatrix}
G
=
\begin{bmatrix}
-6&2&3\\
12&-24&-26\\
0&30&30
\end{bmatrix}.
$$

即

$$
\mathcal A^*g
=
(-6g_0+2g_1+3g_2)
+(12g_0-24g_1-26g_2)x
+(30g_1+30g_2)x^2.
$$

#### f)

对称双线性型的证明略。

系数方阵为

$$
C=
\begin{bmatrix}
II(\varepsilon_1,\varepsilon_1)&II(\varepsilon_1,\varepsilon_2)&II(\varepsilon_1,\varepsilon_3)\\
II(\varepsilon_2,\varepsilon_1)&II(\varepsilon_2,\varepsilon_2)&II(\varepsilon_2,\varepsilon_3)\\
II(\varepsilon_3,\varepsilon_1)&II(\varepsilon_3,\varepsilon_2)&II(\varepsilon_3,\varepsilon_3)
\end{bmatrix}
=
\begin{bmatrix}
1&-\sqrt3&\sqrt5\\
-\sqrt3&15&-13\sqrt{15}\\
\sqrt5&-13\sqrt{15}&365
\end{bmatrix}.
$$

由 $II$ 的定义知，在基 $(e_1,e_2,e_3)$ 下其系数阵为 $I_3$，它与 $C$ 相合。故 $C$ 的相合标准形为

$$
I_3.
$$
