# -*- coding: utf-8 -*-
from pathlib import Path
import re, hashlib, json, datetime
ROOT=Path(r'D:\VMShare\芯片底层软件40周')
BACKUP=Path(r'D:\VMShare\芯片底层软件40周-修改前备份-20261117')
assert ROOT.is_dir() and BACKUP.is_dir(), "目标或备份不存在"
def r(rel): return (ROOT/rel).read_text(encoding='utf-8-sig')
def w(rel, content):
    f=ROOT/rel; f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(content.replace('§',chr(96)).rstrip()+'\n', encoding='utf-8')
def replace(rel, old, new, expected=1):
    s=r(rel)
    assert s.count(old)==expected, (str(rel), repr(old),s.count(old))
    w(rel,s.replace(old,new))
def update(rel, fun):
    s=r(rel); n=fun(s)
    if n!=s: w(rel,n)
    return n!=s
# Individual week addenda: (visual entry, authoritative entry, diagnosis challenge, adjustment)
W = {
1:('Python Tutor: https://pythontutor.com/c.html','GDB: https://sourceware.org/gdb/documentation/','某个寄存器掩码只改动一位，为什么读回值不对？','位运算不熟才补课；熟悉的变量语法快进'),
2:('Python Tutor: https://pythontutor.com/c.html','Clang ASan: https://clang.llvm.org/docs/AddressSanitizer.html','定位一次越界/悬垂指针，记录错误栈与修复前后结果','指针题求质量，不刷重复题'),
3:('Compiler Explorer: https://godbolt.org/','Linux kernel C coding style: https://docs.kernel.org/process/coding-style.html','模拟初始化第二步失败，定位资源泄漏与重复释放','语法、枚举/位域不熟再补，不延长 D6'),
4:('Python Tutor: https://pythontutor.com/c.html','Kernel linked list: https://docs.kernel.org/core-api/list.html','删除链表节点后错误遍历，定位无效地址','单链表重复课程可快进'),
5:('Make 干跑命令 make -n','GNU Make 官方手册: https://www.gnu.org/software/make/manual/','改头文件后可执行文件没有重建，定位依赖缺失','make 只学依赖、变量、规则与排错'),
6:('Compiler Explorer: https://godbolt.org/','GDB manual: https://sourceware.org/gdb/current/onlinedocs/gdb.html','给定 core dump，反推崩溃函数、变量和根因','减少重复演示，保留交叉编译实证'),
7:('strace 调用时间线（本地工具）','Linux man-pages open(2): https://man7.org/linux/man-pages/man2/open.2.html','open 成功但 read 返回 EBADF，利用 strace 与 errno 找原因','熟悉的 stdio 可快进'),
8:('Python Tutor 观察单线程栈，线程另用 TSan','ThreadSanitizer: https://clang.llvm.org/docs/ThreadSanitizer.html','环形缓冲区出现丢项，排除竞争、容量与停止顺序','线程创建课程可自测后跳过'),
9:('画状态机与 epoll 事件时间线','epoll(7): https://man7.org/linux/man-pages/man7/epoll.7.html','故意制造设备断连后卡住，追踪 poll 返回值','不要扩展成网络服务器课程'),
10:('GDB TUI 观察变量和栈','GDB manual: https://sourceware.org/gdb/documentation/','用证据串起：现象→假设→排除→修复→回归','阶段展示主角是定位过程，不是程序界面'),
11:('画 ROM→U-Boot→Kernel→init 启动时间线','NXP i.MX6ULL 原厂文档: https://www.nxp.com/products/i.MX6ULL','串口停在某一启动阶段，证明究竟是内核前还是内核后出错','不要背诵启动流程，先核对真实串口日志'),
12:('dtc 反编译 DTB 对照 DTS','Linux Kbuild: https://docs.kernel.org/kbuild/modules.html','模块 insmod 报 invalid module format，查 vermagic 与日志','Buildroot 全流程仍先选读'),
13:('dmesg 与内核调用栈标注','Kernel driver API: https://docs.kernel.org/driver-api/index.html','设备 probe 失败时是否残留设备号/资源？逐项查','优先失败路径而不是多写一个演示驱动'),
14:('画 sysfs 的 bus→device→driver 匹配关系','Linux driver model: https://docs.kernel.org/driver-api/driver-model/overview.html','设备树 compatible 看似正确却不 probe，记录排查树','kobject 内部源码留选读'),
15:('dtc 生成设备树，画节点/引脚映射','Devicetree usage: https://docs.kernel.org/devicetree/usage-model.html','故意写错 compatible，查启动日志和运行时设备树','仅在具备恢复方案后改 DTB'),
16:('PulseView 波形 / GPIO 中断时间线','GPIO API: https://docs.kernel.org/driver-api/gpio/index.html','按键连续触发异常，区分机械抖动/中断配置/软件逻辑','pinctrl 内部实现维持选读'),
17:('KernelShark: https://kernelshark.org/','Linux tracing: https://docs.kernel.org/trace/index.html','poll 进程 CPU 占用异常，区分忙等和睡眠唤醒','只做一次轻量追踪预览；深入推迟至 W34'),
18:('PulseView I2C 地址与 ACK/NACK','Linux I2C: https://docs.kernel.org/i2c/index.html','读寄存器 NACK：按电源、引脚、地址、波形逐级排查','保留一个真实外设，减少重复样例'),
19:('PulseView SPI 波形 / UART 帧','Linux SPI API: https://docs.kernel.org/spi/spi-summary.html','SPI 读 ID 错位，验证 CPOL/CPHA/CS 而非猜测','UART 上位机交互不扩展成 UI 项目'),
20:('硬件三问：原理图→波形→寄存器','NXP 产品资料: https://www.nxp.com/products/i.MX6ULL','断线或错误中断模式故障注入，证据链必须完整','多接口联调以深挖故障为主，不追求外设数量'),
21:('画 Sensor→CSI→编码→RTSP→解码分层图','Luckfox 官方 Wiki: https://wiki.luckfox.com/','画面卡顿时只改变一个变量，判断采集/编码/网络哪段异常','暂时不要读 ISP 算法理论'),
22:('OpenCV Mat 结构尺寸与 stride 表','OpenCV 官方: https://docs.opencv.org/4.x/','图像出现花屏或行错位，核对 stride/format/width','只保留已有的少量 OpenCV API，不扩展模型训练'),
23:('V4L2 QBUF/DQBUF 队列状态图','V4L2 mmap: https://docs.kernel.org/userspace-api/media/v4l/mmap.html','REQBUFS/S_FMT 参数错误返回 EINVAL，从 ioctl 逐个验证','只到用户态接口，不要求 Sensor 内核驱动'),
24:('帧时间线：产生→采集→解码→处理','V4L2 capture.c: https://docs.kernel.org/userspace-api/media/v4l/capture.c.html','断流后卡住/帧率下降，区分超时、丢帧、积压','不引入复杂多媒体架构'),
25:('P1/P2 两条故障定位时间线对照','V4L2 API: https://docs.kernel.org/userspace-api/media/v4l/','复查一个摄像头故障：证据是否足以证明根因？','以技术复盘代替岗位调研，不提前锁定专项'),
26:('CPUlator: https://cpulator.01xz.net/ （ARMv7 对照）','Arm 架构学习: https://www.arm.com/architecture/learn-the-architecture','QEMU 启动失败时核对架构、入口地址、链接脚本','CPUlator 用来理解 ARMv7，不当作 AArch64 仿真'),
27:('逐字段画 ESR/ELR/SPSR 解释表','Arm 架构资料: https://developer.arm.com/Architectures/','故意触发同步异常，对比异常寄存器与源码地址','页表和 GIC 深入暂不强制'),
28:('QEMU monitor + lspci 枚举关系图','QEMU EDU: https://www.qemu.org/docs/master/specs/edu.html','设备未枚举，分清 QEMU 启动参数与驱动未绑定','QEMU 模型不等于真实 PCIe 链路'),
29:('PCI BAR 与 MMIO 访问关系图','Linux PCI HOWTO: https://docs.kernel.org/PCI/pci.html','BAR 映射失败：资源范围/使能/读写方法逐个查','不提前采购 PCIe 硬件'),
30:('中断时间线 /proc/interrupts','PCI interrupt: https://docs.kernel.org/PCI/pci.html','触发一次中断后无法再触发，检查设备 ACK 和共享 IRQ','先正确使用 IRQ，再选读 MSI-X'),
31:('DMA CPU→设备→内存地址转换图','DMA API HOWTO: https://docs.kernel.org/core-api/dma-api-howto.html','DMA 数据损坏：对比地址掩码、方向、同步与缓冲范围','先把 coherent/streaming 讲清，不强制实现 IOMMU'),
32:('QEMU EDU BAR/IRQ/DMA 全链路示意','QEMU EDU: https://www.qemu.org/docs/master/specs/edu.html','故障注入一次 MMIO/IRQ/DMA 错误，完整闭环','明确真实链路调试能力的边界'),
33:('画竞态时间线（CPU0/CPU1）','Kernel lockdep: https://docs.kernel.org/locking/lockdep-design.html','重现一次锁顺序错误或竞态，记录复现概率与修复','不要求一次穷尽所有锁类型'),
34:('KernelShark: https://kernelshark.org/','Kernel tracing: https://docs.kernel.org/trace/index.html','由 trace 找出一次异常延迟/CPU 热点并量化','perf/ftrace 保持性能与故障两条实验线'),
35:('Compiler Explorer: https://godbolt.org/','CMake 官方教程: https://cmake.org/cmake/help/latest/guide/tutorial/','修改编译参数触发接口/ABI 问题，收集构建证据','C++ 复习缩减，聚焦测试/资源管理'),
36:('Bootlin Elixir 源码交叉引用','Linux source: https://elixir.bootlin.com/linux/latest/source','旧 GPIO/驱动 API 导致构建失败，定位版本差异','不能把上游新 API 生搬到厂商旧内核'),
37:('画设备诊断采样流程与状态图','Kernel debug guide: https://docs.kernel.org/process/debugging/index.html','工具报告状态正常但设备实际异常，排除误判','诊断工具是内核能力的载体，不做 GUI'),
38:('把故障注入及回归结果画矩阵','Kernel debug guide: https://docs.kernel.org/process/debugging/index.html','复现三类故障并分别给出根因与回归证据','可复现、可定位优先于附加新功能'),
39:('选一条技术链画完整调用/数据流','Kernel docs: https://docs.kernel.org/','对选中机制做一次深入源码追踪和故障实验','专项按兴趣与实验条件选择，不按岗位筛选'),
40:('技术知识图谱 + 失败案例时间线','Linux Kernel docs: https://docs.kernel.org/','陌生故障盲测：不给现成答案，用完整六步定位','最终展示重点是可复现技术证据，不做简历包装'),
}
assert len(W)==40
# 1. Rename two active files and replace internal references without touching archived complete original
week_dirs={int(m.group(1)):f for f in ROOT.rglob('W*.md') if '02-每周计划' in str(f) if (m:=re.match(r'W(\d\d)-',f.name))}
assert set(week_dirs)==set(range(1,41)), (len(week_dirs), set(range(1,41))-set(week_dirs))
names={
'W25-轻量周-岗位核对与展示-C.md':'W25-轻量周-机制复盘与展示-C.md',
'W39-岗位专项选修-三选一.md':'W39-专项机制深入-三选一.md'
}
for old,new in names.items():
    f=next(f for f in week_dirs.values() if f.name==old)
    dest=f.with_name(new)
    assert not dest.exists()
    f.rename(dest)
