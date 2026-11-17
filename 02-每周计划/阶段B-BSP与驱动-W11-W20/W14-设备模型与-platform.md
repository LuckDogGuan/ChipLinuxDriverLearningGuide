# W14　设备模型与 platform

> 阶段 B　BSP 与驱动（W11–W20）　｜　小阶段 M7
> 笔记：[04-笔记/W14/note.md](../../04-笔记/W14/note.md)　｜　周报：[report.md](../../04-笔记/W14/report.md)　｜　[进度总表](../../01-进度核对/进度总表.md)
> 标签：✅ 必学　🔧 动手必做（留证据）　⏩ 可快进　⭐ 选读　🟡 条件必学　📝 笔记


目标：能讲清设备与驱动怎么匹配，不用深钻 kobject 源码。

| 日 | 任务 | 课程 / 资料 |
|---|---|---|
| D1 | ✅ 设备驱动模型（kobject 只听框架）、platform 总线 | [Y4 P12 第100讲（18′）](https://www.bilibili.com/video/BV1pf4y1974n?p=12)　[P20 第108讲（10′）](https://www.bilibili.com/video/BV1pf4y1974n?p=20)　[P21 第109讲（12′）](https://www.bilibili.com/video/BV1pf4y1974n?p=21) |
| D2 | ✅ 驱动的分离与分层；驱动、总线和设备 | [Z4 P53 第16.1讲（23′）](https://www.bilibili.com/video/BV1fJ411i7PB?p=53)　[P54 第16.2讲（33′）](https://www.bilibili.com/video/BV1fJ411i7PB?p=54) |
| D3 | ✅ platform 总线简介 | [Z4 P55 第16.3讲（31′）](https://www.bilibili.com/video/BV1fJ411i7PB?p=55)　[P56 第16.4讲（20′）](https://www.bilibili.com/video/BV1fJ411i7PB?p=56) |
| D4 | ✅ 无设备树 platform 设备实验（当作机制示例）；观察 probe 时机 | [Z4 P57 第16.5讲（32′）](https://www.bilibili.com/video/BV1fJ411i7PB?p=57)　[内核驱动模型](https://docs.kernel.org/driver-api/driver-model/index.html) |
| D5 | ⭐ kobject/kset/uevent/class/自建总线 | [Y4 P13–P19](https://www.bilibili.com/video/BV1pf4y1974n?p=13) |
| D6 | 🔧 platform 驱动 + 故障注入（让 probe 失败），写资源释放日志 | — |

验收：能画出"设备出现→匹配→probe→创建设备节点"。 ☐D1 ☐D2 ☐D3 ☐D4 ☐D6

## 本周交付清单

- [ ] 每日 3 行笔记 → `04-笔记/W14/note.md`
- [ ] 实验代码 → `04-笔记/W14/code/`
- [ ] 截图 / 日志 / 波形 → `04-笔记/W14/evidence/`
- [ ] 周报 5 项 → `04-笔记/W14/report.md`
- [ ] 在 [进度总表](../../01-进度核对/进度总表.md) 把本周改成 ✅

用到的模板：[07-模板](../../07-模板/)　｜　卡住了：[常见阻塞与替代](../../08-设备与问题排查/常见阻塞与替代.md)


## 本周深化与定位挑战（2026-11-17 修订）

> 与上面的 D1–D6 课程配套，**替换**部分重复观看或练习，不额外增加固定学习时间；每周调试训练用 [六步定位法](../../05-学习校验/调试能力贯穿40周.md) 记录。70% 是训练重心，不是机械划分学时。

- **先看可视化（5–10 分钟）**：画 sysfs 的 bus→device→driver 匹配关系；先直观理解现象，不追求一次精通。
- **再看一手资料（优先查相关一节）**：Linux driver model: https://docs.kernel.org/driver-api/driver-model/overview.html。记录实际版本/章节/关键函数或寄存器；[原始资料阅读方法](../../03-资料链接/一手资料阅读路线.md)。
- **本周定位挑战（🔧 与 D6 实验合并）**：设备树 compatible 看似正确却不 probe，记录排查树。提交现象、两个假设、排除证据、根因/尚未知、回归结果。
- **减负与边界**：kobject 内部源码留选读。任何硬件特性先以手册、实机配置和日志为准，失败可交阻塞报告。
- **可视化工具总表**：[可视化学习地图](../../03-资料链接/可视化学习地图.md)；报告见 [故障定位报告模板](../../07-模板/故障定位报告模板.md)。
