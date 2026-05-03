cmake_minimum_required(VERSION 3.12)
project(example_project)

find_package(Python REQUIRED COMPONENTS Interpreter Development)

# Use --cmakedir instead of --cmake
execute_process(
    COMMAND "${Python_EXECUTABLE}" -m pybind11 --cmakedir
    OUTPUT_VARIABLE pybind11_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

find_package(pybind11 REQUIRED PATHS "${pybind11_DIR}" NO_DEFAULT_PATH)

# Point to the specific subdirectory
pybind11_add_module(kou_cpp "${CMAKE_CURRENT_SOURCE_DIR}/quantmary/model/kou_cpp.cpp")
pybind11_add_module(merton_cpp "${CMAKE_CURRENT_SOURCE_DIR}/quantmary/model/merton_cpp.cpp")

install(TARGETS kou_cpp
    LIBRARY DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/quantmary/model
    RUNTIME DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/quantmary/model
)

install(TARGETS merton_cpp
    LIBRARY DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/quantmary/model
    RUNTIME DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/quantmary/model
)