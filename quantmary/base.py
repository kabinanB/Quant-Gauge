from scipy.stats import norm
import numpy as np
from abc import ABC, abstractmethod


class OptionRegistry:
    """The hub that maps (model, option_type) to specific classes."""
    _models = {}

    @classmethod
    def register(cls, model_name, type_name):
        def wrapper(subclass):
            # Normalize keys to uppercase/lowercase for consistency
            cls._models[(model_name.upper(), type_name.lower())] = subclass
            return subclass

        return wrapper

    @classmethod
    def get(cls, model, type_name, **kwargs):
        key = (model.upper(), type_name.lower())
        if key not in cls._models:
            available = [f"{m} {t}" for m, t in cls._models.keys()]
            raise ValueError(f"Model '{model}' with type '{type_name}' not found. "
                             f"Available options: {available}")

        # Instantiate the class found in the registry
        return cls._models[key](**kwargs)



class Option(ABC):
    """The Abstract Blueprint every specific option must follow."""
    def __init__(self, s, sigma, r, k, t):
        self.s = float(s)
        self.sigma = sigma
        self.r = r
        self.k = float(k)
        self.t = float(t)

    @abstractmethod
    def price(self) -> float:
        pass

    @abstractmethod
    def delta(self) -> float:
        pass

    @abstractmethod
    def gamma(self) -> float:
        pass

    @abstractmethod
    def vega(self) -> float:
        pass

    @abstractmethod
    def theta(self) -> float:
        pass

    @abstractmethod
    def rho(self) -> float:
        pass

    @abstractmethod
    def summary(self):
        pass

    @staticmethod
    def d1(self) -> float:
        x = np.log(self.s / self.k)
        y = (self.r + self.sigma * self.sigma / 2) * self.t
        d1 = (x + y) / (self.sigma * self.t)

        return d1

    # utilities

    @staticmethod
    def cdf(x) -> float:
        return norm.cdf(x, loc=0, scale=1)


    def pdf(self) -> float:
        d1 = self.d1(self)
        pdf = np.exp(-0.5 * d1 * d1) / (np.sqrt(2 * np.pi))
        return pdf











