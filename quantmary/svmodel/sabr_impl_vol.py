import numpy as np
import matplotlib.pyplot as plt
import warnings


def sabr_vol(K, F, T, alpha, beta, rho, nu):
    """
    SABR volatility model with improved numerical stability.

    Parameters:
    -----------
    K : float or array - Strike price(s)
    F : float - Forward price
    T : float - Time to maturity
    alpha : float - At-the-money volatility
    beta : float - CEV exponent (0 to 1)
    rho : float - Correlation between asset and vol (-1 to 1)
    nu : float - Vol of vol

    Returns:
    --------
    float or array - Implied volatility
    """
    # Suppress warnings during calculation
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        # 1. Handle the ATM case (where F == K)
        is_atm = np.abs(F - K) < 1e-8

        # Formula for ATM volatility
        vol_atm = (alpha / (F ** (1 - beta))) * (
                1 + (
                ((1 - beta) ** 2 / 24) * (alpha ** 2 / (F ** (2 - 2 * beta))) +
                (1 / 4) * (rho * beta * nu * alpha / (F ** (1 - beta))) +
                ((2 - 3 * rho ** 2) / 24) * nu ** 2
        ) * T
        )

        # 2. Handle the general case (where F != K)
        logFK = np.log(np.maximum(F / K, 1e-10))  # Prevent log(0)

        # Avoid division by zero or negative fk
        fk = (F * K) ** ((1 - beta) / 2)
        fk = np.maximum(fk, 1e-10)

        z = (nu / alpha) * fk * logFK

        # x(z) calculation with improved stability
        discriminant = 1 - 2 * rho * z + z ** 2

        # Ensure discriminant is non-negative before sqrt
        discriminant = np.maximum(discriminant, 1e-10)
        sqrt_term = np.sqrt(discriminant)

        pre_x = (sqrt_term + z - rho) / (1 - rho)
        pre_x = np.maximum(pre_x, 1e-10)  # Ensure positive before log

        x_z = np.log(pre_x)

        # Avoid division by zero in z/x_z
        x_z = np.where(np.abs(x_z) < 1e-10, 1e-10, x_z)

        # Denominator calculation with epsilon safeguard
        logFK_sq = logFK ** 2
        logFK_4th = logFK ** 4
        denom = 1 + ((1 - beta) ** 2 / 24) * logFK_sq + ((1 - beta) ** 4 / 1920) * logFK_4th
        denom = np.maximum(denom, 1e-10)  # Prevent division by zero

        term1 = alpha / (fk * denom)

        # General formula
        vol_general = term1 * (z / x_z) * (
                1 + (
                ((1 - beta) ** 2 / 24) * (alpha ** 2 / (fk ** 2)) +
                (1 / 4) * (rho * beta * nu * alpha / fk) +
                ((2 - 3 * rho ** 2) / 24) * nu ** 2
        ) * T
        )

        # Return ATM or general formula based on moneyness
        return np.where(is_atm, vol_atm, vol_general)


def plot_sabr(F, T, alpha, beta, rho, nu, mink=80, maxk=120, step=1.0):
    # Vectorized range of strikes
    k_range = np.arange(mink, maxk, step)

    # Single call to vectorized function
    vols = sabr_vol(k_range, F, T, alpha, beta, rho, nu)

    plt.figure(figsize=(8, 5))
    plt.plot(k_range, vols, label=f"SABR (α={alpha}, β={beta}, ρ={rho}, ν={nu})", color='navy')
    plt.axvline(F, color='red', linestyle='--', label=f"ATM Forward ({F})")
    plt.title("SABR Implied Volatility Surface")
    plt.xlabel("Strike (K)")
    plt.ylabel("Implied Vol")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


# Example Usage
if __name__ == "__main__":
    plot_sabr(F=100, T=1.0, alpha=0.15, beta=0.7, rho=-0.3, nu=0.4)