cmake_minimum_required(VERSION 3.11)
project(MyProject)

set(CMAKE_CXX_STANDARD 14)

include(FetchContent)
FetchContent_Declare(
  prometheus_cpp
  GIT_REPOSITORY https://github.com/jupp0r/prometheus-cpp.git
  GIT_TAG        v0.12.3 # adjust this to the version you want
)
FetchContent_MakeAvailable(prometheus_cpp)

add_executable(MyProject main.cpp)

target_link_libraries(MyProject PRIVATE prometheus-cpp::core prometheus-cpp::pull)
