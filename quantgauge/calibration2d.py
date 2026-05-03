import numpy as np
from scipy.optimize import minimize

# Use the dot (.) to indicate "look inside the current package"
from .svmodel.svi_impl_vol import impl_vol_cal
from .svmodel.sabr_impl_vol import sabr_vol



class SVIModel:

    def objective_function(self, params, strikes, market_vols):
        a, b, sigma, rho, m = params
        # Calculate SVI vols for the current guess
        model_vols = impl_vol_cal(strikes, a, b, sigma, rho, m)
        # Return the sum of squared differences
        return np.sum((model_vols - market_vols)**2)


    def minimise(self, guess, market_strikes, market_vols, bound):

        result = minimize(
            self.objective_function,
            guess,
            args=(market_strikes, market_vols),
            bounds=bound,
            method='L-BFGS-B'
            )

        if result.success:
            optimized_params = result.x
            print(f"Calibrated Parameters: {optimized_params}")


class SABRModel:
    def objective_function(self, params, F, T, market_strikes, market_vols):
        alpha, beta, rho, nu = params
        # Calculate SABR vols for the current guess
        model_vols = sabr_vol(market_strikes, F, T, alpha, beta, rho, nu)
        # Return the sum of squared differences
        return np.sum((model_vols - market_vols) ** 2)

    def minimise_sabr(self,guess, F, T, market_strikes, market_vols, bounds):
        """
        Calibrates SABR parameters (alpha, beta, rho, nu) to market data.
        """
        result = minimize(
            self.objective_function,
            guess,
            args=(F, T, market_strikes, market_vols),
            bounds=bounds,
            method='L-BFGS-B'
        )

        if result.success:
            optimized_params = result.x
            print(f"SABR Calibrated Parameters: {optimized_params}")
            return optimized_params
        else:
            print("Calibration failed:", result.message)
            return None


# --- Example Usage ---
if __name__ == "__main__":
    # Market Data
    F, T = 100.0, 1.0
    strikes = np.array([80, 90, 100, 110, 120])
    vols = np.array([0.22, 0.20, 0.18, 0.19, 0.21])

    # [alpha, beta, rho, nu]
    initial_guess = [0.15, 0.7, -0.2, 0.3]

    # Standard SABR constraints
    sabr_bounds = [
        (0.001, None),  # alpha > 0
        (0.0, 1.0),  # 0 <= beta <= 1
        (-0.99, 0.99),  # -1 < rho < 1
        (0.001, None)  # nu > 0
    ]

    model = SABRModel()
    opt_params = model.minimise_sabr(initial_guess, F, T, strikes, vols, sabr_bounds)