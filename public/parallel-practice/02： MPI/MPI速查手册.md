# MPI 速查手册

> 来源：陈默涵老师《并行程序设计》第 20-25 讲课件
> 适合：快速查阅 MPI 函数和常用模式

---

## 一、MPI 核心概念

### MPI 是什么？

**MPI = Message Passing Interface（消息传递接口）**

- 不是一门编程语言，是**库**，需与 C/C++/Fortran 配合使用
- 用于**跨节点（进程）通信**的基础软件环境
- 每个进程有**私有存储空间**，进程间通过消息传递通信（和 OpenMP 共享内存不同）
- 程序通常采用 **SPMD**（Single Program Multiple Data）方式编写

### 进程 vs 线程

| 特性 | 进程（MPI） | 线程（OpenMP） |
|------|------------|---------------|
| 内存 | 私有，不共享 | 共享 |
| 通信 | 显式 Send/Recv | 读写共享变量 |
| 创建开销 | 大 | 小 |
| 跨节点 | ✓ | ✗ |

### 基本函数速查

| 函数 | 作用 |
|------|------|
| `MPI_Init(&argc, &argv)` | 初始化 MPI 环境（必须第一个调用） |
| `MPI_Finalize()` | 结束 MPI 环境（必须最后一个调用） |
| `MPI_Comm_size(comm, &size)` | 获取通信域中的进程数 |
| `MPI_Comm_rank(comm, &rank)` | 获取当前进程的 rank（0 ~ size-1） |
| `MPI_Get_processor_name(name, &len)` | 获取处理器名称 |
| `MPI_Wtime()` | 获取当前时间（秒），用于计时 |
| `MPI_Barrier(comm)` | 所有进程同步等待 |
| `MPI_Initialized(&flag)` | 检查 MPI 是否已初始化 |
| `MPI_Abort(comm, errorcode)` | 终止所有 MPI 进程 |
| `MPI_Get_version(&ver, &subver)` | 获取 MPI 版本号 |

---

## 二、编译与运行

### 编译器

| 编译器 | 语言 |
|--------|------|
| `mpicc` | C |
| `mpicxx` | C++ |
| `mpif90` | Fortran |

### 编译和运行命令

```bash
# 编译
mpicxx hello_world.cpp -o hello_world

# 运行（4 个进程）
mpirun -np 4 ./hello_world

# 同时设置 OpenMP 线程数
OMP_NUM_THREADS=2 mpirun -np 4 ./program
```

### Makefile 示例

```makefile
CC = mpicxx
CFLAGS = -O2 -Wall

hello_world: hello_world.cpp
	$(CC) $(CFLAGS) -o hello_world hello_world.cpp

clean:
	rm -f hello_world
```

### CMake 示例

```cmake
cmake_minimum_required(VERSION 3.10)
project(HelloWorld)
find_package(MPI REQUIRED)
add_executable(hello_world hello_world.cpp)
target_link_libraries(hello_world PRIVATE MPI::MPI_CXX)
```

---

## 三、Hello World 模板

```cpp
#include <iostream>
#include <mpi.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);                    // 1. 初始化

    int world_size, world_rank;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size); // 2. 获取进程数
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank); // 3. 获取当前rank

    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);

    std::cout << "Hello from processor " << processor_name
              << ", rank " << world_rank
              << " out of " << world_size << std::endl;

    MPI_Finalize();                            // 4. 结束
    return 0;
}
```

> **关键记忆**：Init → Comm_size/Comm_rank → 计算+通信 → Finalize

---

## 四、点对点通信（P2P）

### 阻塞通信

```cpp
// 发送
MPI_Send(buf, count, datatype, dest, tag, comm);

// 接收
MPI_Recv(buf, count, datatype, source, tag, comm, &status);
```

**参数记忆**：buf（数据地址）, count（个数）, datatype（类型）, dest/source（目标/源 rank）, tag（消息标签）, comm（通信域）

### 四种发送模式

| 函数 | 返回时机 | 缓冲 | 特点 |
|------|----------|------|------|
| `MPI_Send` | MPI决定 | 系统自动 | **最常用**，但大数据可能卡死 |
| `MPI_Bsend` | 立即返回 | 用户提供 | 绝不卡死，但使用繁琐 |
| `MPI_Ssend` | 接收方开始接收后 | 无 | 完全同步 |
| `MPI_Rsend` | 立即返回 | 无 | 性能最高，必须先启动接收 |

> **建议**：消息少用 MPI_Send；消息多用非阻塞通信，避免死锁！

### 非阻塞通信（推荐！）