week_dirs={int(m.group(1)):f for f in ROOT.rglob('W*.md') if '02-每周计划' in str(f) if (m:=re.match(r'W(\d\d)-',f.name))}
# title/labels/skill gap general replacements in active documents
for f in ROOT.rglob('*.md'):
    if f.name=='原手册-完整版.md':continue
    s=f.read_text(encoding='utf-8-sig')
    for old,new in names.items(): s=s.replace(old,new)
    s=s.replace('岗位核对与展示 C','机制复盘与展示 C')
    s=s.replace('岗位专项选修：三选一','专项机制深入：三选一')
    s=s.replace('岗位专项选修：三选一','专项机制深入：三选一')
    s=s.replace('招聘技能缺口表','技术机制缺口表')
    s=s.replace('技能缺口表','技术机制缺口表') if '技术技术机制' not in s else s
    s=s.replace('技术技术机制缺口表','技术机制缺口表')
    if s!=f.read_text(encoding='utf-8-sig'):f.write_text(s,encoding='utf-8')
# 2. Rewrite the three obsolete week task tables. Keep metadata, links and delivery sections.
table25='''| 日 | 任务 |
|---|---|
| D1 | 📝 P1、P2 各写一页 README，重点列清数据流、版本、根因与限制 |
| D2 | ✅ 对照官方 V4L2、i.MX6ULL 文档复查本阶段 3 个重要机制；形成“已理解/未理解/缺少证据”技术缺口表 |
| D3 | 🔧 复现 P1 或 P2 的一个故障，提交假设→实验→根因→回归六步证据 |
| D5 | ⭐ 用流程图比较 RTSP、V4L2 用户态、媒体子系统；选读 NJU 操作系统 |
| D6 | 🔧 **展示 C**：解释一帧数据路径、举一例完整定位；只列未来要补的共同基础，不提前选最终专项 |

验收：能用原始资料解释 V4L2 用户态采集和实际局限，完成一份可复现的故障报告。 ☐D1 ☐D2 ☐D3 ☐展示C'''
table39='''| 日 | 任务 |
|---|---|
| D1 | ✅ 回看前 38 周证据，列出三个最难解释的底层机制及待验证问题 |
| D2 | ✅ 选一个机制深挖：**A 启动/BSP/内核**、**B PCI/中断/DMA**、**C V4L2/媒体数据通路**；不按岗位或学历筛选 |
| D3 | 🔧 对照官方手册和对应内核源码，复现一个有解释价值的小实验 |
| D4 | 📝 画调用链/寄存器图/数据流，写出已验证、推断和无法验证的边界 |
| D5 | ⭐ 只作视野扩展：RTOS、RISC-V、NPU Runtime、GPU 驱动，不强制开始新专项 |
| D6 | 🔧 2–3 页机制技术报告：原始出处、实验、故障定位、限制与下一轮问题 |

验收：完成一条原始文档→源码→运行证据→根因分析的链条，不要求此时决定长期唯一专项。 ☐D1 ☐D2 ☐D3 ☐D4 ☐D6'''
table40='''| 日 | 任务 |
|---|---|
| D1 | 📝 整理 P1–P4 的 README：环境、版本、源代码、可复现流程、失败案例 |
| D2 | 📝 绘制 40 周技术知识图谱，区分已实测、源码阅读、虚拟验证和待验证 |
| D3 | 🔧 从已有项目中盲选一个故障，演示独立排查、定位和回归 |
| D5 | ⭐ 根据自己最有兴趣的底层机制，列下一阶段可能深入的 2–3 条分支，不必立刻做唯一选择 |
| D6 | 🔧 **最终展示**：项目复现、原始出处、调试证据、局限说明、未来 12 周深入学习假设 |

验收：干净环境能基本复现；调试报告有假设与排除证据；不把仿真学习描述成实机能力。 ☐D1 ☐D2 ☐D3 ☐最终展示'''
for n,table in [(25,table25),(39,table39),(40,table40)]:
    f=week_dirs[n];s=f.read_text(encoding='utf-8')
    s=re.sub(r'\| 日 \| 任务 \|\n\|---\|---\|.*?(?=\n\n## 本周交付清单)',table,s,flags=re.S)
    if n==25: s=re.sub(r'^# .+$','# W25　轻量周：机制复盘与展示 C',s,count=1,flags=re.M)
    if n==39: s=re.sub(r'^# .+$','# W39　专项机制深入：三选一',s,count=1,flags=re.M)
    w(f.relative_to(ROOT),s)
