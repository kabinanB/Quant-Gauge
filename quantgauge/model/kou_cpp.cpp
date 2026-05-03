#include <pybind11/pybind11.h>

namespace py = pybind11;

#include <cmath>
#include <iostream>
#include <map>
#include <functional>
#include <limits>
#include <utility>
using namespace std;

const double pi = 3.14159265358979323846;

// couldn't compile with just double
inline double Phi(double x)
{
    const double SQRT_TWO = 1.4142135623730950488016887242097;
    return 1.0 - 0.5 * erfc(x / SQRT_TWO);
}

struct Results
{
	double price;
	double error;
	double delta;
	double delta_error;
	double gamma;
	double gamma_error;
	double vega;
	double vega_error;
};

class Option
{
public:
	Option(double T) : m_T(T) {}


protected:
	const double m_T;
	double risingFactorial(double a, double k) const;
	double confluentHyperGeometric(double a, double b, double x) const;
	double HhFunction(int n, double x) const;
	double In(int n, double c, double alpha, double beta, double delta) const;
	double Upsilon(double mu, double sigma, double lambda, double p, double eta1, double eta2, double a, double T, int count) const;
	double P(int n, int k, double eta1, double eta2, double p) const;
	double Q(int n, int k, double eta1, double eta2, double p) const;

};







double nCk(double n, double k) {
    if (k < 0 || k > n) return 0.0;
    return tgamma(n + 1) / (tgamma(k + 1) * tgamma(n - k + 1));
}




double Option::risingFactorial(double a, double k) const {
    return tgamma(a + k) / tgamma(a);
}

double Option::confluentHyperGeometric(double a, double b, double z) const
{
    double sum = 0;
    for (int k = 0; k < 15; ++k)
    {
        const double ak = risingFactorial(a, k);
        const double bk = risingFactorial(b, k);
        const double zk = pow(z, k);
        const double k_fact = tgamma(k + 1);
        sum += (ak / bk) * (zk / k_fact);
    }
    return sum;
}

double Option::HhFunction(int n, double x) const {
    if (n < -1) return 0.0;
    if (n == -1) return exp(-0.5 * x * x);
    if (n == 0) return sqrt(2.0 * pi) * Phi(-x);

    return (HhFunction(n - 2, x) - x * HhFunction(n - 1, x)) / n;
}

double Option::In(int n, double c, double alpha, double beta, double delta) const
{
    if (beta > 0 && alpha != 0) {
        double suma = 0.0;
        for (int i = 0; i <= n; ++i) {
            suma += pow(beta / alpha, n - i) * HhFunction(i, beta * c - delta);
        }
        double T1 = -(exp(alpha * c) / alpha) * suma;
        double exponent = (alpha * delta) / beta + (alpha * alpha) / (2 * beta * beta);
        double cdf = -beta * c + delta + alpha / beta;
        double T2 = pow(beta / alpha, n + 1) * (sqrt(2 * pi) / beta) * exp(exponent) * Phi(cdf);
        return T1 + T2;
    }
    else if (beta < 0 && alpha < 0) {
        double suma = 0.0;
        for (int i = 0; i <= n; ++i) {
            suma += pow(beta / alpha, n - i) * HhFunction(i, beta * c - delta);
        }
        double T1 = -(exp(alpha * c) / alpha) * suma;
        double exponent = (alpha * delta) / beta + (alpha * alpha) / (2 * beta * beta);
        double cdf = beta * c - delta - alpha / beta;
        double T2 = pow(beta / alpha, n + 1) * (sqrt(2 * pi) / beta) * exp(exponent) * Phi(cdf);
        return T1 - T2;
    }
    else {
        return 0.0;
    }
}
double Option::P(int n, int k, double eta1, double eta2, double p) const
{
    double q = 1 - p;
    double sum = 0;
    if (k == n) return pow(p, n);

    for (int i = k; i <= n - 1; ++i) {
        const double T1 = nCk(n - k - 1, i - k);
        const double T2 = nCk(n, i);
        const double T3 = pow(eta1 / (eta1 + eta2), i - k);
        const double T4 = pow(eta2 / (eta1 + eta2), n - i);
        const double T5 = pow(p, i) * pow(q, n - i);
        sum += T1 * T2 * T3 * T4 * T5;
    }
    return sum;
}


