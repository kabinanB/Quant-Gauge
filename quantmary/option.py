from .base import OptionRegistry
import quantmary.model.black_sholes

def blackscholes(type_name: str, s: float, sigma: float, r: float, k: float, t: float):
    """
    The main API entry point.
    Usage: opt = qm.create_option("BS", "call", k=100, t=1.0)
    """
    return OptionRegistry.get("BS", type_name, s=s, sigma=sigma, r=r, k=k, t=t)