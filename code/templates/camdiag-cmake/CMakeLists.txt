cmake_minimum_required(VERSION 3.16)
project(camdiag LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenCV REQUIRED COMPONENTS core imgproc imgcodecs videoio)

add_executable(camdiag src/main.cpp)
target_link_libraries(camdiag PRIVATE ${OpenCV_LIBS})
