from .base import OptionRegistry

def blackscholes(type_name: str, s: float, sigma: float, r: float, k: float, t: float):
    """
    The main API entry point.
    Usage: opt = qm.create_option("BS", "call", k=100, t=1.0)
    """
    return OptionRegistry.get("BS", type_name, s=s, sigma=sigma, r=r, k=k, t=t)


def kou(type_name: str, s: float, sigma: float, r: float, k: float, t: float, lam:float, p: float, eta1: float, eta2: float, count: int) -> float:
    """
    The main API entry point.
    Usage: opt = qm.create_option("BS", "call", k=100, t=1.0)
    """
    return OptionRegistry.get("KouJumpDiffusionModel", type_name, s=s, sigma=sigma, r=r, k=k, t=t, lam=lam, p=p,eta1=eta1, eta2=eta2, count=count)

def merton(type_name: str, s: float, sigma: float, r: float, k: float, t: float, lam:float, m:float, s_2:float, n:float) -> float:
    """
    The main API entry point.
    Usage: opt = qm.create_option("BS", "call", k=100, t=1.0)
    """
    return OptionRegistry.get("MertonJumpDiffusionModel", type_name, s=s, sigma=sigma, r=r, k=k, t=t, lam=lam, m=m, s_2 = s_2, n=n)