```cpp
// 非阻塞发送和接收
MPI_Request request_s, request_r;
MPI_Isend(buf, count, datatype, dest, tag, comm, &request_s);
MPI_Irecv(buf, count, datatype, source, tag, comm, &request_r);

// 做计算...（通信和计算重叠！）

// 等待通信完成
MPI_Wait(&request_s, MPI_STATUS_IGNORE);
MPI_Wait(&request_r, MPI_STATUS_IGNORE);
```

**非阻塞通信的优势**：把一次阻塞调用拆成"启动"+"完成"，中间可以插入计算，**实现计算与通信重叠**。

### MPI_Isend vs MPI_Bsend

| 特性 | MPI_Isend | MPI_Bsend |
|------|-----------|-----------|
| 缓存 | 系统管理 | 用户手动提供 |
| 是否需 Wait | 必须 Wait | 不需要 |
| 使用难度 | 简单 | 麻烦 |
| 性能 | 高 | 低（多一次拷贝） |

### 死锁与解决方案

**死锁**：两个进程互相等待对方，都无法继续。

```cpp
// ❌ 可能死锁
if (rank == 0) {
    MPI_Send(..., 1, ...);
    MPI_Recv(..., 1, ...);
} else {
    MPI_Send(..., 0, ...);
    MPI_Recv(..., 0, ...);
}

// ✓ 方案1：用 MPI_Sendrecv（收发合一，避免死锁）
MPI_Sendrecv(sendbuf, count, type, dest, tag,
             recvbuf, count, type, source, tag, comm, &status);

// ✓ 方案2：用非阻塞通信
// ✓ 方案3：调整发送接收顺序（rank0先收后发）
```

### MPI_Status 结构体

包含三个字段：`MPI_SOURCE`（消息来源）、`MPI_TAG`（消息标签）、`MPI_ERROR`（错误码）

---

## 五、集合通信（Collective）

> 集合通信涉及通信域内**所有进程**，不接受 tag 参数。

### 一对多

| 操作 | 函数 | 含义 |
|------|------|------|
| 广播 | `MPI_Bcast` | 一个进程发相同数据到所有进程 |
| 分发 | `MPI_Scatter` | 一个进程发不同数据到不同进程 |

```cpp
// 广播：所有进程得到相同数据
MPI_Bcast(data, count, datatype, root, comm);

// 分发：从根进程分发不同数据给各进程
MPI_Scatter(sendbuf, sendcount, sendtype,
            recvbuf, recvcount, recvtype, root, comm);
```

### 多对一

| 操作 | 函数 | 含义 |
|------|------|------|
| 收集 | `MPI_Gather` | 收集各进程数据到根进程 |
| 规约 | `MPI_Reduce` | 对各进程数据做运算后汇总到根进程 |

```cpp
// 收集：各进程数据汇总到根进程
MPI_Gather(sendbuf, sendcount, sendtype,
           recvbuf, recvcount, recvtype, root, comm);

// 规约：求和（或求最大/最小等）到根进程
MPI_Reduce(sendbuf, recvbuf, count, datatype, op, root, comm);
```

### 多对多

| 函数 | 含义 |
|------|------|
| `MPI_Allreduce` | 规约后结果**广播给所有进程**（= Reduce + Bcast） |
| `MPI_Allgather` | 收集数据后**广播给所有进程**（= Gather + Bcast） |
| `MPI_Reduce_scatter` | 规约 + 分发组合操作 |
| `MPI_Alltoall` | 每个进程向所有进程发送不同数据 |
| `MPI_Scan` | 前缀和（每个进程拿到它及之前所有进程的累积结果） |

### 预定义规约操作

| 操作 | 含义 |
|------|------|
| `MPI_SUM` | 求和 |
| `MPI_PROD` | 求积 |
| `MPI_MAX` | 最大值 |
| `MPI_MIN` | 最小值 |
| `MPI_MAXLOC` | 最大值及位置 |
| `MPI_MINLOC` | 最小值及位置 |

### MPI_Reduce vs MPI_Allreduce

```text
MPI_Reduce:  结果只在 root 进程（其他进程没有）
MPI_Allreduce: 所有进程都有结果（多一次通信开销！）
```

---

## 六、MPI 数据类型

### 内置类型

| MPI 类型 | C/C++ 类型 |
|----------|-----------|
| `MPI_INT` | `int` |
| `MPI_FLOAT` | `float` |
| `MPI_DOUBLE` | `double` |
| `MPI_CHAR` | `char` |
| `MPI_LONG` | `long` |
| `MPI_BYTE` | 原始字节 |

