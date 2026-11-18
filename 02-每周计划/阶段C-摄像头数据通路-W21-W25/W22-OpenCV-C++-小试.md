# W22　OpenCV C++ 小试

> 阶段 C　摄像头数据通路（W21–W25）　｜　小阶段 M11
> 笔记：[04-笔记/W22/note.md](../../04-笔记/W22/note.md)　｜　周报：[report.md](../../04-笔记/W22/report.md)　｜　[代码](../../04-笔记/W22/code/)　｜　[进度总表](../../01-进度核对/进度总表.md)
> 标签：✅ 必学　🔧 动手必做（留证据）　⏩ 可快进　⭐ 选读　🟡 条件必学　📝 笔记


只学 5 个 API：`VideoCapture`、`Mat`、`imwrite`、`threshold`/`Canny`、`calcHist`。

| 日 | 任务 | 课程 / 资料 |
|---|---|---|
| D1 | ✅ 配置 C++17 + CMake + OpenCV；先用本地视频文件验证 | [OpenCV 文档](https://docs.opencv.org/4.x/)　[CMake 教程](https://cmake.org/cmake/help/latest/guide/tutorial/index.html) |
| D2 | ✅ `VideoCapture` 取帧、`Mat` 的尺寸/通道/stride；`imwrite` 保存 | OpenCV Video I/O 示例（WSL2 没有 imshow 就只写文件） |
| D3 | ✅ 阈值与 `Canny`；`calcHist` 看亮度分布 | OpenCV imgproc 文档 |
| D4 | 🔧 RTSP 源：`VideoCapture` 能否打开取决于你的 OpenCV 是否带 FFmpeg/GStreamer 后端，VLC 能放不代表 OpenCV 能打开；打不开就记录后用文件源 | — |
| D5 | ⭐ ROI、形态学；YOLO/NPU **这个阶段不学** | — |
| D6 | 🔧 `camdiag v0`：`--source <file|rtsp>`、`--frames N`、`--out dir`；输出帧数、分辨率、平均 FPS，保存两张处理图 | — |

验收：能讲清一帧的尺寸、通道、字节数。 ☐D1 ☐D2 ☐D3 ☐D4 ☐D6

## 本周记录：笔记 · 周报 · 代码

- [ ] [笔记](../../04-笔记/W22/note.md)
- [ ] [周报](../../04-笔记/W22/report.md)
- [ ] [代码](../../04-笔记/W22/code/)

截图、日志、波形可按需放入 `../../04-笔记/W22/evidence/`；[进度总表](../../01-进度核对/进度总表.md)只作可选总览。


## 本周深化与定位挑战（2026-11-17 修订）

> 与上面的 D1–D6 课程配套，**替换**部分重复观看或练习，不额外增加固定学习时间；每周调试训练用 [六步定位法](../../05-学习校验/调试能力贯穿40周.md) 记录。70% 是训练重心，不是机械划分学时。

- **先看可视化（5–10 分钟）**：OpenCV Mat 结构尺寸与 stride 表；先直观理解现象，不追求一次精通。
- **再看一手资料（优先查相关一节）**：OpenCV 官方: https://docs.opencv.org/4.x/。记录实际版本/章节/关键函数或寄存器；[原始资料阅读方法](../../03-资料链接/一手资料阅读路线.md)。
- **本周定位挑战（🔧 与 D6 实验合并）**：图像出现花屏或行错位，核对 stride/format/width。提交现象、两个假设、排除证据、根因/尚未知、回归结果。
- **减负与边界**：只保留已有的少量 OpenCV API，不扩展模型训练。任何硬件特性先以手册、实机配置和日志为准，失败可交阻塞报告。
- **可视化工具总表**：[可视化学习地图](../../03-资料链接/可视化学习地图.md)；报告见 [故障定位报告模板](../../07-模板/故障定位报告模板.md)。