# 3. Weekly addenda, all individualized and not additive to fixed weekly hours
for n,f in sorted(week_dirs.items()):
    vis,src,challenge,reduce=W[n]
    s=f.read_text(encoding='utf-8')
    assert '## 本周深化与定位挑战（2026-11-17 修订）' not in s
    addition=f'''
## 本周深化与定位挑战（2026-11-17 修订）

> 与上面的 D1–D6 课程配套，**替换**部分重复观看或练习，不额外增加固定学习时间；每周调试训练用 [六步定位法](../../05-学习校验/调试能力贯穿40周.md) 记录。70% 是训练重心，不是机械划分学时。

- **先看可视化（5–10 分钟）**：{vis}；先直观理解现象，不追求一次精通。
- **再看一手资料（优先查相关一节）**：{src}。记录实际版本/章节/关键函数或寄存器；[原始资料阅读方法](../../03-资料链接/一手资料阅读路线.md)。
- **本周定位挑战（🔧 与 D6 实验合并）**：{challenge}。提交现象、两个假设、排除证据、根因/尚未知、回归结果。
- **减负与边界**：{reduce}。任何硬件特性先以手册、实机配置和日志为准，失败可交阻塞报告。
- **可视化工具总表**：[可视化学习地图](../../03-资料链接/可视化学习地图.md)；报告见 [故障定位报告模板](../../07-模板/故障定位报告模板.md)。
'''
    w(f.relative_to(ROOT),s.rstrip()+'\n\n'+addition)
