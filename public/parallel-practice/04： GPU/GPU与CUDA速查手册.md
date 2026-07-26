# GPU 与 CUDA 速查手册

> 来源：陈默涵老师《并行程序设计》第 40-43 讲课件
> 适合：快速查阅 GPU 架构和 CUDA 编程核心概念

---

## 一、为什么用 GPU？

### CPU vs GPU 架构差异

| 特性 | CPU | GPU |
|------|-----|-----|
| 核心数 | 少（4-32） | 多（上千） |
| 单核性能 | 强（复杂逻辑） | 弱（简单运算） |
| 并行度 | 低 | 极高 |
| 缓存 | 大 | 小 |
| 擅长的任务 | 顺序、分支复杂的任务 | 数据并行、大规模计算 |
| 线程创建开销 | 大 | 极低 |

> **核心理念**：CPU 负责调度控制，GPU 负责密集计算（异构并行）。

### GPU 发展关键节点

| 年份 | 事件 |
|------|------|
| 1999 | 英伟达发布 GeForce 256，"GPU" 一词诞生 |
| 2006 | G80 架构：第一款支持 C 语言的 GPU，引入 SIMT 和共享内存 |
| 2010 | Fermi 架构（GTX 480）：每个 SM 32 个 CUDA 核心，共 512 核 |
| 2012 | AlexNet 用 2 颗 GTX 580 赢得 ImageNet 冠军，GPU 进入 AI |
| 2017 | Volta 架构（V100）：引入 TensorCore |
| 2022 | Hopper 架构（H100）：800 亿晶体管 |

---

## 二、GPU 硬件架构

### 关键层级

```text
GPU
├── SM（流式多处理器） × N
│   ├── CUDA 核心 × 32（Fermi）
│   ├── 共享内存 / L1 缓存
│   ├── 寄存器文件
│   ├── Warp 调度器 × 2
│   └── 指令分派单元
├── L2 缓存（所有 SM 共享）
└── DRAM 全局内存（显存）
```

### Fermi GTX 480 参数

- 15 个 SM × 每个 SM 32 个 CUDA 核心 = **512 个核心**
- 每个 SM 可同时处理 48 个 Warp（线程束）
- 48 × 32 = 每 SM 可处理 **1536 线程**
- 全 GPU 可发起：15 × 48 × 32 = **23040 个线程**

### Volta V100 性能

| 精度 | 峰值 |
|------|------|
| FP64（双精度） | 7.8 TFLOPS |
| FP32（单精度） | 15.7 TFLOPS |
| FP16（半精度） | 125 TFLOPS |

---

## 三、CUDA 编程模型

### 三个核心概念

1. **线程层次**：Thread → Block → Grid
2. **内存层次**：寄存器 → 共享内存 → 全局内存
3. **核函数（Kernel）**：CPU 调用，GPU 执行的函数

### Heterogeneous 异构并行流程

```text
1. 分配 GPU 内存        cudaMalloc()
2. CPU → GPU 拷贝数据   cudaMemcpy(HostToDevice)
3. 调用核函数            kernel<<<nblk, nthread>>>(params)
4. GPU → CPU 拷贝结果   cudaMemcpy(DeviceToHost)
5. 释放 GPU 内存        cudaFree()
```

### 编译和查看 GPU

```bash
# 编译 CUDA 程序
nvcc program.cu -o program

# 查看 GPU 状态
nvidia-smi
```

---

## 四、核函数（Kernel）

### 定义

```cpp
__global__ void kernel_func(params) {
    // 由每个 CUDA 线程执行
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    // 使用 idx 处理不同数据...
}
```

> `__global__`：CPU 调用，GPU 执行。
> `__device__`：只能被 GPU 函数调用（设备子函数）。

### 调用语法

```cpp
kernel_func<<<num_blocks, num_threads>>>(param1, param2, ...);
//            ↑ 线程块数量   ↑ 每块线程数
```

- `num_blocks` 和 `num_threads` 可以是 `int` 或 `dim3` 类型
- 核函数**不能**用 `cout`，只能用 `printf`

### 全局线程 ID

```cpp
int global_id = threadIdx.x + blockIdx.x * blockDim.x;
//               ↑ 块内线程号   ↑ 块号 × 块大小
```

### CUDA 内建变量（三维）

| 变量 | 含义 |
|------|------|
| `threadIdx.x / .y / .z` | 线程在块内的三维索引 |
| `blockIdx.x / .y / .z` | 线程块在 Grid 中的三维索引 |
| `blockDim.x / .y / .z` | 每个线程块的线程数（三维） |
| `gridDim.x / .y / .z` | Grid 中线程块的数量 |

### dim3：三维组织

```cpp
dim3 grid_dim(2, 1, 1);    // 2 个 Block（x方向）
dim3 block_dim(4, 4, 1);   // 每个 Block 4×4=16 个线程
kernel<<<grid_dim, block_dim>>>(...);
```

---

## 五、GPU 内存模型

