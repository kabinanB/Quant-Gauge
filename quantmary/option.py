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

    # utilities

    @staticmethod
    def d1(self) -> float:
        x = np.log(self.s / self.k)
        y = (self.r + self.sigma * self.sigma / 2) * self.t
        d1 = (x + y) / (self.sigma * self.t)

        return d1

    @staticmethod
    def cdf(self, x) -> float:
        return norm.cdf(x, loc=0, scale=1)



# Then, in your model files:
@OptionRegistry.register("BS", "ECall")
class BSEuropeanCall(Option):
    """
        model: Black Scholes
        option type: vanilla European Call option
    """

    def price(self) -> float:

        d1 = self.d1(self)
        d2 = d1 - self.sigma * self.t

        cdf1 = self.cdf(self, d1)
        cdf2 = self.cdf(self, d2)

        return self.s*cdf1 - (self.k * np.exp(-self.r*self.t)*cdf2)

    def delta(self) -> float:
        d1 = self.d1(self)
        cdf = self.cdf(self, d1)
        return cdf

    def gamma(self) -> float:
        pass

    def vega(self) -> float:
        pass

    def theta(self) -> float:
        pass

    def rho(self) -> float:
        pass

    def summary(self):
        pass

@OptionRegistry.register("BS", "EPut")
class BSEuropeanPut(Option):
    """
        model: Black Scholes
        option type: vanilla European Put option
    """

    def price(self) -> float:
        d1 = self.d1(self)
        d2 = d1 - self.sigma * self.t

        cdf1 = self.cdf(self, -d1)
        cdf2 = self.cdf(self, -d2)

        return (self.k * np.exp(-self.r*self.t)*cdf2) - self.s*cdf1

    def delta(self) -> float:
        d1 = self.d1(self)
        cdf = self.cdf(self, d1)
        return cdf - 1

    def gamma(self) -> float:
        pass

    def vega(self) -> float:
        pass

    def theta(self) -> float:
        pass

    def rho(self) -> float:
        pass

    def summary(self):
        pass


@OptionRegistry.register("MertonJumpDiffusionModel", "ECall")
class MertonJumpDiffusionModelECall(Option):

    def price(self) -> float:
        pass

    def delta(self) -> float:
        pass

    def gamma(self) -> float:
        pass

    def vega(self) -> float:
        pass

    def theta(self) -> float:
        pass

    def rho(self) -> float:
        pass

    def summary(self):
        pass


@OptionRegistry.register("MertonJumpDiffusionModel", "EPut")
class MertonJumpDiffusionModelEPut(Option):

    def price(self) -> float:
        pass

    def delta(self) -> float:
        pass

    def gamma(self) -> float:
        pass

    def vega(self) -> float:
        pass

    def theta(self) -> float:
        pass

    def rho(self) -> float:
        pass

    def summary(self):
        pass


@OptionRegistry.register("KouJumpDiffusionModel", "ECall")
class KouJumpDiffusionModelECall(Option):

    def price(self) -> float:
        pass

    def delta(self) -> float:
        pass

    def gamma(self) -> float:
        pass

    def vega(self) -> float:
        pass

    def theta(self) -> float:
        pass

    def rho(self) -> float:
        pass

    def summary(self):
        pass


@OptionRegistry.register("KouJumpDiffusionModel", "EPut")
class KouJumpDiffusionModelEPut(Option):

    def price(self) -> float:
        pass

    def delta(self) -> float:
        pass

    def gamma(self) -> float:
        pass

    def vega(self) -> float:
        pass

    def theta(self) -> float:
        pass

    def rho(self) -> float:
        pass

    def summary(self):
        pass

@OptionRegistry.register("SVIModel", "ECall")
class SVIModelECall(Option):

    def price(self) -> float:
        pass

    def delta(self) -> float:
        pass

    def gamma(self) -> float:
        pass

    def vega(self) -> float:
        pass

    def theta(self) -> float:
        pass

    def rho(self) -> float:
        pass

    def summary(self):
        pass


@OptionRegistry.register("SVIModel", "EPut")
class SVIModelEPut(Option):

    def price(self) -> float:
        pass

    def delta(self) -> float:
        pass

    def gamma(self) -> float:
        pass

    def vega(self) -> float:
        pass

    def theta(self) -> float:
        pass

    def rho(self) -> float:
        pass

    def summary(self):
        pass






