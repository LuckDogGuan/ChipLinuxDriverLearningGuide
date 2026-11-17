# W01　环境、数据表示、GDB 起步

> 阶段 A　C 与 Linux 用户态（W01–W10）　｜　小阶段 M1
> 笔记：[04-笔记/W01/note.md](../../04-笔记/W01/note.md)　｜　周报：[report.md](../../04-笔记/W01/report.md)　｜　[进度总表](../../01-进度核对/进度总表.md)
> 标签：✅ 必学　🔧 动手必做（留证据）　⏩ 可快进　⭐ 选读　🟡 条件必学　📝 笔记


目标：能编译、单步、解释二进制与位运算。

| 日 | 任务 | 课程 / 资料 |
|---|---|---|
| D1 | ✅ 装 gcc/gdb/make；`gcc -g -O0` 编译运行 | [C P2 gcc 与 vim（28′）](https://www.bilibili.com/video/BV18p4y167Md?p=2)　[C P3 编程注意问题1（20′）](https://www.bilibili.com/video/BV18p4y167Md?p=3) |
| D2 | ✅ 数据类型、补码，十六进制核对 | [C P5 二进制及数值类型存储（27′）](https://www.bilibili.com/video/BV18p4y167Md?p=5)　[C P6 bool、char、0（28′）](https://www.bilibili.com/video/BV18p4y167Md?p=6) |
| D3 | ✅ 位运算与掩码 | [C P13 关系/逻辑/位/赋值/条件/sizeof（20′）](https://www.bilibili.com/video/BV18p4y167Md?p=13)　[C P14 位运算的重要意义（29′）](https://www.bilibili.com/video/BV18p4y167Md?p=14) |
| D4 | ✅ GDB：break/next/step/bt/watch/`x/16xb` | [GDB 官方文档 Sample Session](https://sourceware.org/gdb/documentation/)，让 AI 带练 |
| D5 | ⭐ 学习方法、编程注意问题2、常量变量 static/extern | [C P1](https://www.bilibili.com/video/BV18p4y167Md?p=1)　[C P4](https://www.bilibili.com/video/BV18p4y167Md?p=4)　[C P7–P11](https://www.bilibili.com/video/BV18p4y167Md?p=7) |
| D6 | 🔧 `bitops`：SET/CLR/TOGGLE/取字段，5 个测试；故意引入一个 bug，用 GDB 定位并截图 | — |

验收：能解释一段寄存器位掩码代码，有断点截图。 ☐D1 ☐D2 ☐D3 ☐D4 ☐D6

## 本周交付清单

- [ ] 每日 3 行笔记 → `04-笔记/W01/note.md`
- [ ] 实验代码 → `04-笔记/W01/code/`
- [ ] 截图 / 日志 / 波形 → `04-笔记/W01/evidence/`
- [ ] 周报 5 项 → `04-笔记/W01/report.md`
- [ ] 在 [进度总表](../../01-进度核对/进度总表.md) 把本周改成 ✅

用到的模板：[07-模板](../../07-模板/)　｜　卡住了：[常见阻塞与替代](../../08-设备与问题排查/常见阻塞与替代.md)


## 本周深化与定位挑战（2026-11-17 修订）

> 与上面的 D1–D6 课程配套，**替换**部分重复观看或练习，不额外增加固定学习时间；每周调试训练用 [六步定位法](../../05-学习校验/调试能力贯穿40周.md) 记录。70% 是训练重心，不是机械划分学时。

- **先看可视化（5–10 分钟）**：Python Tutor: https://pythontutor.com/c.html；先直观理解现象，不追求一次精通。
- **再看一手资料（优先查相关一节）**：GDB: https://sourceware.org/gdb/documentation/。记录实际版本/章节/关键函数或寄存器；[原始资料阅读方法](../../03-资料链接/一手资料阅读路线.md)。
- **本周定位挑战（🔧 与 D6 实验合并）**：某个寄存器掩码只改动一位，为什么读回值不对？。提交现象、两个假设、排除证据、根因/尚未知、回归结果。
- **减负与边界**：位运算不熟才补课；熟悉的变量语法快进。任何硬件特性先以手册、实机配置和日志为准，失败可交阻塞报告。
- **可视化工具总表**：[可视化学习地图](../../03-资料链接/可视化学习地图.md)；报告见 [故障定位报告模板](../../07-模板/故障定位报告模板.md)。
