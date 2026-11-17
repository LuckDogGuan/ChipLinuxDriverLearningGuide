# W05　轻量周：Makefile

> 阶段 A　C 与 Linux 用户态（W01–W10）　｜　小阶段 M3
> 笔记：[04-笔记/W05/note.md](../../04-笔记/W05/note.md)　｜　周报：[report.md](../../04-笔记/W05/report.md)　｜　[进度总表](../../01-进度核对/进度总表.md)
> 标签：✅ 必学　🔧 动手必做（留证据）　⏩ 可快进　⭐ 选读　🟡 条件必学　📝 笔记


| 日 | 任务 | 课程 / 资料 |
|---|---|---|
| D1 | ✅ Makefile 简介、三要素、管理项目 | [Y1 P31（第30讲 13′）](https://www.bilibili.com/video/BV1JK4y1t7io?p=31)　[P32（11′）](https://www.bilibili.com/video/BV1JK4y1t7io?p=32)　[P33（9′）](https://www.bilibili.com/video/BV1JK4y1t7io?p=33) |
| D2 | ✅ Makefile 变量、模式规则、条件分支 | [Y1 P34（第33讲 20′）](https://www.bilibili.com/video/BV1JK4y1t7io?p=34)　[P35（8′）](https://www.bilibili.com/video/BV1JK4y1t7io?p=35)　[P36（7′）](https://www.bilibili.com/video/BV1JK4y1t7io?p=36) |
| D3 | ✅ 把 W01–W04 代码整理成带 Makefile 的小仓库 | [C P70 Makefile 工程文件编写规则（29′）](https://www.bilibili.com/video/BV18p4y167Md?p=70) |
| D4 | 🔧 可选彩蛋（≤60′，失败就记录后跳过）：按文档用 RTSP 在 VLC 里看 30 秒相机画面 | [Waveshare ISG1321](https://www.waveshare.com/wiki/ISG1321_Camera)　[Luckfox CSI 教程](https://wiki.luckfox.com/zh/Luckfox-Pico-Zero/CSI-Camera/) |
| D5 | ⭐ Makefile 常用函数、头文件依赖 | [Y1 P37（第36讲 26′）](https://www.bilibili.com/video/BV1JK4y1t7io?p=37)　[P38（第37讲 11′）](https://www.bilibili.com/video/BV1JK4y1t7io?p=38) |
| D6 | 🔧 交一个 `Makefile`/`build.sh` 仓库 + 一页《指针与内存》总结（可选：相机预览截图） | — |

验收：Makefile 可重复构建。 ☐D1 ☐D2 ☐D3 ☐D6

## 本周交付清单

- [ ] 每日 3 行笔记 → `04-笔记/W05/note.md`
- [ ] 实验代码 → `04-笔记/W05/code/`
- [ ] 截图 / 日志 / 波形 → `04-笔记/W05/evidence/`
- [ ] 周报 5 项 → `04-笔记/W05/report.md`
- [ ] 在 [进度总表](../../01-进度核对/进度总表.md) 把本周改成 ✅

用到的模板：[07-模板](../../07-模板/)　｜　卡住了：[常见阻塞与替代](../../08-设备与问题排查/常见阻塞与替代.md)


## 本周深化与定位挑战（2026-11-17 修订）

> 与上面的 D1–D6 课程配套，**替换**部分重复观看或练习，不额外增加固定学习时间；每周调试训练用 [六步定位法](../../05-学习校验/调试能力贯穿40周.md) 记录。70% 是训练重心，不是机械划分学时。

- **先看可视化（5–10 分钟）**：Make 干跑命令 make -n；先直观理解现象，不追求一次精通。
- **再看一手资料（优先查相关一节）**：GNU Make 官方手册: https://www.gnu.org/software/make/manual/。记录实际版本/章节/关键函数或寄存器；[原始资料阅读方法](../../03-资料链接/一手资料阅读路线.md)。
- **本周定位挑战（🔧 与 D6 实验合并）**：改头文件后可执行文件没有重建，定位依赖缺失。提交现象、两个假设、排除证据、根因/尚未知、回归结果。
- **减负与边界**：make 只学依赖、变量、规则与排错。任何硬件特性先以手册、实机配置和日志为准，失败可交阻塞报告。
- **可视化工具总表**：[可视化学习地图](../../03-资料链接/可视化学习地图.md)；报告见 [故障定位报告模板](../../07-模板/故障定位报告模板.md)。
