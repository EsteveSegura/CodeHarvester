cmake_minimum_required(VERSION 3.10)
project(CodeHarvester)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Boost REQUIRED COMPONENTS program_options filesystem)

include_directories(include)

add_executable(CodeHarvester 
    src/main.cpp
    src/OptionsHandler.cpp
    src/CodeHarvester.cpp
    src/FileProcessor.cpp
    src/DirectoryProcessor.cpp
)

target_link_libraries(CodeHarvester PRIVATE Boost::program_options Boost::filesystem)
