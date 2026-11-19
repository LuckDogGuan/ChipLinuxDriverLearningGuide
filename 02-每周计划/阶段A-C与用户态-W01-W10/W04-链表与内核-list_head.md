# W04　链表与内核 list_head

> 阶段 A　C 与 Linux 用户态（W01–W10）　｜　小阶段 M2
> [← 课程目录](../../README.md) · [笔记](../../04-笔记/W04/note.md) · [周报](../../04-笔记/W04/report.md) · [代码](../../code/w04/) · [进度](../../01-进度核对/进度总表.md)
> 标签：✅ 必学　🔧 动手必做（留证据）　⏩ 可快进　⭐ 选读　🟡 条件必学　📝 笔记


| 日 | 任务 | 课程 / 资料 |
|---|---|---|
| D1 | ✅ 单向链表（先自己写再对照） | [C P77（24′）](https://www.bilibili.com/video/BV18p4y167Md?p=77)　[P78（23′）](https://www.bilibili.com/video/BV18p4y167Md?p=78) |
| D2 | ✅ 双向链表，留意悬垂指针 | [C P87（22′）](https://www.bilibili.com/video/BV18p4y167Md?p=87)　[P88（25′）](https://www.bilibili.com/video/BV18p4y167Md?p=88) |
| D3 | ✅ 内核双向链表赏析（重点） | [C P94（26′）](https://www.bilibili.com/video/BV18p4y167Md?p=94)　[P95（23′）](https://www.bilibili.com/video/BV18p4y167Md?p=95) |
| D4 | ✅ `container_of` 原理；GDB 看节点内存 | [内核 list 文档](https://docs.kernel.org/core-api/list.html) |
| D5 | ⭐ 单链表其余、双链表其余 | [C P79–P86](https://www.bilibili.com/video/BV18p4y167Md?p=79)　[P89–P93](https://www.bilibili.com/video/BV18p4y167Md?p=89) |
| D6 | 🔧 迷你 `list_head` + `container_of`，4 种错误测试；1 页图解 | — |

验收：能从成员指针推出外层结构体。 ☐D1 ☐D2 ☐D3 ☐D4 ☐D6

实验截图、日志、波形可按需放在 [evidence/](../../04-笔记/W04/evidence/)；无需额外填写记录表。

## 深化与故障定位

> 与上面的 D1–D6 课程配套，**替换**部分重复观看或练习，不额外增加固定学习时间；每周调试训练用 [六步定位法](../../05-学习校验/调试能力贯穿40周.md) 记录。70% 是训练重心，不是机械划分学时。

- **先看可视化（5–10 分钟）**：Python Tutor: https://pythontutor.com/c.html；先直观理解现象，不追求一次精通。
- **再看一手资料（优先查相关一节）**：Kernel linked list: https://docs.kernel.org/core-api/list.html。记录实际版本/章节/关键函数或寄存器；[原始资料阅读方法](../../03-资料链接/一手资料阅读路线.md)。
- **本周定位挑战（🔧 与 D6 实验合并）**：删除链表节点后错误遍历，定位无效地址。提交现象、两个假设、排除证据、根因/尚未知、回归结果。
- **减负与边界**：单链表重复课程可快进。任何硬件特性先以手册、实机配置和日志为准，失败可交阻塞报告。
- **可视化工具总表**：[可视化学习地图](../../03-资料链接/可视化学习地图.md)；报告见 [故障定位报告模板](../../07-模板/故障定位报告模板.md)。
