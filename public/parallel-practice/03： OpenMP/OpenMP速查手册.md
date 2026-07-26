# OpenMP 速查手册

> 来源：陈默涵老师《并行程序设计》第 30-37 讲课件
> 适合：快速查阅 OpenMP 指令和编程模式

---

## 一、OpenMP 核心概念

### 三要素

```text
OpenMP = 编程指导语句（#pragma） + 库函数 + 环境变量
```

### Fork-Join 模式

```text
主线程 ──┬── 串行区
         ├── #pragma omp parallel ──┐
         │   线程0 线程1 ... 线程N   │  ← Fork（分叉）
         ├── #pragma omp parallel ──┘  ← Join（汇合）
         └── 串行区（只有主线程）
```

### 线程数优先级（从低到高）

1. 系统默认（通常 = CPU 核心数）
2. `OMP_NUM_THREADS` 环境变量
3. `omp_set_num_threads()` 库函数
4. `num_threads` 从句
5. `if` 从句（条件并行）

---

## 二、编译与基本指令

### 编译

```bash
g++ -fopenmp program.cpp -o program
```

### 头文件

```cpp
#include <omp.h>
```

### 常用库函数

| 函数 | 作用 |
|------|------|
| `omp_get_thread_num()` | 获取当前线程 ID（0 ~ n-1） |
| `omp_get_num_threads()` | 获取线程总数 |
| `omp_set_num_threads(n)` | 设置线程数 |
| `omp_get_wtime()` | 获取当前时间（秒），用于计时 |
| `omp_get_max_threads()` | 获取最大可用线程数 |

### 常用环境变量

| 环境变量 | 作用 | 示例 |
|----------|------|------|
| `OMP_NUM_THREADS` | 设置线程数 | `export OMP_NUM_THREADS=4` |
| `OMP_SCHEDULE` | 设置调度方式 | `export OMP_SCHEDULE=static,2` |
| `OMP_DYNAMIC` | 是否动态调整线程数 | `export OMP_DYNAMIC=false` |
| `OMP_NESTED` | 是否允许嵌套并行 | `export OMP_NESTED=false` |
| `OMP_STACKSIZE` | 设置线程栈大小 | `export OMP_STACKSIZE=20M` |

---

## 三、并行构造

### #pragma omp parallel

```cpp
#pragma omp parallel
{
    int id = omp_get_thread_num();
    std::cout << "Thread " << id << " says hello" << std::endl;
}
```

每个线程执行大括号内的**全部代码**。

### #pragma omp for

```cpp
#pragma omp parallel
{
    #pragma omp for
    for (int i = 0; i < N; i++) {
        a[i] = b[i] + c[i];   // 循环迭代自动分配给各线程
    }
}
```

### 组合式：parallel for（最常用！）

```cpp
// 等价于 parallel + for 的缩写
#pragma omp parallel for
for (int i = 0; i < N; i++) {
    a[i] = b[i] + c[i];
}
```

> **这是 OpenMP 最常见的写法**，一行指令搞定线程创建和循环划分。

### 循环限制

- 循环索引必须是**整数类型**（int）
- 循环边界必须在进入时确定（不能用 while）
- 循环之间不能有依赖关系

### SPMD 手动并行

```cpp
#pragma omp parallel
{
    int id = omp_get_thread_num();
    int nthreads = omp_get_num_threads();
    // 手动划分（周期分布）
    for (int i = id; i < N; i += nthreads) {
        // 每个线程处理每隔 nthreads 的元素
    }
}
```

---

## 四、同步机制

### 两类同步

```text
线程同步
├── 互斥同步（保护共享数据）
│   ├── critical  ← 临界区，块级保护
│   └── atomic    ← 原子操作，单条语句（更快）
│
└── 事件同步（协调执行顺序）
    ├── barrier   ← 显式同步点
    ├── master    ← 只让主线程执行
    ├── single    ← 只让某个线程执行
    └── ordered   ← 按循环顺序执行
```

### critical —— 互斥锁

