# W01 笔记 · 环境、数据表示、GDB 起步

[课程目录](../../README.md) · [本周课程](../../02-每周计划/阶段A-C与用户态-W01-W10/W01-环境-数据表示-GDB-起步.md) · [周报](report.md) · [代码](../../code/w01/)



## 学习记录

## D1

###  11/18
man gcc 可以直接查看gcc的使用手册
history 查看对应的历史指令
### 11/19
> C语言编译原理 
C源文件-》预处理-》编译-》汇编-》链接-》可执行文件
~~~c
hello.c 
// 1. 预处理 -> hello.i
gcc -E hello.c > hello.i
// 2. 编译   -> hello.s  变成汇编文件
gcc -S hello.i
// 3. 链接   -> hello.o 目标文件
gcc -c hello.s
// 4. 可执行文件 -> hello
gcc hello.o -o hello

// 一步到位 -> 可执行文件 hello1
gcc hello.c -o hello1
~~~

- vim 配置+ 常用快捷方式

看后续吧，如果常用vim 就去学一下，不常用的话就不用了。

> 编程习惯

1. 要注意全部的`waring` ！！！除非你能解释它的作用，否则一定要想办法优化他。 `-Wall` 这个打开全部的警告。 
2. `指针问题`，不能乱处理，要仔细考虑好为什么要这样做！！！

> 手册 man 
用法 man +xxx 即可 Linux 开发手册

>  插件

vscode 插件
1. C/C++ 
2. clangd