# 4. New learning material and primary-source hierarchy
w('00-总览与规则/新版路线与删减依据.md','''# 2026-11-17 修订：长期芯片底层软件学习路线

> 此文是**现行规则**；[原手册-完整版](原手册-完整版.md)为不改动的历史快照。保留 W01–W40、A–E 阶段、M1–M21、P1–P4 和全部原始视频讲次。

## 核心目标

C/Linux 系统编程 → 内核/BSP/真实设备驱动 → 小规模摄像头/V4L2 数据通路 → AArch64/PCI/IRQ/DMA → 系统级调试、性能、机制深入。长期向芯片系统软件、深度驱动、Runtime/Firmware 进阶，**不设置近期求职主线或学历筛选**。

**不必 W08–12 决定最终专项**。可先接触多个子系统的通用机制；到 W39 对一个机制做一次深入验证，仍保留后续选择空间。不是每个底层岗位都要求全部方向。

## 70% 定位能力的落实方式

70% 指训练倾向：每周尽量把动手时间用于故障注入、假设与排除、复现实验、源码/寄存器定位、修复和回归，而不是把 70% 课程专门变成调试工具讲解。每周既学习原理，也要收集一个能证明或否定假设的证据。

## 深度递进和边界

1. W01–10：C、指针/内存、GDB/ASan/strace、系统调用、并发。已掌握的基本语法先自测快进。
2. W11–20：启动链路、kbuild、DTS、设备模型、中断、I2C/SPI/UART；面对具体寄存器直接查 i.MX6ULL 原厂手册和板卡原理图。模块 Oops/ftrace 入门随学随用。
3. W21–25：保持简单，OpenCV 少量 API；V4L2 只要求用户态采集和缓冲队列。**不要求 Sensor 内核驱动、ISP 算法或媒体子系统内部实现。**
4. W26–32：ARMv7 vs AArch64、异常、QEMU x86_64 PCI EDU、MMIO/中断/DMA。明确仿真与真实硬件不是一回事。
5. W33–40：竞态、锁、追踪/性能、版本差异、深度故障复盘。W39 先深入一个机制，不要求锁定毕生专项。

## 每周建议顺序

可视化 5–10 分钟 → 官方资料挑一节 → 原课程/源码 → 小实验 → 故障六步记录 → 五道门验收。可视化是桥梁，不是替代手册或运行证据。旧课程对应内核版本可能较老：具体 API 以板上内核源码与版本为准。

## 做减法的内容

- 普通 C 语法、链表重复演示、Makefile 细枝末节、复杂 GUI / 图像算法和 YOLO 训练：自测通过快进或 ⭐。
- 不删除驱动基本机制：GPIO、IRQ、设备树、I2C/SPI、PCI、DMA 都要理解，但不强制每个外设做大量项目。
- W25、W39、W40 从岗位缺口/简历训练改为机制复盘、源码追踪和技术证据。
- 所有旧教学链接原样保留作补充，资料优先级为：原厂 Datasheet / Reference Manual / Errata / 原理图 → Linux 官方文档 / 精确版本源码 → 官方培训/实验 → 可视化 → 二手课程。

## 本次配套新增

- [原厂资料与源码查找](../03-资料链接/一手资料阅读路线.md)
- [可视化学习地图](../03-资料链接/可视化学习地图.md)
- [40 周调试能力路线](../05-学习校验/调试能力贯穿40周.md)
- [原始资料/故障双联记录卡](../07-模板/技术手册阅读与故障归因卡.md)
- [修订与复核记录](../09-维护与修订/本次变更及两轮核验.md)
''')
w('03-资料链接/一手资料阅读路线.md','''# 一手资料阅读路线：手册 → 源码 → 实机证据

> **一手资料**不是“从头到尾啃完一本参考手册”，而是围绕当周实验定位**具体章节/函数/寄存器**。记录版本、章节和证据；先浅后深。

## 资料优先级与用途

| 第一手材料 | 链接/入口 | 应该怎么读 |
|---|---|---|
| NXP i.MX6ULL 原厂产品/资料 | https://www.nxp.com/products/i.MX6ULL | 先核对板卡实际芯片型号；找 IMX6ULLRM、数据手册和 Errata；部分下载需 NXP 账户 |
| 野火板卡原理图与救援手册 | http://doc.embedfire.com | W11 起核对引脚、供电、模块/镜像版本，先备份再刷写 |
| Linux 内核官方文档 | https://docs.kernel.org/ | 按版本/章节查询 kbuild、driver model、GPIO、I2C、DMA、tracing |
| 当前板卡实际内核源码 | 野火或 Luckfox SDK（以本机实际版本为准） | 最终判断接口是否可用的依据：记录 §uname -a§、编译器、源码提交号 |
| Linux 上游源码交叉引用 | https://elixir.bootlin.com/linux/latest/source | 查函数和结构体调用路径；**latest 仅作导航**，回头对应厂商源码 |
| QEMU EDU 原始设备说明 | https://www.qemu.org/docs/master/specs/edu.html | W28–32 对照 BAR、中断寄存器和 DMA 指令 |
| Linux V4L2 mmap 用户态 API | https://docs.kernel.org/userspace-api/media/v4l/mmap.html | W23 看缓冲流转；不要求此时学习内核 vb2 实现 |
| V4L2 官方 capture.c 示例 | https://docs.kernel.org/userspace-api/media/v4l/capture.c.html | 从设备打开→初始化→QBUF/DQBUF 对照自己的程序 |
| Arm 官方学习资源 | https://www.arm.com/architecture/learn-the-architecture | AArch64、异常、寄存器；区分 ARMv7 和 AArch64 |
| Linux 调试官方指南 | https://docs.kernel.org/process/debugging/index.html | 根据用户态、驱动态、trace 章节逐项查证 |

## 按阶段精选“只看这一段”

- W01–06：GDB 文档中的断点、回溯、观察内存；ASan 官方文档先看报告解析。
- W07–10：man7 的 open/read/ioctl/poll/epoll；用 strace 观察系统调用而非死记参数。
- W11：NXP Reference Manual 的芯片/引脚/时钟章节入口，核对原理图；W12 再读对应内核启动/模块构建部分。
- W13–20：实验用到哪种外设，只读该外设的寄存器描述、时序图和对应驱动源码；补上 Errata 检查。
- W21–25：V4L2 的 mmap 和 capture.c。OpenCV 保持基础，不需要研究训练算法或深入 ISP。
- W26–27：Arm 异常/异常级别体系；先用 QEMU 和串口输出验证，ARMv7 板不假装能跑 AArch64。
- W28–32：QEMU EDU spec + Linux PCI HOWTO + DMA API HOWTO；先讲设备与软件模型。
- W33–40：内核锁/trace/perf/调试手册，追踪实际错误和内核版本差异。

## 每次读手册的 7 分钟方法

1. 我看到的现象是什么？要查的具体外设/接口是什么？
2. 原理图里它接在哪个引脚/总线？供电、复位、时钟来自哪里？
3. 原厂手册哪一章解释这个寄存器/时序？版本、页码、位域和复位值是什么？
4. 当前内核源码哪个函数使用这个设备？关键寄存器写在哪里？
5. 运行时用什么证据证明或推翻假设？日志、寄存器、波形、trace。
6. 将“已经实测 / 仅源码推断 / 参考资料提出 / 未知”明确分开。

> 重要：禁止根据另一个 i.MX 系列芯片的寄存器地址猜测当前板卡；没有真实硬件验证时，不声称完成实机驱动调试。
''')
w('03-资料链接/可视化学习地图.md','''# 可视化学习地图：只为理解底层机制服务

> 可视化资源并不能代替原厂文档。每次使用 5–15 分钟，先观察再调试。部分为在线网站，KernelShark/PulseView 是本地工具；链接可能变化，无法访问就用本地示意图和日志替代。

| 周 | 工具（链接） | 看什么 | 不适用的地方 |
|---|---|---|---|
| W01–04 | [Python Tutor / C](https://pythontutor.com/c.html) | 指针、栈/堆、结构体、函数调用 | 不是 Linux 多线程或内核执行器 |
| W03–06、W26 | [Compiler Explorer](https://godbolt.org/) | C ↔ 汇编、不同编译参数 | 不能代替实机性能或驱动调试 |
| W01 预览、W26 | [CPUlator](https://cpulator.01xz.net/) | ARMv7 寄存器与单步指令 | **不是** AArch64，也不是 i.MX6ULL SoC 全功能模拟 |
| W26 选读 | [Ripes](https://ripes.me/) | RISC-V CPU 流水线/缓存概念 | RISC-V 与 ARM 指令集不同 |
| W16–20 | [PulseView / sigrok](https://sigrok.org/wiki/PulseView) | I2C/SPI/UART 数字波形 | 需要对应逻辑分析仪/可用采样数据 |
| W17 预览、W33–34 | [KernelShark](https://kernelshark.org/) | 调度、IRQ、trace 事件时间线 | 桌面软件，需要 trace 数据 |
| W11–20 | [dtc / Device Tree 编译器](https://www.devicetree.org/) | 设备树节点和硬件拓扑 | 不会模拟外设电路 |
| W21–25 | [Mermaid Live](https://mermaid.live/) | V4L2 队列、传感器数据流 | 只绘图，不提供实机采样 |
| W28–32 | [QEMU 官方文档](https://www.qemu.org/docs/master/) + monitor | PCI EDU、MMIO/IRQ/DMA 软件模型 | 不代表真实 PCIe 信号和时序 |

## 最容易使用的三组入门实验

**A：C 指针（W02）**：打开 Python Tutor → 输入链表与指针小程序 → 单步观察变量和地址 → 人为产生悬垂指针 → 本地 ASan 复核。最后以真实错误报告为准。

**B：GPIO / I2C（W16–18）**：画板卡引脚连接 → 原理图和 NXP 参考手册找到对应模块 → PulseView 抓取一次波形 → 故意配置错误 → 分析边沿、地址、ACK。

**C：V4L2（W23）**：在 Mermaid 绘图：§open → REQBUFS → QUERYBUF → mmap → QBUF → STREAMON → DQBUF → QBUF → STREAMOFF§。再去官方 §capture.c§ 查对应 §ioctl§，最后通过真实节点采集或记录硬件限制。

## 不建议做的事情

- 不要在早期投入大量时间画 UI 或训练视觉网络。
- 不要因为 Ripes 好看就把学习主线改成 RISC-V。
- 不要将网页动画表现视为硬件寄存器实测证据。
''')
w('05-学习校验/调试能力贯穿40周.md','''# 调试能力贯穿 40 周：70% 训练重心

> 70% 是你对定位问题重要程度的**目标权重**，不是对所有岗位的统计数据；每周 D6 留出足够时间做可复现实验和根因分析，不增设额外课程负担。

## 六步法：每一个核心实验都能重复使用

1. **现象与复现**：什么硬件、什么版本、什么操作、重复几次、期望/实际。
2. **收集证据**：日志、栈、寄存器值、波形、trace、内核配置、时间戳；标原始文件名。
3. **至少两个互斥假设**：例如时钟/寄存器问题 vs 用户态参数问题。
4. **最小区分实验**：一次只改一个变量；说明为什么这个结果能排除某个假设。
5. **定位根因**：映射回原厂手册寄存器位、内核源码路径、系统调用或硬件信号。
6. **修复与回归**：同条件复测、错误路径复测、明确剩余不确定性。

## 工具按需提前接触

| 区间 | 定位核心 | 建议工具 | 最小证据 |
|---|---|---|---|
| W01–04 | 越界/指针/资源释放 | GDB、ASan、Python Tutor | 错误栈与修复报告 |
| W05–10 | 构建与用户态系统调用 | make -n、nm、readelf、strace、TSan（可用时） | 系统调用/竞态排除链 |
| W11–16 | 启动、模块、DTS、内核错误 | 串口、dmesg、vermagic、dtc、Oops stack | 具体阶段/函数/节点证据 |
| W17–20 | 中断和时序 | PulseView、/proc/interrupts；轻量 tracefs | 波形/IRQ/时间线 |
| W21–25 | 视频数据流断流、帧率 | V4L2 设备信息、单调时钟、帧计数 | 对不同环节独立测量 |
| W26–32 | 异常、BAR、IRQ、DMA | QEMU Monitor、lspci、dmesg、寄存器打印 | 地址/位域/回读证据 |
| W33–40 | 锁、性能、长时间稳定性 | lockdep、ftrace、perf、KernelShark（条件允许） | 根因、性能前后对比、回归 |

## 每周最低交付标准

- 至少一份简短定位卡：现象、证据、假设 A/B、验证结果、根因或阻塞、回归。
- 标出：🟢 实机复现 / 🔵 虚拟平台验证 / ⚪ 源码或文档推断，不能混为一谈。
- 没有找到根因也可阶段性合格，但要说明哪个假设被排除、下一次可验证什么。
- 五道门仍保留，**调试门**不能被“程序运行成功”代替。

详见：[故障报告模板](../07-模板/故障定位报告模板.md)和[技术手册阅读卡](../07-模板/技术手册阅读与故障归因卡.md)。
''')
w('07-模板/技术手册阅读与故障归因卡.md','''# 技术手册阅读与故障归因卡（复制到每周 evidence）

## 原始出处

- 问题/硬件型号/板卡修订：
- 操作系统与内核版本、工具链：
- 原厂手册名称、Revision、章节/页码：
- 原理图页码与引脚：
- 内核源码仓库、分支/commit、路径/函数：
- 选读/可视化材料（辅助，不能替代原始出处）：

## 先直观看懂（≤10 分钟）

- 一句话描述数据流/寄存器/中断：
- 一张简单框图（可用 Mermaid、手绘或波形）：

## 调试六步

1. 现象（期望/实际）与复现条件：
2. 原始证据（文件路径 + 时间）：
3. 假设 A 与 B（为什么可以区分）：
4. 最小验证实验与排除过程：
5. 根因定位（寄存器位/函数/具体信号）：
6. 修复与回归（重复次数、对比数据）：

## 证据成熟度

- [ ] 实机验证
- [ ] QEMU/仿真验证
- [ ] 源码静态分析
- [ ] 官方手册推断
- [ ] 暂未确认

## 最后总结

- 我真正理解的机制：
- 还不了解、以后再深挖的部分：
- 本实验的硬件边界、风险与回滚方案：
''')
# 5. Adjust global guidance and anchors
def main_readme(s):
    s=s.replace('由《芯片底层软件 40 周学习手册（最终版）》拆分整理而成，原文完整保留在','从原《芯片底层软件 40 周学习手册》拆分整理并于 2026-11-17 深化；原文历史快照保留在')
    s=s.replace('## 先看这 3 个文件','## 先看这 4 个文件\n\n0. [新版路线与删减依据](00-总览与规则/新版路线与删减依据.md)：当前学习方向、70% 故障定位重心、官方资料优先与技术边界')
    s=s.replace('| §00-总览与规则/§ | 原手册全文、使用规则、阶段总览 | 只读 |','| §00-总览与规则/§ | 原手册历史全文、新版路线、使用规则、阶段总览 | 历史稿只读 |')
    s=s.replace('| §03-资料链接/§ | 课程与文档总索引、选读池 | 只读 |','| §03-资料链接/§ | 课程索引、原厂资料路线、可视化地图、选读池 | 查询使用 |')
    s=s.replace('| §07-模板/§ | 故障定位报告、hardware-manifest、摄像头档案、技术机制缺口表、STAR 简历、AI 教练提示词、驱动审查清单 | 复制使用 |','| §07-模板/§ | 故障定位报告、硬件清单、技术机制缺口表、原厂文档阅读卡、AI 教练提示词 | 复制使用 |')
    s=s.replace('## 每周怎么用（5 步)','## 每周怎么用（5 步）\n\n每周至少保留一次**现象→证据→假设→验证→根因→回归**训练，优先阅读 [官方资料](03-资料链接/一手资料阅读路线.md)；抽象概念先看 [可视化地图](03-资料链接/可视化学习地图.md)。')
    s += '\n## 版本说明\n\n本文件夹以 2026-11-17 的学习原则为准；原手册保留为只读历史快照。W25/W39 已改为技术复盘与机制深入，40 周计划均有原始出处、可视化和调试挑战。[修订及核验记录](09-维护与修订/本次变更及两轮核验.md)。\n'
    return s
