# W07　文件 I/O 与设备文件

> 阶段 A　C 与 Linux 用户态（W01–W10）　｜　小阶段 M4
> 笔记：[04-笔记/W07/note.md](../../04-笔记/W07/note.md)　｜　周报：[report.md](../../04-笔记/W07/report.md)　｜　[代码](../../04-笔记/W07/code/)　｜　[进度总表](../../01-进度核对/进度总表.md)
> 标签：✅ 必学　🔧 动手必做（留证据）　⏩ 可快进　⭐ 选读　🟡 条件必学　📝 笔记


| 日 | 任务 | 课程 / 资料 |
|---|---|---|
| D1 | ⏩ 标准 IO：fopen/fclose（先自测，熟就倍速） | [C P124 介绍（17′）](https://www.bilibili.com/video/BV18p4y167Md?p=124)　[P125 fopen1（14′）](https://www.bilibili.com/video/BV18p4y167Md?p=125)　[P126 fopen2（21′）](https://www.bilibili.com/video/BV18p4y167Md?p=126) |
| D2 | ✅ 文件描述符实现原理、open/close | [C P135（29′）](https://www.bilibili.com/video/BV18p4y167Md?p=135)　[P136（23′）](https://www.bilibili.com/video/BV18p4y167Md?p=136) |
| D3 | ✅ read/write/lseek 与 mycopy；系统 IO vs 标准 IO；fcntl/ioctl | [C P137（20′）](https://www.bilibili.com/video/BV18p4y167Md?p=137)　[P138（21′）](https://www.bilibili.com/video/BV18p4y167Md?p=138)　[P141（18′）](https://www.bilibili.com/video/BV18p4y167Md?p=141) |
| D4 | ✅ 文件共享、dup/dup2 | [C P139（23′）](https://www.bilibili.com/video/BV18p4y167Md?p=139)　[P140（27′）](https://www.bilibili.com/video/BV18p4y167Md?p=140) |
| D5 | ⭐ 标准 IO 其余、文件系统 | [C P127–P134](https://www.bilibili.com/video/BV18p4y167Md?p=127)　[P142–P148](https://www.bilibili.com/video/BV18p4y167Md?p=142) |
| D6 | 🔧 带错误处理与耗时统计的 `mycopy`，对比 stdio 与系统调用；在板上按 Y1 的方法操作一个已有 LED 节点（GPIO sysfs 是旧接口，只用来理解老做法） | [Y1 P46（第45讲 LED）](https://www.bilibili.com/video/BV1JK4y1t7io?p=46)　[P47](https://www.bilibili.com/video/BV1JK4y1t7io?p=47)　[P48](https://www.bilibili.com/video/BV1JK4y1t7io?p=48)　[GPIO sysfs 弃用说明](https://docs.kernel.org/admin-guide/gpio/sysfs.html) |

验收：能解释文件描述符生命周期、ioctl 的适用场景。 ☐D1 ☐D2 ☐D3 ☐D4 ☐D6

## 本周记录：笔记 · 周报 · 代码

- [ ] [笔记](../../04-笔记/W07/note.md)
- [ ] [周报](../../04-笔记/W07/report.md)
- [ ] [代码](../../04-笔记/W07/code/)

截图、日志、波形可按需放入 `../../04-笔记/W07/evidence/`；[进度总表](../../01-进度核对/进度总表.md)只作可选总览。


## 本周深化与定位挑战（2026-11-17 修订）

> 与上面的 D1–D6 课程配套，**替换**部分重复观看或练习，不额外增加固定学习时间；每周调试训练用 [六步定位法](../../05-学习校验/调试能力贯穿40周.md) 记录。70% 是训练重心，不是机械划分学时。

- **先看可视化（5–10 分钟）**：strace 调用时间线（本地工具）；先直观理解现象，不追求一次精通。
- **再看一手资料（优先查相关一节）**：Linux man-pages open(2): https://man7.org/linux/man-pages/man2/open.2.html。记录实际版本/章节/关键函数或寄存器；[原始资料阅读方法](../../03-资料链接/一手资料阅读路线.md)。
- **本周定位挑战（🔧 与 D6 实验合并）**：open 成功但 read 返回 EBADF，利用 strace 与 errno 找原因。提交现象、两个假设、排除证据、根因/尚未知、回归结果。
- **减负与边界**：熟悉的 stdio 可快进。任何硬件特性先以手册、实机配置和日志为准，失败可交阻塞报告。
- **可视化工具总表**：[可视化学习地图](../../03-资料链接/可视化学习地图.md)；报告见 [故障定位报告模板](../../07-模板/故障定位报告模板.md)。