windows插件
1. [ssh-mcp ](https://github.com/LuckDogGuan/ssh-mcp) 方便ai工具，直接ssh连接操作服务器。

## D2

### 基础数据类型整理

> 说明：
>
> 1. C 语言中很多类型的长度不是固定死的，和 **编译器、CPU 架构、操作系统 ABI** 有关。  
> 2. 下表中的“常见值”主要参考 **64 位 Linux + GCC** 的常见情况。  
> 3. 实际项目中，最终要以 `sizeof(...)`、`limits.h`、`float.h` 和编译结果为准。  
> 4. “占位”列是给我后续自己实测填写的。
> 5. C语言只规定了对应的范围 char <=short <= int <=long,没有规定大小，和对应的平台相关。

#### 1. 整型基础类型总表

| 类型 | 常见字节数 | 常见位宽 | 是否可带符号 | 常见取值范围 | 说明 | 本机 `sizeof` 占位 |
|---|---:|---:|---|---|---|---|
| `char` | 1 | 8 | **实现相关**（可能 signed，也可能 unsigned） | `-128 ~ 127` 或 `0 ~ 255` | 最小寻址单位，常用于字符和字节数据 | `____` |
| `signed char` | 1 | 8 | 有符号 | `-128 ~ 127` | 明确指定有符号 | `____` |
| `unsigned char` | 1 | 8 | 无符号 | `0 ~ 255` | 常用于原始字节数据 | `____` |
| `short` / `short int` | 2 | 16 | 有符号 | `-32768 ~ 32767` | 短整型 | `____` |
| `unsigned short` | 2 | 16 | 无符号 | `0 ~ 65535` | 无符号短整型 | `____` |
| `int` | 4 | 32 | 有符号 | `-2147483648 ~ 2147483647` | 最常用整型 | `____` |
| `unsigned int` | 4 | 32 | 无符号 | `0 ~ 4294967295` | 无符号整型 | `____` |
| `long` | 8（Linux 64 位常见） | 64 | 有符号 | `-9223372036854775808 ~ 9223372036854775807` | **Linux 64 位常见 8 字节**，Windows 64 位常见 4 字节 | `____` |
| `unsigned long` | 8（Linux 64 位常见） | 64 | 无符号 | `0 ~ 18446744073709551615` | 需要注意平台差异 | `____` |
| `long long` | 8 | 64 | 有符号 | `-9223372036854775808 ~ 9223372036854775807` | 长长整型，通常固定 8 字节 | `____` |
| `unsigned long long` | 8 | 64 | 无符号 | `0 ~ 18446744073709551615` | 大范围无符号整型 | `____` |

---

#### 2. 浮点类型总表

| 类型 | 常见字节数 | 常见位宽 | 是否有符号 | 常见有效数字 | 常见范围（十进制近似） | 说明 | 本机 `sizeof` 占位 |
|---|---:|---:|---|---|---|---|---|
| `float` | 4 | 32 | 有符号 | 约 6~7 位 | `1.2e-38 ~ 3.4e38` | 单精度浮点 | `____` |
| `double` | 8 | 64 | 有符号 | 约 15~16 位 | `2.2e-308 ~ 1.8e308` | 双精度浮点，最常用 | `____` |
| `long double` | 16（常见） | 80 / 96 / 128（实现相关） | 有符号 | 通常高于 `double` | 依实现而不同 | 平台差异很大，不能想当然 | `____` |

#### 2.1 浮点数 注意

1. 浮点数不能像整数一样精确表示所有十进制小数，例如 `0.1` 往往不能被二进制浮点精确表示。  
所以比较浮点数时，通常不能直接 `a == b`，而是要比较误差范围。
~~~C
/// 比较范围这对吗？？？
int numberCheck(float number){
    if(number>0){
        return 1;
    }else if(number==0){
        return 0;
    }
    return -1;
}

/// number 是 float ,表示的数不是很精确
/// 1.0f / 3.0f = 0.3333 3循环。
/// 实际的收到类型范围的影响
/// float 1/3 = 0.333333
/// float 1/3 *3 = 0.99999999，永远都不能等于1.
/// 所以我们需要判断小于某一个范围就表示数据接近了。

// 误差范围 float 7位，
#defint EPSILON 1e-6f // 0.000001
int nunberCheck(float number){
    if(number>EPSILON){
        return 1;
    }else if(number<-EPSILON){
        return -1;
    }
    return 0;
}

~~~

2. 一般Linux内核中不适用浮点数据，一般 会保存为整数，后续会通过转换来读取,如果有FPU(Floating Point Unit) 还是能直接进行计算的，但是还会有调度开销，所以一般会避免。
3. stm32 单片机中，会先放大对应的数据，后续计算完成又缩小对应的数据  `定点数表示`,统一存储格式，以及精度。

---

#### 3. `signed` / `unsigned` 对比

| 对比项 | `signed`（有符号） | `unsigned`（无符号） |
|---|---|---|
| 是否表示负数 | 可以 | 不可以 |
| 取值范围特点 | 一半表示负数，一半表示正数 | 全部用于表示 0 和正数 |
| 是否适合计数/长度 | 一般也能用 | 更适合计数、长度、位操作 |
| 风险点 | 负数参与运算可能符合直觉 | 与有符号数混算时容易出 bug |
| 常见场景 | 普通数值计算 | 长度、容量、寄存器、位掩码 |

> `存储方式` 负数 = 去取绝对值+1,也就是补码。
> 例如
~~~c
 -254 -> 1111 1110
// 取反
 |-254| -> 0000 0001 +1 -> 0000 0010
~~~


> 开发中要特别注意：  
> **有符号数和无符号数混合运算**，经常会出现结果不符合直觉的情况。

--- 

#### 4. 平台差异要点

| 项目 | Linux 64 位（LP64 常见） | Windows 64 位（LLP64 常见） | 备注 |
|---|---|---|---|
| `char` | 1 字节 | 1 字节 | 一般一致 |
| `short` | 2 字节 | 2 字节 | 一般一致 |
| `int` | 4 字节 | 4 字节 | 一般一致 |
| `long` | 8 字节 | 4 字节 | **重点差异** |
| `long long` | 8 字节 | 8 字节 | 一般一致 |
| 指针 `void *` | 8 字节 | 8 字节 | 64 位一般为8字节 |

> 结论：  
> **不要想当然认为 `long` 一定是 8 字节。**  
> 做跨平台开发时，必须实测，或直接使用固定宽度整数类型。

---

#### 5. 固定宽度整数类型（推荐实际开发多用）

头文件：

```c
#include <stdint.h>
```

| 位宽 | 有符号 | 无符号 |
|---:|---|---|
| 8 位 | `int8_t` | `uint8_t` |
| 16 位 | `int16_t` | `uint16_t` |
| 32 位 | `int32_t` | `uint32_t` |
| 64 位 | `int64_t` | `uint64_t` |

- 数据手册明确写着“32 位寄存器”时，用户态练习可用 `uint32_t` 表示寄存器值。Linux 内核驱动中常见的对应类型是 `u32`（`<linux/types.h>`）。
- 字节数和 `sizeof` 的结果用 `size_t` 表示，`printf` 用 `%zu`。固定宽度类型适合协议字段和寄存器值，普通整数可从 `int` 选起。
- 上述精确宽度类型由实现按支持情况提供。目标平台支持 `uint32_t` 时，它正好是 32 位。

#### 6. 布尔类型与 `void`

- `_Bool` 是 C99 引入的布尔类型。在 C99 到 C17 中，引入 `<stdbool.h>` 后可写 `bool ready = true;`。转换到布尔类型时，零变为假，非零变为真。
~~~c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

void main(){
    bool status =true;
    printf("status = %d\r\n",status);
}
~~~

~~~
gcc boolTest.c -o boolTest && ./boolTest
~~~

- `void` 表示没有值。例如 `void reset(void)` 表示函数无返回值且不接收参数。
- `void *` 是通用对象指针，例如 `malloc` 返回的指针。访问所指对象时要使用对应类型的指针。

#### 7. 用 `sizeof` 实测

`sizeof` 的单位是 C 语言中的字节，`sizeof(char)` 恒为 1。`<limits.h>` 中的 `CHAR_BIT` 给出每字节的位数，`INT_MIN` 和 `INT_MAX` 给出 `int` 的取值上下限。

```c
#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

int main(void)
{
    bool ready = true;

    printf("CHAR_BIT = %d\n", CHAR_BIT);
    printf("sizeof(char) = %zu\n", sizeof(char));
    printf("sizeof(int) = %zu\n", sizeof(int));
    printf("sizeof(long) = %zu\n", sizeof(long));
    printf("sizeof(long double) = %zu\n", sizeof(long double));
    printf("sizeof(uint32_t) = %zu\n", sizeof(uint32_t));
    printf("INT_MIN = %d, INT_MAX = %d\n", INT_MIN, INT_MAX);
    printf("ready = %d\n", ready);
    return 0;
}
```

保存为 `types.c`，编译并运行，然后把输出填入上面的实测占位。

```bash
gcc -std=c11 -Wall -Wextra -pedantic types.c -o types && ./types
```

#### 8. 进制转换

> 要点

一般10进制转换为2进制 后，转换为 8，16进制 就很容易了。
> 例如

~~~c
254 -》B 11111110 -> 0 376 ->0x FE
// 默认是10 进制 是不带任何说明的。
// B 是二进制 C语言无法处理二进制，不要使用它。
// 0 开头是8进制
// 0x 是16进制
~~~

### char , 0 ,以及常见的错误。


## 疑问与资料
