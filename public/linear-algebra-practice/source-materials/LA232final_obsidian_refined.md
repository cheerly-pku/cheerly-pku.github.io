# LA232final（Obsidian 精校版）

_Source: LA232final.pdf_

## 第 1 页：试题

北京大学工学院课程试卷

课程名称：高等代数

2023-2024 学年第（2）学期期末。本试卷共 4 道大题，满分 100 分。

（考试结束后请将试卷、答题本一起交给监考老师）

以下各题中，数域均为 $\mathbb{R}$。

### 1.

#### 1）（15 分）

用最小二乘法近似求解方程组

$$
\begin{cases}
x_1-2x_2=4,\\
x_1-x_2=2,\\
x_1=1.
\end{cases}
$$

#### 2）（15 分）

对矩阵

$$
\begin{bmatrix}
1&2&3\\
3&2&1
\end{bmatrix}
$$

作奇异值分解。

#### 3）（15 分）

计算

$$
f(x,y,z)=x^2+2xy+2y^2+4yz+4z^2
$$

的规范形。

#### 4）（20 分）

在 $\mathcal P_2[x]$ 上定义内积

$$
(f,g)=\int_1^2 f(x)g(x)\,dx.
$$

若取

$$
\{x-1,(x-1)^2,1\}
$$

为一组基，求对偶基中相应于 $1$ 的基向量（多项式）；针对于上面给出的 $\mathcal P_2[x]$ 上的基，通过 Gram-Schmidt 正交化求单位正交基。

### 2.（15 分）

$n$ 阶对称方阵 $A,B$ 可同时正交对角化（即用同一正交矩阵为过渡阵）的充要条件是 $A,B$ 可交换，即

$$
AB=BA.
$$

### 3.（10 分）

$A$ 为 $n$ 阶对称正定阵，$x$ 为 $n$ 阶非零列向量，求证：

$$
|A+xx^T|>|A|.
$$

### 4.（10 分）

在 $n$ 维内积空间 $V$ 上，求证：双线性型 $f(a,b)$ 为对称的，当且仅当 $V$ 有一组标准正交基，使 $f(a,b)$ 的度量阵为对角阵。

---

## 第 2 页：参考解答

### 1.

#### 1）解

以系数阵的转置乘以增广矩阵，并作初等变换：

$$
\begin{bmatrix}
1&1&1\\
-2&-1&0
\end{bmatrix}
\begin{bmatrix}
1&-2&4\\
1&-1&2\\
1&0&1
\end{bmatrix}
=
\begin{bmatrix}
3&-3&7\\
-3&5&-10
\end{bmatrix}
\longrightarrow
\begin{bmatrix}
1&-1&\dfrac73\\[4pt]
0&2&-3
\end{bmatrix}.
$$

于是最小二乘解为

$$
x_1=\frac56,\qquad x_2=-\frac32.
$$

#### 2）解

设

$$
C=
\begin{bmatrix}
1&2&3\\
3&2&1
\end{bmatrix}.
$$

计算

$$
CC^T=
\begin{bmatrix}
14&10\\
10&14
\end{bmatrix},
$$

其特征对为

$$
\lambda_1=24,\qquad r_1=\frac1{\sqrt2}
\begin{bmatrix}
1\\
1
\end{bmatrix};
\qquad
\lambda_2=4,\qquad r_2=\frac1{\sqrt2}
\begin{bmatrix}
1\\
-1
\end{bmatrix}.
$$

令

$$
U=[r_1,r_2]=\frac1{\sqrt2}
\begin{bmatrix}
1&1\\
1&-1
\end{bmatrix}.
$$

奇异值为

$$
\sigma_1=2\sqrt6,\qquad \sigma_2=2.
$$

由

$$
v_i=\frac{C^Tr_i}{\sigma_i}
$$

得

