# 外部内核模块 Makefile
# 1. 把 KDIR 改成野火提供的、与板子当前镜像匹配的内核源码目录（必须先在那里编译过内核）
# 2. 确认 CROSS_COMPILE 与野火工具链前缀一致
# 3. make  →  生成 hello.ko
#
# QEMU x86_64（W28）用宿主内核时改成：
#   make ARCH=x86_64 CROSS_COMPILE= KDIR=/lib/modules/$(uname -r)/build

obj-m := hello.o

KDIR          ?= /home/you/ebf-linux-kernel
ARCH          ?= arm
CROSS_COMPILE ?= arm-linux-gnueabihf-

all:
	$(MAKE) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) -C $(KDIR) M=$(CURDIR) modules

clean:
	$(MAKE) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) -C $(KDIR) M=$(CURDIR) clean

.PHONY: all clean
