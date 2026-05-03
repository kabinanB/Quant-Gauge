cmake_minimum_required(VERSION 3.12)
project(quantgauge)

find_package(Python REQUIRED COMPONENTS Interpreter Development)

execute_process(
    COMMAND "${Python_EXECUTABLE}" -m pybind11 --cmakedir
    OUTPUT_VARIABLE pybind11_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

find_package(pybind11 REQUIRED PATHS "${pybind11_DIR}" NO_DEFAULT_PATH)

# Build all three modules
pybind11_add_module(merton_cpp "quantgauge/model/merton_cpp.cpp")
pybind11_add_module(kou_cpp "quantgauge/model/kou_cpp.cpp")

# Set output directory to quantgauge/model (not a Release subfolder)
set_target_properties(merton_cpp kou_cpp PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/quantgauge/model"
    LIBRARY_OUTPUT_DIRECTORY_RELEASE "${CMAKE_CURRENT_SOURCE_DIR}/quantgauge/model"
    LIBRARY_OUTPUT_DIRECTORY_DEBUG "${CMAKE_CURRENT_SOURCE_DIR}/quantgauge/model"
)

# Install to the same location
install(TARGETS merton_cpp kou_cpp
    LIBRARY DESTINATION "${CMAKE_CURRENT_SOURCE_DIR}/quantgauge/model"
    RUNTIME DESTINATION "${CMAKE_CURRENT_SOURCE_DIR}/quantgauge/model"
)