$$
v_1=\frac1{\sqrt3}
\begin{bmatrix}
1\\
1\\
1
\end{bmatrix},
\qquad
v_2=\frac1{\sqrt2}
\begin{bmatrix}
-1\\
0\\
1
\end{bmatrix}.
$$

再补一个标准正交向量

$$
v_3=\frac1{\sqrt6}
\begin{bmatrix}
1\\
-2\\
1
\end{bmatrix}.
$$

于是可取

$$
V^T=
\begin{bmatrix}
\dfrac1{\sqrt3}&\dfrac1{\sqrt3}&\dfrac1{\sqrt3}\\[6pt]
-\dfrac1{\sqrt2}&0&\dfrac1{\sqrt2}\\[6pt]
\dfrac1{\sqrt6}&-\dfrac2{\sqrt6}&\dfrac1{\sqrt6}
\end{bmatrix},
\qquad
\Sigma=
\begin{bmatrix}
2\sqrt6&0&0\\
0&2&0
\end{bmatrix}.
$$

因此奇异值分解为

$$
C=U\Sigma V^T
=
\begin{bmatrix}
\dfrac1{\sqrt2}&\dfrac1{\sqrt2}\\[6pt]
\dfrac1{\sqrt2}&-\dfrac1{\sqrt2}
\end{bmatrix}
\begin{bmatrix}
2\sqrt6&0&0\\
0&2&0
\end{bmatrix}
\begin{bmatrix}
\dfrac1{\sqrt3}&\dfrac1{\sqrt3}&\dfrac1{\sqrt3}\\[6pt]
-\dfrac1{\sqrt2}&0&\dfrac1{\sqrt2}\\[6pt]
\dfrac1{\sqrt6}&-\dfrac2{\sqrt6}&\dfrac1{\sqrt6}
\end{bmatrix}.
$$

等价地，

$$
C
=
2\sqrt6
\begin{bmatrix}
\dfrac1{\sqrt2}\\[4pt]
\dfrac1{\sqrt2}
\end{bmatrix}
\begin{bmatrix}
\dfrac1{\sqrt3}&\dfrac1{\sqrt3}&\dfrac1{\sqrt3}
\end{bmatrix}
+
2
\begin{bmatrix}
\dfrac1{\sqrt2}\\[4pt]
-\dfrac1{\sqrt2}
\end{bmatrix}
\begin{bmatrix}
-\dfrac1{\sqrt2}&0&\dfrac1{\sqrt2}
\end{bmatrix}.
$$

> 注：原 PDF 此处 $V^T$ 中第二个奇异向量的符号疑似与题面矩阵不一致。上式按题面矩阵修正，满足 $C=U\Sigma V^T$。

#### 3）解

$$
f(x,y,z)=(x+y)^2+(y+2z)^2.
$$

令

$$
\tilde x=x+y,\qquad \tilde y=y+2z,
$$

则

$$
f(x,y,z)\equiv \tilde x^2+\tilde y^2.
$$

---

## 第 3 页：参考解答（续）

#### 4）解

记

$$
y=x-1.
$$

设对偶基中相应于 $1$ 的基向量为

$$
e^3=ay^2+by+c.
$$

由对偶基定义，应有

$$
\begin{cases}
\displaystyle \int_0^1 (ay^2+by+c)y\,dy=0,\\[6pt]
\displaystyle \int_0^1 (ay^2+by+c)y^2\,dy=0,\\[6pt]
\displaystyle \int_0^1 (ay^2+by+c)\,dy=1.
\end{cases}
$$

即

$$
\begin{cases}
\displaystyle \frac a4+\frac b3+\frac c2=0,\\[6pt]
\displaystyle \frac a5+\frac b4+\frac c3=0,\\[6pt]
\displaystyle \frac a3+\frac b2+c=1.
\end{cases}
$$

解得

$$
a=30,\qquad b=-36,\qquad c=9.
$$

故

$$
e^3=30y^2-36y+9=30x^2-96x+75.
$$

