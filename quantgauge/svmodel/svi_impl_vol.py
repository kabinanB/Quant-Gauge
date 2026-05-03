import numpy as np
import matplotlib.pyplot as plt


def impl_vol_cal(k, a, b, sig, rho, m):
    # k can now be a NumPy array
    t1 = (k - m) ** 2
    t2 = sig ** 2
    q1 = rho * (k - m) + np.sqrt(t1 + t2)
    return a + b * q1


def plot(mink, maxk, interval, a, b, sig, rho, m):
    # Create the strike range as a vector
    k_range = np.arange(mink, maxk, interval)

    # Calculate all vols using vectorisation
    vols = impl_vol_cal(k_range, a, b, sig, rho, m)

    plt.plot(k_range, vols, label="SVI Fit")
    plt.xlabel('Strike (k)')
    plt.ylabel('Implied Vol')
    plt.legend()
    plt.show()