update('README.md',main_readme)
def rules(s):
    s=s.replace('只有岗位需要或硬件到位才升级','只有实际技术问题需要、前置基础具备或硬件到位才升级')
    s=s.replace('notes/Wxx/','04-笔记/Wxx/')
    s += '\n### 现行优先级（2026-11-17）\n\n每周可视化≤15 分钟作为引导；原始手册/官方源码为依据；调试与根因分析是约 70% 的实践重心（不是机械学时配比）。不因为近期求职而限制芯片深度。详见 [修订路线](新版路线与删减依据.md) 和 [故障定位方法](../05-学习校验/调试能力贯穿40周.md)。\n'
    return s
update('00-总览与规则/使用规则.md',rules)
# stage overview and progress specific row labels, and obsolete demo
for rel in ['00-总览与规则/阶段总览.md','01-进度核对/进度总表.md']:
    def change(s):
        s=s.replace('M13 | W25 | 技术机制缺口表 + 展示 C','M13 | W25 | P1/P2 机制缺口表 + 故障报告 + 展示 C')
        s=s.replace('展示 C：P1 + P2 + 技术机制缺口表','展示 C：P1/P2 数据流解释 + 故障定位闭环')
        s=s.replace('W39 | 专项机制深入：三选一','W39 | 专项机制深入：三选一')
        if rel.endswith('阶段总览.md'):
            s+='\n\n> 当前原则：请先阅读 [新版路线](新版路线与删减依据.md)；调试贯穿 40 周，W21–25 V4L2 保持用户态入门，W39 不需要确定长期唯一专项。\n'
        else:
            s+='\n\n## 四、调试训练与官方资料核对（2026-11-17 新增）\n\n每周完成 [六步法](../05-学习校验/调试能力贯穿40周.md) 最小故障卡，出处参照 [一手资料阅读路线](../03-资料链接/一手资料阅读路线.md)。**本表原有 40 周进度状态不预填**。\n'
        return s
    update(rel,change)
