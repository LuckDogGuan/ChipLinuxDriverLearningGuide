# 代码模板说明

> 这些是**脚手架**（编译配置、空壳程序），不是作业答案。手册规定：W01–W10 的代码自己先写第一版；W11 之后可以让 AI 起草，但必须逐行解释。
> 用法：把需要的文件夹**复制**到当周的 `04-笔记/Wxx/code/` 再改，不要直接在这里改。

| 文件夹 | 用在哪周 | 是什么 | 怎么用 |
|---|---|---|---|
| `c-app-makefile/` | W01–W10 | 用户态 C 程序通用 Makefile，带 ASan 和 ARM 交叉编译目标 | 把 `.c` 文件放进同一目录，执行 `make` / `make asan` / `make arm` |
| `kernel-module/` | W12–W19、W28 | 最小内核模块 `hello.c` + 外部模块 Makefile | 改 Makefile 里的 `KDIR` 指向野火提供的内核源码，执行 `make`，然后在板上 `insmod hello.ko`，用 `dmesg` 看输出 |
| `qemu-edu/` | W28–W32 | QEMU 启动带 EDU 设备的 x86_64 虚拟机的脚本 | 准备好内核 `bzImage` 和 `initramfs.cpio.gz`，执行 `./run.sh`，进去后 `lspci` 应看到 `1234:11e8` |
| `camdiag-cmake/` | W22、W35 | C++17 + OpenCV 的 CMake 工程骨架 | `cmake -B build && cmake --build build`，再运行 `./build/camdiag --buildinfo` 确认 OpenCV 是否带 FFmpeg/GStreamer |

## 需要提前装的工具（Ubuntu）

```bash
sudo apt install build-essential gdb make cmake git
```

```bash
sudo apt install gcc-arm-linux-gnueabihf
```

```bash
sudo apt install qemu-system-x86 qemu-system-arm gcc-aarch64-linux-gnu gdb-multiarch
```

```bash
sudo apt install libopencv-dev
```

> 交叉编译内核模块时，**优先用野火提供的、与板子镜像匹配的工具链**，上面 apt 装的那个只用于练习用户态程序。