double Option::Q(int n, int k, double eta1, double eta2, double p) const
{
    double q = 1 - p;
    double sum = 0;
    if (k == n) return pow(q, n);

    for (int i = k; i <= n - 1; ++i) {
        const double T1 = nCk(n - k - 1, i - k);
        const double T2 = nCk(n, i);
        const double T3 = pow(eta1 / (eta1 + eta2), n - i);
        const double T4 = pow(eta2 / (eta1 + eta2), i - k);
        const double T5 = pow(q, i) * pow(p, n - i);
        sum += T1 * T2 * T3 * T4 * T5;
    }
    return sum;
}



double Option::Upsilon(double mu, double sigma, double lambda, double p, double eta1, double eta2, double a, double T, int count) const {
    //
    // Goal is to estimate anlytical solution in 15 decimal places and estimate how many counts until it converges
    // change it to long double, for more accuracy?
    //
    //const int count = 10; //European call option price under Kou Jump Diffusion is: 9.147317303895392, analytical solution elapsed time : 0.000491400000000 s
    //let's try count higher!
    //const int count = 15; //it works! European call option price under Kou Jump Diffusion is: 9.147317303936937, analytical solution elapsed time : 0.001211400000000 s
    //little bit more higher!
    //const int count = 20; // it works! European call option price under Kou Jump Diffusion is: 9.147317303936937, analytical solution elapsed time : 0.007024300000000 s
    //little more!
    //At the moment i could use count as 25.
    /*const int count = 25;*/ //it works! European call option price under Kou Jump Diffusion is: 9.147317303936937, analytical solution elapsed time : 0.065775100000000 s
    //const int count = 35; // it works but slower! European call option price under Kou Jump Diffusion is: 9.147317303936937, analytical solution elapsed time : 7.061756500000000 s
    //const int count = 40; //much slower! European call option price under Kou Jump Diffusion is: 9.14732, analytical solution elapsed time : 81.4449 s
    //it looks like as count increases the run time gets much slower meaning i should incorporate CUDA
    double pi0 = exp(-lambda * T);

    double sum1 = 0.0;
    double sum2 = 0.0;

    for (int n = 1; n <= count; ++n) {
        double sum3 = 0.0;
        double sum4 = 0.0;

        double pi_n = exp(-lambda * T) * std::pow(lambda * T, n) / tgamma(n + 1);

        for (int k = 1; k <= n; ++k) {

            double P1 = P(n, k, eta1, eta2, p);
            P1 *= std::pow(sigma * std::sqrt(T) * eta1, k);
            P1 *= In(k - 1, a - mu * T, -eta1, -1.0 / (sigma * sqrt(T)), -sigma * eta1 * sqrt(T));
            sum3 += P1;


            double Q1 = Q(n, k, eta1, eta2, p);
            Q1 *= std::pow(sigma * std::sqrt(T) * eta2, k);
            Q1 *= In(k - 1, a - mu * T, eta2, 1.0 / (sigma * sqrt(T)), -sigma * eta2 * sqrt(T));
            sum4 += Q1;
        }
        sum1 += pi_n * sum3;
        sum2 += pi_n * sum4;
    }


    double T1 = exp(pow(sigma * eta1, 2) * T / 2) / (sigma * sqrt(2 * pi * T)) * sum1;
    double T2 = exp(pow(sigma * eta2, 2) * T / 2) / (sigma * sqrt(2 * pi * T)) * sum2;
    double T3 = pi0 * Phi(-(a - mu * T) / (sigma * sqrt(T)));

    return T1 + T2 + T3;
}

