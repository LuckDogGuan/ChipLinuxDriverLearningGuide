# W35　C++17 / CMake 工程化

> 阶段 E　调试与交付（W33–W40）　｜　小阶段 M19
> [← 课程目录](../../README.md) · [笔记](../../04-笔记/W35/note.md) · [周报](../../04-笔记/W35/report.md) · [代码](../../code/w35/) · [进度](../../01-进度核对/进度总表.md)
> 标签：✅ 必学　🔧 动手必做（留证据）　⏩ 可快进　⭐ 选读　🟡 条件必学　📝 笔记


| 日 | 任务 | 课程 / 资料 |
|---|---|---|
| D1 | ✅ RAII、`unique_ptr`、包装 C API | [cppreference](https://en.cppreference.com/w/cpp.html) |
| D2 | ✅ CMake target、include、link、install | [CMake 教程](https://cmake.org/cmake/help/latest/guide/tutorial/index.html) |
| D3 | ✅ CLI 参数、JSON 配置、日志等级、返回码 | — |
| D4 | 🔧 为 `camdiag` 拆出 capture/process/metrics 接口，加 CTest 测试 | — |
| D5 | ⭐ 模板元编程、Qt 深入、RPC 框架（现阶段用不到） | — |
| D6 | 🔧 `camdiag v2`：无 GUI 可批量运行，输出 JSON/CSV，不依赖绝对路径 | — |

☐D1 ☐D2 ☐D3 ☐D4 ☐D6

实验截图、日志、波形可按需放在 [evidence/](../../04-笔记/W35/evidence/)；无需额外填写记录表。

## 深化与故障定位

> 与上面的 D1–D6 课程配套，**替换**部分重复观看或练习，不额外增加固定学习时间；每周调试训练用 [六步定位法](../../05-学习校验/调试能力贯穿40周.md) 记录。70% 是训练重心，不是机械划分学时。

- **先看可视化（5–10 分钟）**：Compiler Explorer: https://godbolt.org/；先直观理解现象，不追求一次精通。
- **再看一手资料（优先查相关一节）**：CMake 官方教程: https://cmake.org/cmake/help/latest/guide/tutorial/。记录实际版本/章节/关键函数或寄存器；[原始资料阅读方法](../../03-资料链接/一手资料阅读路线.md)。
- **本周定位挑战（🔧 与 D6 实验合并）**：修改编译参数触发接口/ABI 问题，收集构建证据。提交现象、两个假设、排除证据、根因/尚未知、回归结果。
- **减负与边界**：C++ 复习缩减，聚焦测试/资源管理。任何硬件特性先以手册、实机配置和日志为准，失败可交阻塞报告。
- **可视化工具总表**：[可视化学习地图](../../03-资料链接/可视化学习地图.md)；报告见 [故障定位报告模板](../../07-模板/故障定位报告模板.md)。
