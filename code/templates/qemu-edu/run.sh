#!/bin/sh
# QEMU 启动带 EDU 设备的 x86_64 虚拟机（W28 D6 一键启动脚本的起点）
# 用法：KERNEL=./bzImage INITRD=./initramfs.cpio.gz ./run.sh
# 进入后执行 lspci，应看到 1234:11e8。退出 QEMU：Ctrl+A 然后按 X
# 宿主机支持 KVM 时可加 -enable-kvm 加速（WSL2 通常不支持）

KERNEL=${KERNEL:-./bzImage}
INITRD=${INITRD:-./initramfs.cpio.gz}

exec qemu-system-x86_64 \
    -m 512M \
    -nographic \
    -kernel "$KERNEL" \
    -initrd "$INITRD" \
    -append "console=ttyS0 rdinit=/init" \
    -device edu
