from quantmary.option import Option

# quantmary/__init__.py
from quantmary.option import OptionRegistry

def create_option(model: str, type_name: str, s: float, sigma: float, r: float, k: float, t: float):
    """
    The main API entry point.
    Usage: opt = qm.create_option("BS", "call", k=100, t=1.0)
    """
    return OptionRegistry.get(model, type_name, s=s, sigma=sigma, r=r, k=k, t=t)