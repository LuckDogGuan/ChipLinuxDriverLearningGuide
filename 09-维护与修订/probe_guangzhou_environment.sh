#!/usr/bin/env bash
set +e
export LC_ALL=C
echo '===OS==='
grep -E '^(PRETTY_NAME|VERSION_ID|ID)=' /etc/os-release
echo "KERNEL=$(uname -r)"
echo "ARCH=$(uname -m)"
echo '===HARDWARE==='
printf 'CPU_MODEL='
awk -F': ' '/model name/{print $2;exit}' /proc/cpuinfo
echo "LOGICAL_CPUS=$(nproc)"
awk '/MemTotal/{printf "RAM_GIB=%.1f\n", $2/1024/1024}' /proc/meminfo
printf 'ROOT_SIZE='
df -h --output=size / | tail -n1 | tr -d ' '
printf 'VIRTUALIZATION='
systemd-detect-virt 2>/dev/null || echo unknown
[ -e /dev/kvm ] && echo 'KVM_DEVICE=present' || echo 'KVM_DEVICE=absent'
echo '===DEVTOOLS==='
for p in gcc g++ clang clang++ gdb lldb make cmake git python3 pip3 ninja strace perf bpftrace qemu-system-aarch64 qemu-system-x86_64 qemu-aarch64 aarch64-linux-gnu-gcc arm-linux-gnueabihf-gcc rustc cargo docker podman clangd pkg-config nm objdump readelf ld; do
  if command -v "$p" >/dev/null 2>&1; then
    case "$p" in
      python3) v=$($p --version 2>&1 | head -n1) ;;
      git) v=$($p --version 2>&1 | head -n1) ;;
      make) v=$($p --version 2>&1 | head -n1) ;;
      gcc|g++|clang|clang++|aarch64-linux-gnu-gcc|arm-linux-gnueabihf-gcc) v=$($p --version 2>&1 | head -n1) ;;
      objdump|readelf|ld|nm) v=$($p --version 2>&1 | head -n1) ;;
      *) v=$($p --version 2>&1 | head -n1) ;;
    esac
    printf '%s|present|%s\n' "$p" "$v"
  else
    printf '%s|absent|not installed or not on PATH\n' "$p"
  fi
done
echo '===KERNEL_DEV==='
if [ -e "/lib/modules/$(uname -r)/build/Makefile" ]; then echo 'RUNNING_KERNEL_BUILD_TREE=present'; else echo 'RUNNING_KERNEL_BUILD_TREE=absent'; fi
for p in /sys/kernel/debug /sys/kernel/tracing /sys/kernel/debug/tracing; do
  if [ -d "$p" ]; then echo "TRACE_PATH=$p:present"; fi
done
echo '===OTHER==='
if command -v apt-get >/dev/null 2>&1; then echo 'PKG_MGR=apt'; elif command -v dnf >/dev/null 2>&1; then echo 'PKG_MGR=dnf'; fi
echo '===END==='
exit 0
