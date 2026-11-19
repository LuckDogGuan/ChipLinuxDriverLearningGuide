# W34　日志、ftrace 与 perf

> 阶段 E　调试与交付（W33–W40）　｜　小阶段 M18
> [← 课程目录](../../README.md) · [笔记](../../04-笔记/W34/note.md) · [周报](../../04-笔记/W34/report.md) · [代码](../../code/w34/) · [进度](../../01-进度核对/进度总表.md)
> 标签：✅ 必学　🔧 动手必做（留证据）　⏩ 可快进　⭐ 选读　🟡 条件必学　📝 笔记


| 日 | 任务 | 课程 / 资料 |
|---|---|---|
| D1 | ✅ dmesg、dynamic debug、tracepoint | [Bootlin 文档](https://bootlin.com/docs/) |
| D2 | ✅ `ftrace`/`trace-cmd` 的 function_graph | [内核 tracing](https://docs.kernel.org/trace/index.html) |
| D3 | ✅ `perf stat/record/report` 与其限制 | [perf wiki](https://perf.wiki.kernel.org/index.php/Main_Page)　[perf 示例](https://www.brendangregg.com/perf.html) |
| D4 | 🔧 对 EDU DMA 或 `camdiag` 做一次 CPU/系统调用热点测量 | — |
| D5 | ⭐ eBPF/bpftrace（不要求写程序） | — |
| D6 | 🔧 《性能证据》：工具版本、场景、命令、原始输出、解释；区分吞吐、延迟、CPU 占用 | — |

☐D1 ☐D2 ☐D3 ☐D4 ☐D6

实验截图、日志、波形可按需放在 [evidence/](../../04-笔记/W34/evidence/)；无需额外填写记录表。

## 深化与故障定位

> 与上面的 D1–D6 课程配套，**替换**部分重复观看或练习，不额外增加固定学习时间；每周调试训练用 [六步定位法](../../05-学习校验/调试能力贯穿40周.md) 记录。70% 是训练重心，不是机械划分学时。

- **先看可视化（5–10 分钟）**：KernelShark: https://kernelshark.org/；先直观理解现象，不追求一次精通。
- **再看一手资料（优先查相关一节）**：Kernel tracing: https://docs.kernel.org/trace/index.html。记录实际版本/章节/关键函数或寄存器；[原始资料阅读方法](../../03-资料链接/一手资料阅读路线.md)。
- **本周定位挑战（🔧 与 D6 实验合并）**：由 trace 找出一次异常延迟/CPU 热点并量化。提交现象、两个假设、排除证据、根因/尚未知、回归结果。
- **减负与边界**：perf/ftrace 保持性能与故障两条实验线。任何硬件特性先以手册、实机配置和日志为准，失败可交阻塞报告。
- **可视化工具总表**：[可视化学习地图](../../03-资料链接/可视化学习地图.md)；报告见 [故障定位报告模板](../../07-模板/故障定位报告模板.md)。
