# 用户态 C 程序通用 Makefile（W01–W10）
# make        普通调试版（-g -O0）
# make asan   带 AddressSanitizer，查越界 / use-after-free / 泄漏
# make arm    交叉编译成 ARM 程序，拷到 i.MX6ULL 上运行
# make clean  清理

TARGET  := app
SRCS    := $(wildcard *.c)
CC      := gcc
CFLAGS  := -g -O0 -Wall -Wextra

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) -o $@ $^

asan: CFLAGS += -fsanitize=address -fno-omit-frame-pointer
asan: clean $(TARGET)

arm: CC := arm-linux-gnueabihf-gcc
arm: clean $(TARGET)
	file $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: asan arm clean
