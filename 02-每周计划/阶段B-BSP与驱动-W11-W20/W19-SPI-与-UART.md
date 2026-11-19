# W19　SPI 与 UART

> 阶段 B　BSP 与驱动（W11–W20）　｜　小阶段 M10
> [← 课程目录](../../README.md) · [笔记](../../04-笔记/W19/note.md) · [周报](../../04-笔记/W19/report.md) · [代码](../../code/w19/) · [进度](../../01-进度核对/进度总表.md)
> 标签：✅ 必学　🔧 动手必做（留证据）　⏩ 可快进　⭐ 选读　🟡 条件必学　📝 笔记


| 日 | 任务 | 课程 / 资料 |
|---|---|---|
| D1 | ✅ SPI 物理总线、驱动框架（CPOL/CPHA/CS） | [Y4 P62 第150讲（10′）](https://www.bilibili.com/video/BV1pf4y1974n?p=62)　[P63 第151讲（22′）](https://www.bilibili.com/video/BV1pf4y1974n?p=63) |
| D2 | ✅ spidev"万能"驱动 | [Y4 P66 第154讲（14′）](https://www.bilibili.com/video/BV1pf4y1974n?p=66)　[P67 第155讲（15′）](https://www.bilibili.com/video/BV1pf4y1974n?p=67) |
| D3 | ✅ SPI 驱动实验；UART 驱动框架 | [Y4 P68 第156讲（17′）](https://www.bilibili.com/video/BV1pf4y1974n?p=68)　[P69 第157讲（14′）](https://www.bilibili.com/video/BV1pf4y1974n?p=69)　[Z4 P88 第24.1讲（34′）](https://www.bilibili.com/video/BV1fJ411i7PB?p=88) |
| D4 | ✅ UART 使能与 `termios` 读写、超时（minicom 移植不用学） | [Z4 P89 第24.2讲（12′）](https://www.bilibili.com/video/BV1fJ411i7PB?p=89) |
| D5 | ⭐ SPI 控制器内部；片选更正；input/触摸屏 | [Z4 P81–P82](https://www.bilibili.com/video/BV1fJ411i7PB?p=81)　[P87](https://www.bilibili.com/video/BV1fJ411i7PB?p=87)　[Y4 P75–P79](https://www.bilibili.com/video/BV1pf4y1974n?p=75) |
| D6 | 🔧 UART 回环 + SPI 一项实验（读 ID，没有器件就做回环）；抓波形算波特率/核对 CPOL/CPHA（**硬件三问 #5**） | — |

验收：串口收发无乱码；SPI 有波形或明确的模拟证据。 ☐D1 ☐D2 ☐D3 ☐D4 ☐D6

实验截图、日志、波形可按需放在 [evidence/](../../04-笔记/W19/evidence/)；无需额外填写记录表。

## 深化与故障定位

> 与上面的 D1–D6 课程配套，**替换**部分重复观看或练习，不额外增加固定学习时间；每周调试训练用 [六步定位法](../../05-学习校验/调试能力贯穿40周.md) 记录。70% 是训练重心，不是机械划分学时。

- **先看可视化（5–10 分钟）**：PulseView SPI 波形 / UART 帧；先直观理解现象，不追求一次精通。
- **再看一手资料（优先查相关一节）**：Linux SPI API: https://docs.kernel.org/spi/spi-summary.html。记录实际版本/章节/关键函数或寄存器；[原始资料阅读方法](../../03-资料链接/一手资料阅读路线.md)。
- **本周定位挑战（🔧 与 D6 实验合并）**：SPI 读 ID 错位，验证 CPOL/CPHA/CS 而非猜测。提交现象、两个假设、排除证据、根因/尚未知、回归结果。
- **减负与边界**：UART 上位机交互不扩展成 UI 项目。任何硬件特性先以手册、实机配置和日志为准，失败可交阻塞报告。
- **可视化工具总表**：[可视化学习地图](../../03-资料链接/可视化学习地图.md)；报告见 [故障定位报告模板](../../07-模板/故障定位报告模板.md)。
