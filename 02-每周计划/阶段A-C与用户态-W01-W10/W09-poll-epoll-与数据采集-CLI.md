# W09　poll / epoll 与数据采集 CLI

> 阶段 A　C 与 Linux 用户态（W01–W10）　｜　小阶段 M5
> [← 课程目录](../../README.md) · [笔记](../../04-笔记/W09/note.md) · [周报](../../04-笔记/W09/report.md) · [代码](../../code/w09/) · [进度](../../01-进度核对/进度总表.md)
> 标签：✅ 必学　🔧 动手必做（留证据）　⏩ 可快进　⭐ 选读　🟡 条件必学　📝 笔记


| 日 | 任务 | 课程 / 资料 |
|---|---|---|
| D1 | ✅ 数据中继原理、有限状态机编程 | [C P220（26′）](https://www.bilibili.com/video/BV18p4y167Md?p=220)　[P221（25′）](https://www.bilibili.com/video/BV18p4y167Md?p=221) |
| D2 | ✅ select 与 poll | [C P226 select（19′）](https://www.bilibili.com/video/BV18p4y167Md?p=226)　[P228 poll 实例（22′）](https://www.bilibili.com/video/BV18p4y167Md?p=228) |
| D3 | ✅ epoll、内存映射 | [C P229（33′）](https://www.bilibili.com/video/BV18p4y167Md?p=229)　[P230（15′）](https://www.bilibili.com/video/BV18p4y167Md?p=230) |
| D4 | 🔧 设计 `sensor-logger`：数据源→poll→线程缓冲→CSV；先写设计说明和骨架 | `man 2 poll` |
| D5 | ⭐ select 实例、内存映射实例 | [C P227](https://www.bilibili.com/video/BV18p4y167Md?p=227)　[P231](https://www.bilibili.com/video/BV18p4y167Md?p=231) |
| D6 | 🔧 完成 `sensor-logger`（模拟数据或真实串口），含 Ctrl+C 退出与拔设备测试 | — |

验收：有端到端运行记录。 ☐D1 ☐D2 ☐D3 ☐D4 ☐D6

实验截图、日志、波形可按需放在 [evidence/](../../04-笔记/W09/evidence/)；无需额外填写记录表。

## 深化与故障定位

> 与上面的 D1–D6 课程配套，**替换**部分重复观看或练习，不额外增加固定学习时间；每周调试训练用 [六步定位法](../../05-学习校验/调试能力贯穿40周.md) 记录。70% 是训练重心，不是机械划分学时。

- **先看可视化（5–10 分钟）**：画状态机与 epoll 事件时间线；先直观理解现象，不追求一次精通。
- **再看一手资料（优先查相关一节）**：epoll(7): https://man7.org/linux/man-pages/man7/epoll.7.html。记录实际版本/章节/关键函数或寄存器；[原始资料阅读方法](../../03-资料链接/一手资料阅读路线.md)。
- **本周定位挑战（🔧 与 D6 实验合并）**：故意制造设备断连后卡住，追踪 poll 返回值。提交现象、两个假设、排除证据、根因/尚未知、回归结果。
- **减负与边界**：不要扩展成网络服务器课程。任何硬件特性先以手册、实机配置和日志为准，失败可交阻塞报告。
- **可视化工具总表**：[可视化学习地图](../../03-资料链接/可视化学习地图.md)；报告见 [故障定位报告模板](../../07-模板/故障定位报告模板.md)。
