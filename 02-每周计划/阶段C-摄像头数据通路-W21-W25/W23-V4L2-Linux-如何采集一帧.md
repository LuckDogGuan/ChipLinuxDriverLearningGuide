# W23　V4L2：Linux 如何采集一帧

> 阶段 C　摄像头数据通路（W21–W25）　｜　小阶段 M12
> [← 课程目录](../../README.md) · [笔记](../../04-笔记/W23/note.md) · [周报](../../04-笔记/W23/report.md) · [代码](../../04-笔记/W23/code/) · [进度](../../01-进度核对/进度总表.md)
> 标签：✅ 必学　🔧 动手必做（留证据）　⏩ 可快进　⭐ 选读　🟡 条件必学　📝 笔记


| 日 | 任务 | 课程 / 资料 |
|---|---|---|
| D1 | ✅ V4L2 设备模型；`QUERYCAP`、`ENUM_FMT`、`S_FMT` | [capture.c 示例](https://docs.kernel.org/userspace-api/media/v4l/capture.c.html) |
| D2 | ✅ 流式采集：`REQBUFS`→`QUERYBUF`→`mmap`→`QBUF`/`DQBUF`→`STREAMON`；画流程图 | [mmap 文档](https://docs.kernel.org/userspace-api/media/v4l/mmap.html) |
| D3 | ✅ 像素格式与帧大小：YUYV、NV12、MJPEG（压缩帧不定长）、灰度/原始格式 | [V4L2 文档](https://docs.kernel.org/userspace-api/media/v4l/) |
| D4 | 🔧 选一条能走通的路：**①**官方页面说明 V4L2 拿到的是未经 ISP 的原始图，且需先停掉 rkipc（`RkLunch-stop.sh`），在 Luckfox 上用 SDK 工具链交叉编译采集程序，看 `ENUM_FMT` 返回什么格式；**②**PC 上用 UVC 摄像头（虚拟机需 USB 透传）；**③**内核自带的 `vivid` 虚拟视频驱动（部分发行版有，`modprobe vivid`，没有就跳过）；**④**都不行就只读代码、画图，不虚构实测 | [Waveshare ISG1321](https://www.waveshare.com/wiki/ISG1321_Camera) |
| D5 | ⭐ media-controller、vb2 驱动内部 | — |
| D6 | 🔧 `v4l2cap.c`：采 N 帧存盘，打印格式与每帧字节数；或交一张流程图 + 官方示例的逐行注释 | — |

验收：能说明"RTSP 不是 V4L2 设备，V4L2 是内核采集接口"。 ☐D1 ☐D2 ☐D3 ☐D4 ☐D6

实验截图、日志、波形可按需放在 [evidence/](../../04-笔记/W23/evidence/)；无需额外填写记录表。

## 深化与故障定位

> 与上面的 D1–D6 课程配套，**替换**部分重复观看或练习，不额外增加固定学习时间；每周调试训练用 [六步定位法](../../05-学习校验/调试能力贯穿40周.md) 记录。70% 是训练重心，不是机械划分学时。

- **先看可视化（5–10 分钟）**：V4L2 QBUF/DQBUF 队列状态图；先直观理解现象，不追求一次精通。
- **再看一手资料（优先查相关一节）**：V4L2 mmap: https://docs.kernel.org/userspace-api/media/v4l/mmap.html。记录实际版本/章节/关键函数或寄存器；[原始资料阅读方法](../../03-资料链接/一手资料阅读路线.md)。
- **本周定位挑战（🔧 与 D6 实验合并）**：REQBUFS/S_FMT 参数错误返回 EINVAL，从 ioctl 逐个验证。提交现象、两个假设、排除证据、根因/尚未知、回归结果。
- **减负与边界**：只到用户态接口，不要求 Sensor 内核驱动。任何硬件特性先以手册、实机配置和日志为准，失败可交阻塞报告。
- **可视化工具总表**：[可视化学习地图](../../03-资料链接/可视化学习地图.md)；报告见 [故障定位报告模板](../../07-模板/故障定位报告模板.md)。