struct Resultsdr
{
	double price;
	double error;
	double delta;

};

class EuropeanOption : public Option
{
public:
	EuropeanOption(double T, double K) : Option(T), m_K(K){}
	virtual double priceByKouJumpDiffusion(double S0, double r, double sigma, double lambda, double p, double eta1, double eta2, int count) const = 0;
protected:
	const double m_K;

};


class EuropeanCall : public EuropeanOption
{
public:
	EuropeanCall(double T, double K) : EuropeanOption(T,K){}
	double priceByKouJumpDiffusion(double S0, double r, double sigma, double lambda, double p, double eta1, double eta2, int count) const;
};

class EuropeanPut : public EuropeanOption
{
public:
	EuropeanPut(double T, double K) : EuropeanOption(T,K) {}
	double priceByKouJumpDiffusion(double S0, double r, double sigma, double lambda, double p, double eta1, double eta2, int count) const;



};



double EuropeanCall::priceByKouJumpDiffusion(double S0, double r, double sigma,
    double lambda, double p,
    double eta1, double eta2, int count) const
{
    const double q = 1 - p;
    const double zeta = (p * eta1) / (eta1 - 1) + (q * eta2) / (eta2 + 1) - 1;
    const double lambda_tilda = lambda * (zeta + 1);
    const double p_tilda = (p / (1 + zeta)) * (eta1 / (eta1 - 1));
    const double nu1_tilda = eta1 - 1;
    const double nu2_tilda = eta2 + 1;

    const double logKS = log(m_K / S0);

    double mu1 = r + 0.5 * sigma * sigma - lambda * zeta;
    double U1 = Upsilon(mu1, sigma, lambda_tilda, p_tilda, nu1_tilda, nu2_tilda, logKS, m_T,count);
    double T1 = S0 * U1;

    double mu2 = r - 0.5 * sigma * sigma - lambda * zeta;
    double U2 = Upsilon(mu2, sigma, lambda, p, eta1, eta2, logKS, m_T, count);
    double T2 = m_K * exp(-r * m_T) * U2;

    return T1 - T2;
}


double EuropeanPut::priceByKouJumpDiffusion(double S0, double r, double sigma, double lambda, double p, double eta1, double eta2, int count) const
{
    EuropeanCall c(m_T, m_K);

    return c.priceByKouJumpDiffusion(S0, r, sigma, lambda, p, eta1, eta2, count) + m_K * exp(-r * m_T) - S0;
}


std::unique_ptr<EuropeanCall> create_european_call(double T, double K) {
    return std::make_unique<EuropeanCall>(T, K);
}

std::unique_ptr<EuropeanPut> create_european_put(double T, double K) {
    return std::make_unique<EuropeanPut>(T, K);
}


// --- 2. The Module Registration ---
PYBIND11_MODULE(kou_cpp, m) {
    // Register the Base
    py::class_<Option>(m, "Option");

    // Register the Intermediate (Abstract) class
    // THIS IS WHERE WE LINK THE PRICE FUNCTION
    py::class_<EuropeanOption, Option>(m, "EuropeanOption")
        .def("priceByKouJumpDiffusion", &EuropeanOption::priceByKouJumpDiffusion,
             py::arg("S"), py::arg("r"), py::arg("sigma"),
             py::arg("lam"), py::arg("p"), py::arg("eta1"), py::arg("eta2"),
             py::arg("n"));

    // Register the Concrete Child
    py::class_<EuropeanCall, EuropeanOption>(m, "KouEuropeanCall")
        .def(py::init<double, double>());

    // Register the Concrete Child for Put
    py::class_<EuropeanPut, EuropeanOption>(m, "KouEuropeanPut")
        .def(py::init<double, double>());

    // REGISTER THE FACTORY SO PYTHON CAN CALL IT
    m.def("create_european_call", &create_european_call, py::arg("T"), py::arg("K"));
    m.def("create_european_put", &create_european_put, py::arg("T"), py::arg("K"));
}