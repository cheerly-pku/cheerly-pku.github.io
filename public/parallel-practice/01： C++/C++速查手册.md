# C++ 速查手册

> 来源：陈默涵老师《并行程序设计》第 10-11 讲课件
> 适合：C++ 基础薄弱，需要快速查阅语法和常用库

---

## 一、最简单的 C++ 程序

```cpp
#include <iostream>          // 头文件：提供输入输出功能
using namespace std;         // 使用标准命名空间（可以省去 std::）

int main() {                 // 主函数：程序的入口，必须有
    cout << "Hello World!" << endl;
    return 0;                // return 0 表示程序正常结束
}
```

编译运行：
```bash
g++ hello.cpp -o hello
./hello
```

### 逐个解释

| 元素 | 含义 |
|------|------|
| `#include <iostream>` | 预处理指令，在编译前把 iostream 头文件的内容"粘贴"进来 |
| `using namespace std;` | `std` 是标准库的命名空间，写了这行后 `cout` 不用写成 `std::cout` |
| `int main()` | 程序入口，`int` 表示返回整数（0=成功，非0=失败） |
| `cout << ...` | 标准输出流，`<<` 是插入运算符，把数据送到屏幕 |
| `endl` | 换行 + 刷新缓冲区 |

---

## 二、注释

```cpp
// 这是单行注释，从 // 到行末都被忽略

/*
 * 这是多行注释
 * 可以跨越多行
 * 编译器完全忽略
 */
```

---

## 三、基本数据类型

### 总览表

| 类型 | 含义 | 典型大小 | 范围 |
|------|------|----------|------|
| `int` | 整数 | 4 字节 | 约 -21亿 ~ 21亿 |
| `long long` | 长整数 | 8 字节 | 约 ±9×10¹⁸ |
| `float` | 单精度浮点 | 4 字节 | 6-7 位有效数字 |
| `double` | 双精度浮点 | 8 字节 | 15-16 位有效数字 |
| `char` | 字符 | 1 字节 | -128 ~ 127 |
| `bool` | 布尔 | 1 字节 | `true` / `false` |
| `size_t` | 无符号整数 | 8 字节（64位系统） | 用于表示大小和索引 |

### 关键记忆点

- **科学计算默认用 `double`**，精度比 `float` 高得多
- `complex<double>` 占 **16 字节**（两个 double）
- `int` 溢出是常见 bug（超过约 21 亿就溢出）
- `float` 字面量要加 `f`：`0.01f`（不加 `f` 默认是 `double`）

### int 溢出示例

```cpp
int x = 2000000000;  // 20 亿，没问题
int y = 2000000000;
int z = x + y;        // 40 亿，超出 int 范围 → 溢出，结果错误！
```

---

## 四、输入输出

### 屏幕输出（cout）

```cpp
#include <iostream>
#include <iomanip>   // 格式控制需要这个头文件
using namespace std;

int main() {
    double pi = 3.14159265358979;

    // 基本输出
    cout << "π = " << pi << endl;

    // 设置精度（有效数字位数）
    cout << setprecision(6) << pi << endl;        // 3.14159

    // 右对齐，占 10 个字符宽度
    cout << right << setw(10) << 123 << endl;     // "       123"

    // 用 # 填充空白
    cout << right << setfill('#') << setw(10) << 123 << endl;  // "#######123"

    // 科学计数法
    cout << scientific << pi << endl;             // 3.141593e+00

    // 十六进制输出
    cout << hex << 255 << endl;                   // ff

    return 0;
}
```

### 键盘输入（cin）

```cpp
int x;
cout << "请输入一个数字: ";
cin >> x;                        // 用户输入 → 存入变量 x
cout << "你输入的是: " << x << endl;
```

### 流与缓冲区的概念

- C++ 把输入输出当成**字节流**（stream）
- 输出先进入**缓冲区**（内存中的临时存储区），积累到一定量再写入屏幕/文件
- `endl` 会**刷新缓冲区**（立即输出），`'\n'` 只换行不刷新
- **Debug 技巧**：程序崩溃时缓冲区可能还没输出，导致误判错误位置 → 用 `endl` 确保即时输出

---

## 五、string 字符串

`std::string` 是 C++ 的字符串类型，比 C 风格字符数组好用得多。

```cpp
#include <string>
using namespace std;

// 定义
string s1;                    // 空字符串
string s2 = "Hello";          // 直接赋值
string s3("World");           // 构造函数方式

// 拼接
string s4 = s2 + " " + s3;    // "Hello World"

// 长度
int len = s4.length();        // 11（注意 length() 是函数，要加括号）

// 访问单个字符（下标从 0 开始！）
char c = s4[0];               // 'H'
s4[0] = 'h';                  // 修改为 "hello World"

// 查找
size_t pos = s4.find("World");       // 返回位置 6
size_t pos2 = s4.find("World", 7);   // 从位置 7 开始找
if (pos == string::npos) {           // npos 表示没找到
    cout << "未找到" << endl;
}

// 截取子串
string sub = s4.substr(6, 5);        // 从位置 6 开始取 5 个字符 → "World"

// 删除
s4.erase(8, 3);                      // 从位置 8 删 3 个字符

// 插入
s4.insert(1, "999");                 // 在位置 1 插入 "999"
```

