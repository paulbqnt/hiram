# CMakeList.txt : CMake project for hiram, include source and define
# project specific logic here.
#

# Add source to this project's executable.
# add_executable (hiram   "MarketData.hpp" "MarketData.cpp" "main.cpp" "PayoffCall.cpp" "PayoffPut.cpp" "EuropeanOption.cpp" "Option.cpp")

# Automatically find all .cpp files in the current directory and subdirectories
file(GLOB_RECURSE SOURCES CONFIGURE_DEPENDS "*.cpp")

# Add the executable and link all source files
add_executable(hiram ${SOURCES} "BlackScholesModel.cpp")


if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET hiram PROPERTY CXX_STANDARD 20)
endif()

# TODO: Add tests and install targets if needed.
