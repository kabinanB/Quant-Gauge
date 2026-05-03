cmake_minimum_required(VERSION 3.15) # 3.15+ is highly recommended for modern Python discovery
project(quantgauge LANGUAGES CXX)

# 1. Use the modern FindPython module.
# Development.Module is specifically for creating .so/.pyd files.
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

# 2. Simplified pybind11 discovery.
# scikit-build-core and cibuildwheel provide pybind11 in a way that
# find_package(pybind11) can usually find it automatically.
find_package(pybind11 REQUIRED)

# 3. Build the modules using the standard pybind11 function
pybind11_add_module(merton_cpp "quantgauge/model/merton_cpp.cpp")
pybind11_add_module(kou_cpp "quantgauge/model/kou_cpp.cpp")

# 4. Handle Output Directories.
# We remove the hardcoded local paths for the CI/CD build.
# scikit-build-core will handle moving these into the right place for the wheel.
if(NOT SKBUILD)
    set_target_properties(merton_cpp kou_cpp PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/quantgauge/model"
        LIBRARY_OUTPUT_DIRECTORY_RELEASE "${CMAKE_CURRENT_SOURCE_DIR}/quantgauge/model"
    )
endif()

# 5. Standard Install (Required for wheels)
install(TARGETS merton_cpp kou_cpp LIBRARY DESTINATION model)