<img width="1717" height="916" alt="Image May 4, 2026, 01_06_50 PM" src="https://github.com/user-attachments/assets/4e078637-4bc9-4d22-8cfc-d09995f5bcf4" />


![Python Version](https://img.shields.io/badge/python-%3E%3D3.9-blue)
![CMake](https://img.shields.io/badge/CMake-%3E%3D3.15-brightgreen)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Ubuntu%20%7C%20macOS-lightgrey)

# QuantGauge (DEMO LIBRARY)

A high-performance Python library for derivative pricing using C++.

## Quick Start

To install the library, simply run:
```bash
!pip install quantgauge
```
If you are using Google Colab, you can paste this command into a code cell in a new [notebook](https://colab.research.google.com/).

---

## Usage Example of Option Pricing Model

This module implements three option pricing models: Black-Scholes (BS), Merton Jump-Diffusion, and the Kou Double Exponential Jump-Diffusion model. While many other models exist, this module currently focuses on theoretical pricing for European Call and Put options across these three frameworks.

Future updates could expand the library to include various option types and stochastic models, such as:

**Specialized Option Types**
- Binary Options: Options with fixed payouts based on whether a condition is met.
- Barrier Options: Path-dependent options that activate or deactivate if the underlying price hits a specific level.
- Asian Options: Options where the payoff depends on the average price of the underlying asset over a period.
- American Options: Options that can be exercised at any point before the expiration date.

**Advanced Quantitative Models**
- Stochastic Volatility Models: The Heston Model or the Stochastic Volatility with Jumps (SVJ) model.
- Term-Structure Models: Interest rate models such as Hull-White or Vasicek.
- Black-76: Specifically for pricing options on futures or forward contracts.

### Black-Scholes Model

```python
import quantgauge as qg

# Define option parameters
s = 100.0      # Spot price
k = 105.0      # Strike price
t = 1.0        # Time to maturity (years)
r = 0.05       # Risk-free rate
sigma = 0.15   # Volatility

option = qg.option.blackscholes(
        type_name="ECall",
        s=s, sigma=sigma, r=r, k=k, t=t
)

price = option.price() # price = 6.0355636711334455
```

### Merton Jump-Diffusion Model

Price a European call option using the Merton Jump-Diffusion model:

```python
import quantgauge as qg

# Define option parameters
s = 100.0      # Spot price
k = 105.0      # Strike price
t = 1.0        # Time to maturity (years)
r = 0.05       # Risk-free rate
sigma = 0.15   # Volatility

# Jump-diffusion parameters
lam = 1.0      # Jump intensity
m = 0.05       # Mean of log jump size
s_2 = 0.30     # Volatility of log jump size
n = 10         # Number of terms in series

# Calculate option price
option = qg.option.merton(
    type_name="ECall",
    s=s, sigma=sigma, r=r, k=k, t=t,
    lam=lam, m=m, s_2=s_2, n=n
)

price = option.price()
print(f"Merton Call Price: {price:.4f}") # Merton Call Price: 13.1094
```

### Kou's Double Exponential Jump-Diffusion Model

Price options using Kou's asymmetric jump model:

```python
import quantgauge as qg

# Option parameters
s = 100.0      # Spot price
k = 108.0      # Strike price
t = 1.0        # Time to maturity
r = 0.05       # Risk-free rate
sigma = 0.2    # Volatility

# Kou jump-diffusion parameters
lam = 1.0      # Jump intensity
p = 0.5        # Probability of up jump
eta1 = 20.0    # Up jump decay rate
eta2 = 30.0    # Down jump decay rate
count = 10     # Number of terms in series

# Calculate option price
option = qg.option.kou(
    type_name="ECall",
    s=s, sigma=sigma, r=r, k=k, t=t,
    lam=lam, p=p, eta1=eta1, eta2=eta2, count=count
)

price = option.price()
print(f"Kou Call Price: {price:.4f}") # Kou Call Price: 7.1370
```
---
## Usage Example of Implied Volatility Smile Model

Beyond option pricing, I have implemented implied volatility models such as SVI and SABR to calibrate and analyze the volatility smile.

**SVI Model (Stochastic Volatility Inspired)**

The SVI model, developed by Jim Gatheral, is a popular parametric formulation used to fit the implied volatility smile at a single expiration (a vertical slice of the surface).
- The Math: It maps the total implied variance $w(k, t)$ against the log-strike $k$.
- Key Parameters: It typically uses five parameters ($a, b, \rho, m, \sigma$) to control the level, orientation, and curvature of the smile.
- Strength: SVI is highly flexible and is guaranteed to be free of static arbitrage (like "butterfly arbitrage") if calibrated correctly. It is the industry standard for equity index volatility surfaces.

**SABR Model (Stochastic, Alpha, Beta, Rho)**

The SABR model is a dynamic model that describes how the forward price $F$ and its volatility $\alpha$ evolve over time. It is widely used in interest rate derivatives (swaps and swaptions).
- The Concept: It assumes the volatility of an asset is itself a stochastic process.The Four Parameters:
    - $\alpha$ (Alpha): The initial volatility level.
    - $\beta$ (Beta): The "leverage" parameter (determines the relationship between price and volatility).
    - $\rho$ (Rho): The correlation between the asset price and its volatility.
    - $\nu$ (Nu): The "volatility of volatility," which dictates the convexity (the "smile").
- Strength: Its greatest advantage is the ability to predict how the volatility smile will move as the underlying price changes, which is crucial for hedging (calculating "Greeks").

### SABR Model
```python
import quantgauge.calibration2d as ca

F, T = 100.0, 1.0
strikes = np.array([80, 90, 100, 110, 120])
vols = np.array([0.22, 0.20, 0.18, 0.19, 0.21])

# [alpha, beta, rho, nu]
initial_guess = [0.15, 0.7, -0.2, 0.3]

# Standard SABR constraints
sabr_bounds = [ (0.001, None),  # alpha > 0
  (0.0, 1.0),  # 0 <= beta <= 1
  (-0.99, 0.99),  # -1 < rho < 1
  (0.001, None)  # nu > 0
  ]

model = ca.SABRModel()
opt_params = model.minimise_sabr(initial_guess, F, T, strikes, vols, sabr_bounds)

```
### SVI Model

```python
import quantgauge.calibration2d as ca

bound = [
        (0.0001, 2.0),  # a: Must be positive
        (0.0, 1.0),  # b: Must be non-negative
        (0.0001, 1.0),  # sigma: Must be positive
        (-0.99, 0.99),  # rho: Must be between -1 and 1
        (-1.0, 1.0)  # m: Strike offset
]

# 3. Initial Guess
initial_guess = [0.1, 0.1, 0.1, 0.0, 0.0]

    # Create a random number generator with a specific seed
rng = np.random.default_rng(seed=42)
market_strikes = np.linspace(30, 150, 40)
market_vols = svi_impl_vol.impl_vol_cal(market_strikes, 0.04, 0.1, 0.1, -0.5, 0) + rng.normal(0, 0.002, 40)

# 4. Run the Optimizer
model = ca.SVIModel()
model.minimise(initial_guess, market_strikes, market_vols, bound)

```
---

## Project Motivation

### Why Quant-Gauge?

Traditional option pricing models like Black-Scholes assume continuous asset prices and log-normal distributions. However, real-world markets exhibit **sudden jumps** in asset prices due to:

- Earnings announcements
- Market shocks
- Regulatory changes
- Geopolitical events

**Quant-Gauge solves this** by providing:

1. **Speed of C++** with the ease of Python
2. **Accurate jump-diffusion models** that capture market reality
3. **Zero compilation overhead** - pre-built binaries for all platforms
4. **Seamless integration** with existing Python quantitative finance workflows

---

## Performance Insights

### C++ Backend Architecture

Quant-Gauge uses:

- **pybind11**: Seamless C++/Python interoperability with zero overhead
- **Analytical solutions**: Closed-form pricing (no Monte Carlo variance)

### Why It's Fast

| Aspect | Benefit |
|--------|---------|
| **Compiled C++** | faster than pure Python NumPy |
| **Analytical pricing** | Instant results, no simulation overhead |
| **Direct binary** | No compilation step on user machines |

---

## Roadmap / Future Work

**Expanded Model Library:** Implement additional quantitative models and ensure each includes the computation of Greeks (Delta, Gamma, Vega, Theta, and Rho) for risk management.

**Numerical Methods:** Incorporate advanced numerical techniques—such as Monte Carlo simulations, Finite Difference Methods (FDM), and Binomial/Trinomial Trees—to price complex derivatives that lack analytical closed-form solutions.

**Demo Python Library**: I have not yet verified the reliability of the SABR and SVI models; however, I plan to implement comprehensive testing using pytest to ensure their accuracy and stability.

### Performance Enhancements

- [ ] **GPU Acceleration** - CUDA kernels for batch pricing
- [ ] **Vectorized Pricing** - Price multiple options in parallel
- [ ] **Greeks Computation** - Delta, Gamma, Vega, Theta, Rho

---

## License

MIT License - See LICENSE file for details

---

## Support

For bugs, questions, or feature requests:
- **GitHub Issues**: [Open an issue](https://github.com/kabinanB/quant-gauge/issues)
- **Email**: bkabinan@email.com

---

## References

1. **Merton, R. C.** (1976). "Option pricing when underlying stock returns are discontinuous"
2. **Kou, S. G.** (2002). "A Jump-Diffusion Model for Option Pricing"
3. **Cont, R. & Tankov, P.** (2004). "Financial Modelling with Jump Processes"
4. **Gatheral, J & Jacquier, A.** (2012). "Arbitrage-free SVI volatility surfaces"
5. **Hagan, P. S. & Kumar, D.** (2014). "Arbitrage‐free SABR"