### 内存类型一览

```text
速度 快 ←──────────────────────→ 慢
容量 小 ←──────────────────────→ 大

寄存器 ── 共享内存 ── 常量内存 ── 纹理内存 ── 全局内存
(线程私有) (Block 共享) (只读)   (只读)    (所有线程访问)
```

| 内存类型 | 访问速度 | 作用域 | 修饰符 | 特点 |
|----------|:---:|--------|--------|------|
| **寄存器** | 最快 | 单线程 | 默认（局部变量） | 数量极少，线程私有 |
| **共享内存** | 很快 | Block 内 | `__shared__` | 低 20-30 倍延迟，可编程缓存 |
| **常量内存** | 快 | 全局只读 | `__constant__` | 有缓存，适合 warp 内同地址读取 |
| **纹理内存** | 中等 | 全局只读 | `__texture__` | 空间局部性优化，图像处理 |
| **全局内存** | 最慢 | 全局读写 | 默认（显存） | 容量最大，所有线程可访问 |

### 全局内存

```cpp
// 分配 GPU 显存
float* d_data;
cudaMalloc((void**)&d_data, N * sizeof(float));

// CPU ↔ GPU 数据传输
cudaMemcpy(d_data, h_data, N * sizeof(float), cudaMemcpyHostToDevice);
cudaMemcpy(h_data, d_data, N * sizeof(float), cudaMemcpyDeviceToHost);

// 释放
cudaFree(d_data);
```

### 设备变量

```cpp
__device__ int dev_var;   // 全局内存中的变量，所有 GPU 线程可访问

// CPU 读写设备变量需用特殊函数
cudaMemcpyToSymbol(dev_var, &host_val, sizeof(int));
cudaMemcpyFromSymbol(&host_val, dev_var, sizeof(int));
```

### 共享内存

```cpp
__global__ void kernel() {
    __shared__ float s_data[256];   // 编译时确定大小（静态分配）
    // 或
    extern __shared__ float s_data[];  // 调用时确定大小（动态分配）

    s_data[threadIdx.x] = ...;
    __syncthreads();                // 确保所有线程写入完成后再读取
    float val = s_data[...];
}
```

> 共享内存访问延迟比全局内存低 20-30 倍，带宽高约 10 倍！

**共享内存动态分配示例**：

```cpp
// 核函数调用时，第三个参数指定共享内存字节数
kernel<<<1, 100, 100 * sizeof(float)>>>(...);
//                ↑ 动态共享内存大小
```

> A100 GPU：共享内存 48 KB，double 数组最多 48×1024/8 = 6144 个元素。

### 常量内存

```cpp
__constant__ float const_factor;   // 只读，有缓存

// 当 warp 内所有线程读取同一地址时：
// 硬件只从缓存读一次，然后广播给所有线程 → 极快
```

### 统一内存（CUDA 6.0+）

```cpp
// 简化编程：CPU 和 GPU 用同一指针
cudaMallocManaged(&data, N * sizeof(float));

// GPU 写完后，CPU 读之前需同步
cudaDeviceSynchronize();
```

> 统一内存**简化编程但无性能优势**。

---

## 六、原子操作

**问题**：多个线程同时读写同一地址 → 数据竞争。

**解决**：原子操作保证"读取-修改-写入"不被打断。

```cpp
// CUDA 原子加法
atomicAdd(&dev_sum, local_val);    // 安全！
// 其他：atomicSub, atomicExch, atomicMin, atomicMax, atomicAnd, atomicOr...

// 完整示例：64 个线程各自 +1，结果正确 = 64
__global__ void kernel() {
    atomicAdd(&dev_count, 1);  // 每个线程原子 +1
}
```

---

## 七、线程束（Warp）

### 基本概念

- **线程束大小 = 32 线程**（所有 NVIDIA GPU）
- Warp 是 GPU 的**基本调度和执行单元**
- 同一个 Warp 内的所有线程执行**相同指令**（SIMT）
- 一个 Block 内的线程按 32 个一组被划分为不同 Warp

### 线程束分支（Warp Divergence）

```cpp
__global__ void kernel() {
    if (threadIdx.x <= 8) {
        // 部分线程执行这里
    } else {
        // 另一部分线程执行这里
    }
    // 同一 Warp 内有分支 → GPU 硬件利用率下降！
}
```

> 同一 Warp 内尽量**避免分支**，否则一半线程闲置，利用率 50%。

### __syncthreads vs __syncwarp

| 同步函数 | 同步范围 | 注意事项 |
|----------|----------|----------|
| `__syncthreads()` | 整个 Block | **严禁**放在 if/else 分支内（部分线程跳过会死锁） |
| `__syncwarp()` | 同一 Warp 内（32 线程） | 可在分支内使用（只要同步的线程在同一 Warp） |