```cpp
#pragma omp parallel
{
    // 每次只有一个线程能进入临界区
    #pragma omp critical
    {
        sum += local_sum;   // 安全！（但串行化，降低效率）
    }
}
```

### atomic —— 原子操作（优先使用！）

```cpp
#pragma omp parallel
{
    #pragma omp atomic
    sum += local_sum;       // 编译为一条机器指令，更快
}
```

> **atomic 比 critical 更快**，但只能保护**单条语句**。能用 atomic 就优先用 atomic。

### barrier —— 同步点

```cpp
#pragma omp parallel
{
    // 各线程做各自的工作...
    #pragma omp barrier      // 所有线程在此等待，直到全部到达
    // 然后一起继续...
}
```

> parallel、for、single、sections 构造末尾都有**隐式 barrier**。

### nowait —— 取消隐式 barrier

```cpp
#pragma omp for nowait     // for 结束后不等待其他线程，直接继续
```

### master vs single

| 指令 | 谁执行 | 末尾 barrier |
|------|--------|:--:|
| `master` | 只主线程（id=0） | **无** |
| `single` | 第一个到达的线程 | **有**（可用 nowait 去掉） |

### ordered —— 保证循环顺序

```cpp
#pragma omp parallel for ordered
for (int i = 0; i < N; i++) {
    #pragma omp ordered
    std::cout << i << " ";  // 按 i=0,1,2,... 顺序输出
}
```

> ordered 会大幅降低并行效率（5~10 倍正常），**非必要不用**。

---

## 五、调度（schedule）

### 四种调度方式

| 调度 | 语法 | 分配方式 | 适用场景 |
|------|------|----------|----------|
| `static` | `schedule(static[, chunk])` | 编译时固定分配 | 每次迭代工作量**相同** |
| `dynamic` | `schedule(dynamic[, chunk])` | 运行时动态分配 | 每次迭代工作量**不同** |
| `guided` | `schedule(guided[, chunk])` | 块大小逐渐减小 | 工作量差异大 |
| `auto` | `schedule(auto)` | 系统自选 | 不确定时 |

### static 的分块规则

```text
不指定 chunk: 每个线程一个大块（块数 = 线程数）
chunk = 1:    周期分配（轮流分配每个迭代）
chunk = k:    每 k 个连续迭代为一块，块间循环分配给线程
```

**例子**（3 线程，8 次迭代）：
- `schedule(static)` → 线程0:{0,1,2}, 线程1:{3,4,5}, 线程2:{6,7}
- `schedule(static, 2)` → 线程0:{0,1,6,7}, 线程1:{2,3}, 线程2:{4,5}

### static vs dynamic 对比

| 特性 | static | dynamic |
|------|--------|---------|
| 调度时机 | 编译时 | 运行时 |
| 调度开销 | 极低 | 高（每次分配都有开销） |
| 负载均衡 | 差（迭代时间不等时） | 好（自动均衡） |
| 何时用 | 可预测的均匀工作量 | 不可预测的不均匀工作量 |

---

## 六、数据环境

### 核心规则

> **并行区外定义的变量 → 默认共享（shared）**
> **并行区内定义的局部变量 → 默认私有（private）**

### 数据属性子句

| 子句 | 含义 |
|------|------|
| `shared(var)` | 所有线程共享，可读可写 |
| `private(var)` | 每个线程有独立副本，**初始值未定义** |
| `firstprivate(var)` | 每个线程有独立副本，**用外部值初始化** |
| `lastprivate(var)` | 类似 private，但最后迭代的值**写回外部** |
| `default(none)` | 强制显式声明所有变量的属性（推荐！用于 debug） |

### 例题

```cpp
int A = 1, B = 1, C = 1;
#pragma omp parallel private(B) firstprivate(C)
{
    // A: 共享（默认），可能被任何线程修改
    // B: 私有，初值未定义（不是1！）
    // C: 私有，初值 = 1
}
// 出来后：A 可能是被修改过的值，B=1，C=1（恢复外部值）
```

### threadprivate（全局变量私有化）

```cpp
int global_a;
#pragma omp threadprivate(global_a)   // 每个线程有独立的全局变量副本
```