### string vs 字符数组

| 特性 | `std::string` | `char[]`（字符数组） |
|------|---------------|---------------------|
| 内存 | 动态分配，自动管理 | 静态分配，需预设大小 |
| 操作 | 内置 `+`、`find`、`substr` 等 | 需手动用 C 函数 |
| 结尾 | 无需 `\0` | 必须以 `\0` 结尾 |
| 速度 | 稍慢 | 更快 |

---

## 六、const 限定符

`const` 修饰的变量**不能被修改**。

```cpp
const int MAX = 100;     // 常量，值不可改
// MAX = 200;            // 编译错误！

const double PI = 3.14159;

// const 在函数参数中：防止函数内部修改传入的变量
void print_time(const time_t& start) {
    // start 在函数内只读，不能被修改
}

// const 的规律：先作用于左边，没有左边再作用于右边
const int* p1;    // p1 指向的 int 是 const（不能通过 p1 改值）
int* const p2;    // p2 本身是 const（不能改指向，但能改值）
```

### 为什么用 const 而不是 #define？

```cpp
// ❌ 不推荐
#define PI 3.14159

// ✓ 推荐
const double PI = 3.14159;
```

原因：宏（`#define`）没有类型检查、不受作用域限制、出错信息难追踪。`const` 是真正的 C++ 变量，有类型、有作用域、编译器能检查。

---

## 七、文件输入输出

### 写文件（ofstream）

```cpp
#include <fstream>
using namespace std;

ofstream fout("output.txt");          // 打开文件用于写入
// ofstream fout("output.txt", ios::app);  // 追加模式

if (!fout) {                          // 检查文件是否打开成功
    cerr << "文件打开失败！" << endl;
    return 1;
}

fout << "Hello, file!" << endl;       // 写入文件（和 cout 语法一样）
fout.close();                         // 关闭文件
```

### 读文件（ifstream）

```cpp
#include <fstream>
using namespace std;

ifstream fin("input.txt");

if (!fin) {
    cerr << "文件未找到！" << endl;
    return 1;
}

// 读取 3×4 矩阵
double matrix[3][4];
for (int i = 0; i < 3; i++)
    for (int j = 0; j < 4; j++)
        fin >> matrix[i][j];

fin.close();
```

### 二进制文件读写

```cpp
// 写入二进制
double data[10000];
ofstream fout("out.binary", ios::binary);
fout.write(reinterpret_cast<char*>(data), sizeof(data));
fout.close();

// 读取二进制
ifstream fin("out.binary", ios::binary);
fin.read(reinterpret_cast<char*>(data), sizeof(data));
fin.close();
```

二进制格式的优点：精度无损、速度快、占空间小。缺点：人不可读。

---

## 八、stringstream（动态生成文件名）

```cpp
#include <sstream>

ostringstream oss;
for (int i = 1; i <= 100; i++) {
    oss.str("");                       // 清空
    oss << "output_" << i << ".dat";   // 拼接文件名
    string filename = oss.str();
    // 现在 filename = "output_1.dat", "output_2.dat", ...
}
```

---

## 九、编译器简介

| 编译器 | 平台 | 特点 |
|--------|------|------|
| **g++** | Linux/macOS/Windows | 开源免费，最常用，跨平台 |
| **Clang++** | macOS/Linux | 编译快，错误提示更友好 |
| **MSVC** | Windows | 微软 Visual Studio 自带 |

本课程使用 **g++**：

```bash
g++ source.cpp -o program    # 编译
./program                    # 运行
```

---

## 十、快速记忆卡片

```text
┌────────────────────────────────────────────┐
│  最常用的头文件                             │
│  <iostream>   cout / cin                   │
│  <iomanip>    setw / setprecision / right  │
│  <fstream>    ifstream / ofstream          │
│  <string>     std::string                  │
│  <sstream>    ostringstream                │
│  <cmath>      sqrt / pow / sin 等数学函数   │
│  <cassert>    assert() 断言                 │
│  <ctime>      time_t / clock_t 计时        │
├────────────────────────────────────────────┤
│  C++ 中下标从 0 开始！                      │
│  double 是科学计算的默认浮点类型             │
│  const 优于 #define                         │
│  endl 刷新缓冲区，'\n' 不刷新                │
└────────────────────────────────────────────┘
```
