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


## 疑问与资料