# course index and optional pool
update('03-资料链接/课程与文档索引.md',lambda s:s+'''
## 2026-11-17 补充：源头优先与可视化

此表的所有 B 站课程链接继续保留，但属于 **辅助讲解**；遇到外设、驱动、异常、DMA，先读 [原始资料路线](一手资料阅读路线.md)，再看 [可视化学习地图](可视化学习地图.md)，最后找具体视频讲次。

重点工具：[Python Tutor](https://pythontutor.com/c.html)（W01–04）、[Compiler Explorer](https://godbolt.org/)（W03–06/W26）、[CPUlator](https://cpulator.01xz.net/)（ARMv7 概念）、[PulseView](https://sigrok.org/wiki/PulseView)（W16–20）、[KernelShark](https://kernelshark.org/)（W33–34）。NXP 原厂 IMX6ULLRM 可能需登录；任何示例仍须核对**实际内核版本**。
''')
update('03-资料链接/选读池.md',lambda s:s.replace('投 BSP/固件岗再学','需要深入 BSP/固件机制再学').replace('确定岗位需要且有硬件再学','技术问题明确且有硬件再学').replace('NPU demo、RKNN、YOLO（训练不安排）；更多 OpenCV 算法','NPU demo、RKNN、YOLO（训练不安排）；更多 OpenCV 算法。与 Linux 驱动主线无关时不占必学时间')+'\n> **专项原则**：W08–12 不锁定方向，W39 是一次机制深挖而不是岗位选择。参考 [现行路线](../00-总览与规则/新版路线与删减依据.md)。\n')
# Templates
def fault(s):
    s=s.replace('## 现象','## 原始资料来源（必填）\n\n- 原厂手册（名称/修订/章节/页码）或 Linux 官方文档：\n- 实际内核/驱动源码版本与路径：\n- 实机 / QEMU / 仅文档推断（明确标注）：\n\n## 现象')
    s=s.replace('## 修复与回归验证','## 排除链路（为什么不是其他故障）\n\n- 排除的假设与直接证据：\n- 尚不能排除的原因：\n\n## 修复与回归验证')
    s+='\n> 每周调试训练约占实践重点，见 [40 周调试能力路线](../05-学习校验/调试能力贯穿40周.md)。\n'
    return s