按 Gram-Schmidt 正交化，计算

$$
\varepsilon_1
=
\frac{y}{\sqrt{\int_0^1 y^2\,dy}}
=
\sqrt3(x-1).
$$

再算

$$
\widetilde e_2
=
y^2-\sqrt3y\int_0^1 y^2\sqrt3y\,dy
=
y^2-\frac34y.
$$

归一化得

$$
\varepsilon_2
=
\sqrt{80}\,\widetilde e_2
=
\sqrt5\bigl(4(x-1)^2-3(x-1)\bigr).
$$

类似算得

$$
\widetilde e_3
=
1-4y+\frac{10}{3}y^2.
$$

再归一化得

$$
\varepsilon_3
=
3-12(x-1)+10(x-1)^2.
$$

### 2. 证明

#### 必要性

若 $A,B$ 可同时正交对角化，即有正交矩阵 $P$，使

$$
PAP^T=\Lambda_1,\qquad PBP^T=\Lambda_2,
$$

其中 $\Lambda_1,\Lambda_2$ 为对角阵。由于对角阵可交换，

$$
\Lambda_1\Lambda_2=\Lambda_2\Lambda_1.
$$

于是

$$
AB
=
P^T\Lambda_1PP^T\Lambda_2P
=
P^T\Lambda_1\Lambda_2P
=
P^T\Lambda_2\Lambda_1P
=
BA.
$$

#### 充分性

若

$$
AB=BA.
$$

设对称阵 $A$ 的互异特征值为

$$
\lambda_1>\lambda_2>\cdots>\lambda_s,
$$

其代数重数（亦即几何重数）依次为

$$
n_1,n_2,\ldots,n_s,
\qquad
n_1+\cdots+n_s=n.
$$

则 $\mathbb R^n$ 直和分解为相应的特征子空间

$$
\mathbb R^n=V_1\oplus V_2\oplus\cdots\oplus V_s.
$$

对于任一个特征子空间 $V_i$ 中的向量 $v$，由

$$
Av=\lambda_i v
$$

知

$$
A(Bv)=B(Av)=\lambda_i Bv.
$$

故

$$
Bv\in V_i.
$$

因此 $V_i$ 为 $B$ 的不变子空间。又 $B$ 对称，所以 $B|_{V_i}$ 仍可在 $V_i$ 中取标准正交特征基而对角化。把各 $V_i$ 中取到的标准正交特征基合起来，即得 $\mathbb R^n$ 的一组标准正交基。在这组基下，$A,B$ 同时对角化。

---

## 第 4 页：参考解答（续）

等价地，由 $A$ 实对称，存在正交矩阵 $P$，使

$$
PAP^T=\operatorname{diag}(\lambda_1I_{n_1},\ldots,\lambda_sI_{n_s}).
$$

令

$$
\widetilde B=PBP^T=(B_{ij})
$$

为相应的分块矩阵。由 $AB=BA$ 可知

$$
\begin{bmatrix}
\lambda_1I_{n_1}&&O\\
&\ddots&\\
O&&\lambda_sI_{n_s}
\end{bmatrix}
\begin{bmatrix}
B_{11}&\cdots&B_{1s}\\
\vdots&\ddots&\vdots\\
B_{s1}&\cdots&B_{ss}
\end{bmatrix}
=
\begin{bmatrix}
B_{11}&\cdots&B_{1s}\\
\vdots&\ddots&\vdots\\
B_{s1}&\cdots&B_{ss}
\end{bmatrix}
\begin{bmatrix}
\lambda_1I_{n_1}&&O\\
&\ddots&\\
O&&\lambda_sI_{n_s}
\end{bmatrix}.
$$

于是对于非对角子矩阵，成立

$$
\lambda_i B_{ij}=\lambda_j B_{ij}.
$$

但 $i\ne j$ 时 $\lambda_i\ne \lambda_j$，因此

