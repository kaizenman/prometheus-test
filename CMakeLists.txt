cmake_minimum_required(VERSION 3.14)  # for FetchContent

project(cpp_prometheus)

set(CMAKE_CXX_STANDARD 14)

# Locate Boost libraries: context, coroutine, and system
set(Boost_USE_STATIC_LIBS OFF)
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME OFF)
find_package(Boost 1.65.1 REQUIRED COMPONENTS system)

include_directories(${Boost_INCLUDE_DIRS})

# Include nlohmann_json via FetchContent
include(FetchContent)
FetchContent_Declare(
  json
  GIT_REPOSITORY https://github.com/nlohmann/json.git
  GIT_TAG v3.10.4
)
FetchContent_MakeAvailable(json)

add_executable(cpp_prometheus main.cpp)

# Link Boost libraries to the new target
target_link_libraries(cpp_prometheus ${Boost_LIBRARIES} nlohmann_json::nlohmann_json)
