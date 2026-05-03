#include <pybind11/pybind11.h>

namespace py = pybind11;


#include <iostream>
#include <vector>
#include <fstream>
#include <iomanip>
#include <sstream>
using namespace std;

double Phi(double x)
{
	const double SQRT_TWO = 1.4142135623730950488016887242097;
	return 1.0 - 0.5 * erfc(x / SQRT_TWO);
}

double factorial(int n)
{
	if (n == 0 || n == 1)
	{
		return 1;
	}
	return n * factorial(n - 1);
}


class EuropeanCall
{
public:
	EuropeanCall(double K, double T) :m_K(K), m_T(T){}
	double BSAnalyticalPrice(double S0, double sigma, double r) const
	{
		const double d_plus = (log(S0 / m_K) + (r + sigma * sigma / 2.0) * m_T) / sigma / sqrt(m_T);
		const double d_minus = d_plus - sigma * sqrt(m_T);
		return S0 * Phi(d_plus) - m_K * exp(-r * m_T) * Phi(d_minus);
	}
	double JDAnalyticalPrice(double S0, double sigma, double r, double lambda, double m, double s, double n) const;
private:
	const double m_T;
	const double m_K;

};

double EuropeanCall::JDAnalyticalPrice(double S0, double sigma, double r, double lambda, double m, double s, double n) const
{
	const double k = exp(m + pow(s, 2) * 0.5) - 1;
	const double lambda_dsh = lambda * (1 + k);

	const double C1 = lambda_dsh * m_T;
	const double r1 = r - lambda * k;
	const double r2 = log(1 + k) / m_T;
	const double s1 = sigma * sigma;
	const double s2 = pow(s, 2) / m_T;
	double sum = 0.0;
	for (int i = 0; i <= n; ++i)
	{
		double sigma_n = sqrt(s1 + s2 * i);
		double r_n = r1 + i * r2;
		sum += ((exp(-C1) * pow(C1, i)) / factorial(i)) * BSAnalyticalPrice(S0, sigma_n, r_n);

	}

	return sum;
}


// --- 2. The Module Registration ---
PYBIND11_MODULE(merton_cpp, m) {
    // Register the Base
    py::class_<EuropeanCall>(m, "EuropeanCall").def(py::init<double, double>())
                                               .def("JDAnalyticalPrice", &EuropeanCall::JDAnalyticalPrice,
                                               py::arg("S"), py::arg("sigma"), py::arg("r"),
                                               py::arg("lam"), py::arg("m"), py::arg("s"), py::arg("n"));
}



