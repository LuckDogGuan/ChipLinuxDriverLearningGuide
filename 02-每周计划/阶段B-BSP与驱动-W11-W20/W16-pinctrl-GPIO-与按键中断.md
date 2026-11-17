# W16　pinctrl、GPIO 与按键中断

> 阶段 B　BSP 与驱动（W11–W20）　｜　小阶段 M8
> 笔记：[04-笔记/W16/note.md](../../04-笔记/W16/note.md)　｜　周报：[report.md](../../04-笔记/W16/report.md)　｜　[进度总表](../../01-进度核对/进度总表.md)
> 标签：✅ 必学　🔧 动手必做（留证据）　⏩ 可快进　⭐ 选读　🟡 条件必学　📝 笔记


| 日 | 任务 | 课程 / 资料 |
|---|---|---|
| D1 | ✅ pinctrl 概念与引脚设置接口（内部实现不用啃） | [Y4 P28 第116讲（16′）](https://www.bilibili.com/video/BV1pf4y1974n?p=28)　[P40 第128讲（15′）](https://www.bilibili.com/video/BV1pf4y1974n?p=40)　[P41 第129讲（14′）](https://www.bilibili.com/video/BV1pf4y1974n?p=41) |
| D2 | ✅ GPIO 子系统，`gpiod_*` 写法 | [Y4 P42 第130讲（14′）](https://www.bilibili.com/video/BV1pf4y1974n?p=42)　[P43 第131讲（17′）](https://www.bilibili.com/video/BV1pf4y1974n?p=43)　[内核 GPIO 文档](https://docs.kernel.org/driver-api/gpio/index.html) |
| D3 | ✅ Linux 中断基础与按键中断实验 | [Y4 P70 第158讲（14′）](https://www.bilibili.com/video/BV1pf4y1974n?p=70)　[P71 第159讲（21′）](https://www.bilibili.com/video/BV1pf4y1974n?p=71) |
| D4 | ✅ 工作队列与按键消抖；中断里不能睡眠 | [Y4 P74 第162讲（14′）](https://www.bilibili.com/video/BV1pf4y1974n?p=74)　[Z4 P46 第13.6讲 定时器消抖（32′）](https://www.bilibili.com/video/BV1fJ411i7PB?p=46) |
| D5 | ⭐ pinctrl 内部映射；tasklet（旧用法，新代码优先 workqueue/threaded IRQ） | [Y4 P29–P39](https://www.bilibili.com/video/BV1pf4y1974n?p=29)　[Y4 P72–P73](https://www.bilibili.com/video/BV1pf4y1974n?p=72) |
| D6 | 🔧 按键 + LED 驱动，统计触发次数与消抖效果；有逻辑分析仪就抓波形（**硬件三问 #2**） | — |

验收：能说出中断里哪些事不能做；能说明 GPIO sysfs 是旧接口。 ☐D1 ☐D2 ☐D3 ☐D4 ☐D6

## 本周交付清单

- [ ] 每日 3 行笔记 → `04-笔记/W16/note.md`
- [ ] 实验代码 → `04-笔记/W16/code/`
- [ ] 截图 / 日志 / 波形 → `04-笔记/W16/evidence/`
- [ ] 周报 5 项 → `04-笔记/W16/report.md`
- [ ] 在 [进度总表](../../01-进度核对/进度总表.md) 把本周改成 ✅

用到的模板：[07-模板](../../07-模板/)　｜　卡住了：[常见阻塞与替代](../../08-设备与问题排查/常见阻塞与替代.md)


## 本周深化与定位挑战（2026-11-17 修订）

> 与上面的 D1–D6 课程配套，**替换**部分重复观看或练习，不额外增加固定学习时间；每周调试训练用 [六步定位法](../../05-学习校验/调试能力贯穿40周.md) 记录。70% 是训练重心，不是机械划分学时。

- **先看可视化（5–10 分钟）**：PulseView 波形 / GPIO 中断时间线；先直观理解现象，不追求一次精通。
- **再看一手资料（优先查相关一节）**：GPIO API: https://docs.kernel.org/driver-api/gpio/index.html。记录实际版本/章节/关键函数或寄存器；[原始资料阅读方法](../../03-资料链接/一手资料阅读路线.md)。
- **本周定位挑战（🔧 与 D6 实验合并）**：按键连续触发异常，区分机械抖动/中断配置/软件逻辑。提交现象、两个假设、排除证据、根因/尚未知、回归结果。
- **减负与边界**：pinctrl 内部实现维持选读。任何硬件特性先以手册、实机配置和日志为准，失败可交阻塞报告。
- **可视化工具总表**：[可视化学习地图](../../03-资料链接/可视化学习地图.md)；报告见 [故障定位报告模板](../../07-模板/故障定位报告模板.md)。
