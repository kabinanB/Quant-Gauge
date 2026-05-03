#include <pybind11/pybind11.h>

namespace py = pybind11;

// Your existing functions
int func1(int i, int j) {
    return i + j;
}

double func2(double d) {
    return d * d;
}

// The pybind11 module definition
PYBIND11_MODULE(example, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    // Expose func1 as example.func1
    m.def("func1", &func1, "A function that adds two integers");

    // Expose func2 as example.func2
    m.def("func2", &func2, "A function that squares a double");
}