关联子句：
- `copyin(var)`：进入并行区时，用主线程的值覆盖所有线程的 threadprivate 副本
- `copyprivate(var)`：single 结束时，把该线程的值广播给其他线程的私有副本

### 私有变量总结

| 从句 | 数据类型 | 作用范围 | 初始化 | 写回外部 |
|------|----------|----------|--------|----------|
| `private` | 局部变量 | 并行区域 | 未定义 | 否 |
| `firstprivate` | 局部变量 | 并行区域 | 外部值 | 否 |
| `lastprivate` | 局部变量 | 并行区域 | 未定义 | **是**（最后迭代值） |
| `threadprivate` | 全局变量 | 整个程序 | 继承主线程值 | - |
| `copyin` | 全局变量 | 并行区入口 | **强制**用主线程值覆盖 | - |
| `copyprivate` | 局部变量 | single 结束时 | - | 广播到所有线程 |

---

## 七、规约（reduction）

### 语法

```cpp
int sum = 0;
#pragma omp parallel for reduction(+ : sum)
for (int i = 0; i < N; i++) {
    sum += a[i];   // 每线程自动创建私有 sum，最后自动合并
}
```

### 常用规约运算符及初始值

| 运算符 | 含义 | 私有变量初始值 |
|--------|------|:--:|
| `+` | 求和 | 0 |
| `*` | 求积 | 1 |
| `-` | 求差 | 0 |
| `min` | 最小值 | 最大正数 |
| `max` | 最大值 | 最大负数 |
| `&` | 按位与 | ~0 |
| `|` | 按位或 | 0 |
| `^` | 按位异或 | 0 |
| `&&` | 逻辑与 | true |
| `||` | 逻辑或 | false |

---

## 八、collapse（循环合并）

```cpp
// 三重循环，只有 i 外层被并行，8 线程只有 2 个线程有任务
#pragma omp parallel for
for (int i = 0; i < 2; i++)
    for (int j = 0; j < 2; j++)
        for (int k = 0; k < 2; k++) { ... }

// collapse(2)：合并 i,j → 8 线程中 4 个有任务
#pragma omp parallel for collapse(2)
for (int i = 0; i < 2; i++)
    ...

// collapse(3)：合并 i,j,k → 8 线程全部有任务
#pragma omp parallel for collapse(3)
for (int i = 0; i < 2; i++)
    ...
```

> 前提：合并的循环间**不能有依赖关系**。

---

## 九、task 构造（OpenMP 3.0，不规则问题）

### 适用场景

- while 循环（长度编译时未知）
- 链表/树遍历（递归问题）
- 每次迭代工作量差异极大

### 用法

```cpp
#pragma omp parallel
{
    #pragma omp single
    {
        // 由一个线程启动递归，不断生成 task
        process_tree(root);   // 内部有 #pragma omp task
    }  // single 结束处有隐式 barrier，等待所有 task 完成
}
```

### 二叉树遍历示例

```cpp
void process_node(Node* node) {
    if (node == nullptr) return;

    #pragma omp task
    process_node(node->left);    // 左子树作为新 task

    #pragma omp task
    process_node(node->right);   // 右子树作为新 task

    #pragma omp taskwait         // 等待左右都算完
    // 处理当前节点...
}
```

### task vs section

| 特性 | task | section |
|------|------|---------|
| 任务划分 | 动态（运行时） | 静态（编译时固定数量） |
| 适用场景 | 递归、链表、不规则 | 固定数量的独立任务块 |
| 版本 | OpenMP 3.0+ | 早起版本 |

---

## 十、内存模型与伪共享

### 缓存层次

```text
寄存器（最快，最小）
  ↓
L1 缓存（每核私有）
  ↓
L2 缓存（每核私有）
  ↓
L3 缓存（共享，最后一级缓存）
  ↓
DRAM 主内存（最慢，最大）
```

### 伪共享（False Sharing）

**原因**：两个线程修改**不同变量**，但它们落在**同一缓存行**（64 字节），导致缓存频繁失效。