update('07-模板/故障定位报告模板.md',fault)
def other(s):
    a=s.find('## 3. ')
    assert a>=0
    return s[:a]+'''## 3. 技术机制缺口表（W25、W39 使用）

> 按理解程度与证据记录，不收集招聘岗位。

§§§markdown
| 机制/子系统 | 官方资料及版本 | 已做的实验 | 仍无法解释的现象 | 下一步验证 | 证据路径 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
§§§

---

## 4. 技术成果证据卡（W40 使用）

> 技术结果按实机、仿真、源码推断严格区分，不把阅读等同于实测。

§§§markdown
### 项目：
- 核心机制与对应原始资料：
- 运行平台/内核版本/源码提交：
- 亲自完成的操作：
- 故障现象及定位根因：
- 数据（帧率/耗时/中断数/稳定时长）：
- 证据路径与局限：
§§§

---
'''
update('07-模板/其他记录模板.md',other)
# Project docs: remove resume-specific heading while preserving project architecture
def projects(s):
    s=s.replace('作品集仓库结构（W40 整理成这个样子再上传）','技术实验仓库结构（W40 整理，可选上传）')
    s=s.replace('resume-evidence.md     # STAR 简历素材','technical-evidence.md  # 原始资料、故障与实验结果')
    s += '\n## 2026-11-17 强化：每个项目至少一条调试闭环\n\n在 README 增加：原始手册/内核源码版本、最小故障复现、假设与排除、根因、回归数据、硬件能力边界。以 [六步定位法](../05-学习校验/调试能力贯穿40周.md) 为验收基础，**P2 不要求开发 V4L2 内核驱动**。\n'
    return s