```cpp
// ✓ 安全：syncwarp 在分支内
if (threadIdx.x < 16) {
    __syncwarp();      // 只有 lane 0~15 参与，不会死锁
}

// ❌ 危险：syncthreads 在分支内
if (threadIdx.x < 16) {
    __syncthreads();   // 死锁！lane 16~31 跳过了，永远等不到
}
```

---

## 八、延迟隐藏

### 两类延迟

| 延迟类型 | 大小 |
|----------|------|
| 算术指令延迟 | ~10-20 时钟周期 |
| 访存指令延迟 | ~400-800 时钟周期 |

### GPU 如何隐藏延迟？

GPU 不靠减少单条指令延迟，而靠**大量并发线程束切换**：

```text
Warp 0 访存（等待） → SM 切换到 Warp 1 执行
Warp 1 访存（等待） → SM 切换到 Warp 2 执行
...
Warp 0 数据返回     → SM 切换回 Warp 0 继续
```

### 利特尔法则

$$所需 Warp 数 = 延迟 \times 吞吐量$$

例如：延迟 5 周期 × 每周期 6 个 Warp → 需要至少 **24 个活跃 Warp** 才能完全隐藏延迟。

---

## 九、完整示例：矩阵加法

```cpp
#include <iostream>
#include <cuda_runtime.h>

// 核函数
__global__ void matrixAdd(float* a, float* b, float* c, int n) {
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}

int main() {
    const int N = 4096;
    const int bytes = N * sizeof(float);

    // 1. CPU 端分配并初始化
    float *h_a = new float[N];
    float *h_b = new float[N];
    float *h_c = new float[N];
    for (int i = 0; i < N; i++) {
        h_a[i] = 1.0f; h_b[i] = 2.0f;
    }

    // 2. GPU 端分配显存
    float *d_a, *d_b, *d_c;
    cudaMalloc(&d_a, bytes);
    cudaMalloc(&d_b, bytes);
    cudaMalloc(&d_c, bytes);

    // 3. CPU → GPU 拷贝
    cudaMemcpy(d_a, h_a, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, bytes, cudaMemcpyHostToDevice);

    // 4. 调用核函数
    int threadsPerBlock = 256;
    int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;
    matrixAdd<<<blocksPerGrid, threadsPerBlock>>>(d_a, d_b, d_c, N);

    // 5. GPU → CPU 拷贝结果
    cudaMemcpy(h_c, d_c, bytes, cudaMemcpyDeviceToHost);

    // 6. 释放内存
    cudaFree(d_a); cudaFree(d_b); cudaFree(d_c);
    delete[] h_a; delete[] h_b; delete[] h_c;

    return 0;
}
```

**编译运行**：
```bash
nvcc matadd.cu -o matadd
./matadd
```

> **计算量**：4096 个元素 × 16 个 Block × 每 Block 256 线程 = 每个线程处理 1 个元素。

---

## 十、GPU 快速记忆卡片

```text
┌──────────────────────────────────────────────────┐
│  GPU 硬件                                         │
│  • SM = 流多处理器，GPU 的核心计算单元             │
│  • Warp = 32 线程，GPU 调度和执行的最小单位        │
│  • Block → 分为多个 Warp                          │
│  • 一个 SM 可同时处理大量并发 Warp（隐藏延迟）      │
├──────────────────────────────────────────────────┤
│  CUDA 编程                                        │
│  • __global__ → 核函数（CPU调GPU跑）              │
│  • __device__ → 设备函数（只能GPU调）             │
│  • <<<nBlk, nThd>>> → 核函数调用语法              │
│  • nvcc → CUDA 编译器                             │
│  • nvidia-smi → 查看 GPU 状态                     │
├──────────────────────────────────────────────────┤
│  内存（从快到慢）                                  │
│  • 寄存器 → 线程私有，最快                         │
│  • 共享内存(__shared__) → Block共享，快           │
│  • 常量内存(__constant__) → 全局只读，有缓存       │
│  • 全局内存 → 显存，全GPU可访问，最慢              │
│  • cudaMalloc / cudaMemcpy / cudaFree             │
├──────────────────────────────────────────────────┤
│  同步                                             │
│  • __syncthreads() → Block内同步，严禁放分支中     │
│  • __syncwarp() → Warp内同步，分支中可用           │
│  • cudaDeviceSynchronize() → CPU等GPU完成          │
│  • atomicAdd → 原子操作，防止数据竞争              │
├──────────────────────────────────────────────────┤
│  性能关键                                         │
│  • 避免 Warp 内分支（if/else）→ 降低利用率        │
│  • 多用共享内存代替全局内存（快 20-30 倍）          │
│  • 足够多的活跃 Warp 才能隐藏访存延迟              │
│  • 用 -O3 编译激活 SIMD（nvcc 也有优化选项）       │
├──────────────────────────────────────────────────┤
│  CPU-GPU 经典流程（五大步）                         │
│  cudaMalloc → cudaMemcpy(H2D) → kernel<<<>>>     │
│  → cudaMemcpy(D2H) → cudaFree                    │
└──────────────────────────────────────────────────┘
```
