# quantgauge/option.py

from .base import OptionRegistry


def blackscholes(type_name: str, s: float, sigma: float, r: float, k: float, t: float):
    """
    Black-Scholes model API entry point.
    Usage: opt = qg.blackscholes("call", s=100, sigma=0.2, r=0.05, k=105, t=1.0)
    """
    return OptionRegistry.get("BS", type_name, s=s, sigma=sigma, r=r, k=k, t=t)


def kou(type_name: str, s: float, sigma: float, r: float, k: float, t: float,
        lam: float, p: float, eta1: float, eta2: float, count: int):
    """
    Kou Jump Diffusion model API entry point.
    Usage: opt = qg.kou("call", s=100, sigma=0.2, r=0.05, k=105, t=1.0,
                        lam=1.0, p=0.5, eta1=10, eta2=10, count=10)
    """
    return OptionRegistry.get("KouJumpDiffusionModel", type_name,
                              s=s, sigma=sigma, r=r, k=k, t=t,
                              lam=lam, p=p, eta1=eta1, eta2=eta2, count=count)


def merton(type_name: str, s: float, sigma: float, r: float, k: float, t: float,
           lam: float, m: float, s_2: float, n: float):
    """
    Merton Jump Diffusion model API entry point.
    Usage: opt = qg.merton("call", s=100, sigma=0.2, r=0.05, k=105, t=1.0,
                           lam=1.0, m=0.05, s_2=0.3, n=10)
    """
    return OptionRegistry.get("MertonJumpDiffusionModel", type_name,
                              s=s, sigma=sigma, r=r, k=k, t=t,
                              lam=lam, m=m, s_2=s_2, n=n)