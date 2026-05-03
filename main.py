import svi_impl_vol as svi_impl_vol
from calibration2d import SVIModel
import numpy as np

if __name__ == "__main__":
    # a = 0.04
    # b = 0.4
    # sig = 0.1
    # rho = -0.4
    # m =0.1
    # svi_impl_vol.plot(-1.0, 1.0, 0.05, a, b, sig, rho, m)

    # 2. Set Bounds
    # params: (a, b, sigma, rho, m)
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
    model = SVIModel()
    model.minimise(initial_guess, market_strikes, market_vols, bound)