**表现**：性能差 10~100 倍（两个"无关"变量的修改互相干扰）

**解决方案**：
1. 变量 64 字节对齐：`alignas(64)`
2. 填充字节 padding
3. 尽量用线程私有变量
4. 操作数组时，让不同线程访问相隔较远的元素

### flush 操作

强制缓存中的数据写回内存，让其他线程能看到。在以下位置**隐式包含**：
- parallel 构造分叉时
- 进入/退出 critical 区域
- 进入/退出 task 区域
- 退出 barrier

---

## 十一、SIMD 向量化

### 概念

**SIMD = 单指令多数据**：一条指令同时对多个数据做相同操作（利用 128/256/512 位向量寄存器）。

### 编译器优化级别

| 级别 | 优化程度 | SIMD |
|------|----------|:--:|
| `-O0` | 无优化（默认） | ✗ |
| `-O1` | 轻度优化 | ✗ |
| `-O2` | 标准优化 | ✓ |
| `-O3` | 激进优化 | ✓✓ |

### OpenMP SIMD 指令

```cpp
#pragma omp simd           // 提示编译器向量化此循环
for (int i = 0; i < N; i++) {
    a[i] = b[i] + c[i];
}
```

### 编译器不自动向量化的情况

1. 循环内有 `if/else/break`（分支）
2. 循环内有外部函数调用
3. 数据有依赖（a[i] 依赖 a[i-1]）
4. 下标不连续
5. 浮点求和（不满足结合律，编译器不敢优化）

### 三重加速

```cpp
#pragma omp parallel for simd      // 多线程 + SIMD 同时使用！
for (int i = 0; i < N; i++) { ... }
```

---

## 十二、MPI-OpenMP 混合编程

```cpp
MPI_Init(&argc, &argv);
MPI_Comm_rank(MPI_COMM_WORLD, &rank);

// 每个 MPI 进程再开启 OpenMP 线程
#pragma omp parallel for num_threads(4)
for (int i = 0; i < N; i++) {
    local_data[i] *= 2;
}

MPI_Finalize();
```

> **模式**：MPI 负责跨节点（分布式内存），OpenMP 负责节点内（共享内存多线程）。

---

## 十三、OpenMP 快速记忆卡片

```text
┌──────────────────────────────────────────────────┐
│  #pragma omp parallel for  ← 最常用！             │
│  reduction(+:sum)          ← 安全求和             │
├──────────────────────────────────────────────────┤
│  数据默认属性                                      │
│  • 并行区外变量 → shared（共享）                   │
│  • 并行区内局部变量 → private（私有）              │
│  • 循环索引 i → 强制 private                      │
│  • 用 default(none) 强制显式声明（推荐）           │
├──────────────────────────────────────────────────┤
│  同步互斥                                         │
│  • critical → 临界区（块级），速度慢               │
│  • atomic → 原子操作（单条语句），速度快、优先用    │
│  • barrier → 同步等待，隐含在 for/parallel 末尾    │
│  • nowait → 取消隐式 barrier                      │
├──────────────────────────────────────────────────┤
│  调度                                            │
│  • static → 迭代均匀，编译时分配，开销低            │
│  • dynamic → 迭代不均匀，运行时分配，自动负载均衡    │
│  • 默认 chunk = N/nthreads (static) 或 1 (dynamic)│
├──────────────────────────────────────────────────┤
│  高级特性                                         │
│  • collapse(n) → 合并 n 层嵌套循环                 │
│  • task → 处理递归/链表/while等不规则问题          │
│  • #pragma omp simd → 向量化提示                  │
│  • -O3 编译才能激活自动 SIMD 向量化                │
├──────────────────────────────────────────────────┤
│  常见错误                                         │
│  • 数据竞争：多线程同时写共享变量（用 reduction/    │
│    critical/atomic 解决）                         │
│  • 伪共享：不同线程写同一缓存行的相邻变量 → 极慢    │
│  • 死锁：syncthreads 放 if/else 分支中              │
│  • 忘记 -fopenmp → 指令被忽略，程序变串行           │
└──────────────────────────────────────────────────┘
```
