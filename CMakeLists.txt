cmake_minimum_required(VERSION 3.29)
project(hiram)

set(CMAKE_CXX_STANDARD 23)

add_executable(
        hiram hiram/main.cpp
        hiram/Derivative.cpp
        hiram/MarketData.cpp
)