> 注意：MPI 数据类型只用于 MPI 通信，不是 C++ 变量类型！

---

## 七、通信器与进程组

### 通信器（Communicator）

- `MPI_COMM_WORLD`：默认通信器，包含所有进程
- 所有 MPI 通信必须在某个通信器内进行

### MPI_Comm_split（划分通信器）

```cpp
MPI_Comm new_comm;
int color = rank % 2;     // 偶数进程 → color=0，奇数 → color=1
int key = rank / 2;       // 组内排序
MPI_Comm_split(MPI_COMM_WORLD, color, key, &new_comm);

// 使用 new_comm 进行组内通信...

MPI_Comm_free(&new_comm); // 用完后释放
```

**三个参数的含义**：
- `color`：分组依据，同色进同组（color = MPI_UNDEFINED 不加入任何组）
- `key`：组内 rank 排序依据
- **必须所有进程一起调用**，否则死锁！

### 进程组（Group）

- 进程组是"成员列表"，**不能直接用来通信**
- 可以求并集（`MPI_Group_union`）、交集（`MPI_Group_intersection`）、子集（`MPI_Group_incl`）
- 通过 `MPI_Comm_create` 基于进程组创建通信器才能通信

---

## 八、并行 I/O

三种模式：
1. **一个进程读写**：最稳定，适合小数据（但性能瓶颈）
2. **多进程各自读写不同文件**：简单，但输出文件多
3. **多进程协同读写同一文件**：最高性能，每个进程使用不同 offset

```cpp
MPI_File fh;
MPI_File_open(MPI_COMM_WORLD, "data.bin",
              MPI_MODE_CREATE | MPI_MODE_WRONLY,
              MPI_INFO_NULL, &fh);
// 每个进程在 offset = rank * sizeof(data) 处写入
MPI_File_write_at(fh, offset, buf, count, datatype, MPI_STATUS_IGNORE);
MPI_File_close(&fh);
```

---

## 九、性能分析

### 加速比

$$S_P = \frac{T_s}{T_P}$$

- $T_s$：串行程序运行时间
- $T_P$：P 个处理器的并行运行时间
- 理想：$S_P = P$（完美线性加速比）

### 强可扩展性 vs 弱可扩展性

| 类型 | 问题规模 | 变化量 | 衡量标准 |
|------|----------|--------|----------|
| 强可扩展性 | **不变** | 处理器数 P | 加速比 |
| 弱可扩展性 | **按比例增大** | 处理器数 P 和问题规模 | 单处理器效率 |

### 阿姆达尔定律

若串行部分占 $W_s$，并行部分占 $W_p$（$W_s + W_p = 1$），则最大加速比：

$$S_{max} = \frac{1}{W_s}$$

例如：25% 串行 → 最大加速比不超过 4 倍。

---

## 十、MPI 快速记忆卡片

```text
┌──────────────────────────────────────────────────┐
│  MPI 核心流程                                     │
│  Init → Comm_size/rank → 计算+通信 → Finalize    │
├──────────────────────────────────────────────────┤
│  编译运行                                         │
│  • mpicxx → 编译，mpirun -np N → 运行             │
│  • CMake: find_package(MPI REQUIRED)             │
├──────────────────────────────────────────────────┤
│  点对点通信                                       │
│  • MPI_Send/Recv → 阻塞（简单但可能死锁）          │
│  • MPI_Isend/Irecv + Wait → 非阻塞（推荐）        │
│  • MPI_Sendrecv → 收发合一，避免死锁              │
│  • 四种模式：Send/Bsend/Ssend/Rsend              │
├──────────────────────────────────────────────────┤
│  集合通信                                         │
│  • 一对多：Bcast（同数据）、Scatter（不同数据）     │
│  • 多对一：Gather（收集）、Reduce（汇总+运算）      │
│  • 多对多：Allreduce、Allgather、Scan             │
│  • Reduce 只在 root 有结果，Allreduce 全有         │
├──────────────────────────────────────────────────┤
│  通信器                                          │
│  • MPI_COMM_WORLD → 默认全进程通信器              │
│  • MPI_Comm_split(color, key) → 按颜色分组       │
│  • 必须所有进程一起调用 split，否则死锁！          │
├──────────────────────────────────────────────────┤
│  常见错误                                        │
│  • Send/Recv 不配对 → 死锁                       │
│  • 只有部分进程调用集合通信 → 死锁                │
│  • 忘记 MPI_Finalize → 资源泄漏                  │
│  • tag 不匹配 → 永远等不到消息                    │
└──────────────────────────────────────────────────┘
```