$$
B_{ij}=O.
$$

这就是说，$\widetilde B$ 为对称的块对角阵。由于每一个对角块仍然对称，故存在相应阶的正交矩阵 $Q_1,\ldots,Q_s$，使

$$
Q_iB_{ii}Q_i^T=\widetilde\Lambda_i
$$

为对角阵。于是

$$
\operatorname{diag}(Q_1,\ldots,Q_s)PAP^T\operatorname{diag}(Q_1^T,\ldots,Q_s^T)
=
\operatorname{diag}(\lambda_1I_{n_1},\ldots,\lambda_sI_{n_s}),
$$

且

$$
\operatorname{diag}(Q_1,\ldots,Q_s)PBP^T\operatorname{diag}(Q_1^T,\ldots,Q_s^T)
=
\operatorname{diag}(\widetilde\Lambda_1,\ldots,\widetilde\Lambda_s).
$$

故 $A,B$ 可同时正交对角化。

### 3. 证明

因为 $A$ 为对称正定阵，存在可逆矩阵 $P$，使

$$
P^TAP=I_n.
$$

记

$$
y=P^Tx.
$$

由于 $x\ne0$ 且 $P$ 可逆，故 $y\ne0$。于是

$$
P^T(A+xx^T)P=I_n+yy^T.
$$

取正交矩阵 $Q$，使

$$
Q^Ty=\begin{bmatrix}
\|y\|\\
0\\
\vdots\\
0
\end{bmatrix}.
$$

则

$$
Q^T(I_n+yy^T)Q
=
I_n+
\begin{bmatrix}
\|y\|^2&0&\cdots&0\\
0&0&\cdots&0\\
\vdots&\vdots&\ddots&\vdots\\
0&0&\cdots&0
\end{bmatrix}
=
\operatorname{diag}(1+\|y\|^2,1,\ldots,1).
$$

因此

$$
\bigl|P^T(A+xx^T)P\bigr|
=
1+\|y\|^2
>
1
=
|P^TAP|.
$$

又

$$
|P^T(A+xx^T)P|=|P|^2|A+xx^T|,
\qquad
|P^TAP|=|P|^2|A|,
$$

且 $|P|^2>0$，故

$$
|A+xx^T|>|A|.
$$

---

## 第 5 页：参考解答（续）

### 4. 证明

#### 必要性

若 $f$ 对称，任选一组标准正交基

$$
\{e_1,\ldots,e_n\}.
$$

则其度量阵 $G=(g_{ij})$ 中分量满足

$$
g_{ij}=f(e_i,e_j)=f(e_j,e_i)=g_{ji}.
$$

故 $G$ 为实对称阵。由实对称阵可正交对角化，存在正交矩阵 $P$，使

$$
\widetilde G=P^TGP
$$

为对角阵。

在基

$$
[\varepsilon_1,\ldots,\varepsilon_n]=[e_1,\ldots,e_n]P
$$

下，因为 $P$ 为正交矩阵，所以 $\{\varepsilon_1,\ldots,\varepsilon_n\}$ 仍为标准正交基；且该基下 $f$ 的度量阵正是

$$
\widetilde G=P^TGP,
$$

为对角阵。

#### 充分性

若某标准正交基 $\{e_1,\ldots,e_n\}$ 下 $f$ 的度量阵 $G$ 为对角阵，那么对任意两个向量

$$
a=x_1e_1+\cdots+x_ne_n,
\qquad
b=y_1e_1+\cdots+y_ne_n,
$$

由双线性性知

$$
\begin{aligned}
f(a,b)
&=\sum_{i,j=1}^n x_i y_j f(e_i,e_j)\\
&=\sum_{i=1}^n x_i y_i g_{ii}\\
&=\sum_{i=1}^n y_i x_i g_{ii}\\
&=f(b,a).
\end{aligned}
$$

因此 $f$ 为对称双线性型。证毕。
