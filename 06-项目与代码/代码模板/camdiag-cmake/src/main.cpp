// camdiag 骨架（W22 起步，W24 v1，W35 v2）
// 构建：cmake -B build && cmake --build build
// 运行：./build/camdiag --buildinfo   查看 OpenCV 的 Video I/O 后端（有没有 FFMPEG / GStreamer）
#include <opencv2/core.hpp>
#include <iostream>
#include <string>

int main(int argc, char** argv)
{
    std::cout << "OpenCV " << CV_VERSION << "\n";

    if (argc > 1 && std::string(argv[1]) == "--buildinfo") {
        std::cout << cv::getBuildInformation() << "\n";
        return 0;
    }

    // TODO(W22 D6) 解析参数：--source <file|rtsp>  --frames N  --out dir
    // TODO 用 cv::VideoCapture 打开源；打不开要打印原因并返回非 0
    // TODO 循环取 N 帧：统计帧数、分辨率、通道数；用 std::chrono::steady_clock 计算平均 FPS
    //      （不要用 CAP_PROP_FPS 当真实帧率）
    // TODO 对两帧做 threshold / Canny，用 cv::imwrite 存到 --out 目录
    // TODO(W24) 每帧带时间戳写 CSV；有界队列 + 丢帧计数
    return 0;
}