update('06-项目与代码/四个项目说明.md',projects)
# Every report gets a small consistent diagnosing prompt, existing notes are preserved unchanged
for n in range(1,41):
    f=ROOT/f'04-笔记/W{n:02d}/report.md'
    assert f.exists(),f
    s=f.read_text(encoding='utf-8')
    s+=f'''
## 2026-11-17 新增：本周根因定位卡

- 故障现象与可重复条件：
- 原始资料（手册 Revision/页码或 kernel 源码版本/函数）：
- 证据（日志、波形、寄存器、trace 文件）：
- 假设 A / B 与区分实验：
- 被排除的解释、根因或下一步：
- 修复与回归结果（注明实机 / 仿真 / 推断）：
- 本周定位挑战请看 [W{n:02d} 计划](../../02-每周计划/{week_dirs[n].parent.name}/{week_dirs[n].name})。
'''
    w(f.relative_to(ROOT),s)
# W25/W39/W40 acceptance and review consistency
def checklist(s):
    s=s.replace('验收：明确下一阶段重点（设备控制 / BSP / 芯片系统 / 视觉底层）。','验收：能用原始资料解释 V4L2 用户态采集和实际局限，完成一份可复现的故障报告。')
    s=s.replace('### [W39　专项机制深入：三选一]','### [W39　专项机制深入：三选一]')
    s=s.replace('### [W40　轻量周：作品集与最终展示]','### [W40　轻量周：作品集与最终展示]')
    s=s.replace('验收：干净环境能基本复现；不把"了解"写成"独立交付经验"。','验收：干净环境能基本复现；调试报告有排除证据，区分实机、仿真和文档推断。')
    s+='\n## 全程共同验收（2026-11-17）\n\n每周至少提交一条 [六步故障定位卡](调试能力贯穿40周.md)；标出原始手册/源码版本及证据成熟度，合并到 D6，不额外增加学时。W39 只深挖一次机制，不必提前确定唯一专项。\n'
    return s
update('05-学习校验/每周验收清单.md',checklist)
# all docs that call out the old jobs path or career emphasis check in later audit
w('09-维护与修订/变更原则.md','''# 2026-11-17 变更原则与后续维护

- 历史快照：§00-总览与规则/原手册-完整版.md§ 完全保留。
- 修改前完整备份：§D:\\VMShare\\芯片底层软件40周-修改前备份-20261117§（独立目录）。
- 仅替换 W25/W39/W40 与长期目标冲突的 D 日任务；其余 37 周原有 D1–D6/课程讲次不覆盖，通过周末定位挑战替代重复性练习。
- W01–W40 新增个性化可视化入口、官方资料、调试挑战、减负边界，报告模板增补根因记录。
- 不修改笔记中已产生的原始记录或项目代码。
- 40 周和 M1–M21 保持不变，P1–P4 名称与实验主线保留。
- 学历、近期招聘、简历等不作为当前学习决策因素。特殊历史材料仍可在备份和完整原手册中找到。
- 每次更新需通过：40 周唯一性、40 个笔记/周报、关键 Markdown 相对链接、历史手册 SHA256、核心知识点、调试练习证据校验。
''')
# Case: stage pages may contain legacy "岗位" passages, detected later.
print(json.dumps({'result':'updated','week_files':len(week_dirs),'backup':str(BACKUP),'new_docs':7},ensure_ascii=False))
