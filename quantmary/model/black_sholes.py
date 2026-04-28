import numpy as np
from ..base import OptionRegistry, Option

@OptionRegistry.register("BS", "ECall")
class BSEuropeanCall(Option):
    """
        model: Black Scholes
        option type: vanilla European Call option
    """

    def price(self) -> float:

        d1 = self.d1(self)
        d2 = d1 - self.sigma * np.sqrt(self.t)

        cdf1 = self.cdf(d1)
        cdf2 = self.cdf(d2)

        return self.s*cdf1 - (self.k * np.exp(-self.r*self.t)*cdf2)

    def delta(self) -> float:
        d1 = self.d1(self)
        cdf = self.cdf(d1)
        return cdf

    def gamma(self) -> float:
        return self.pdf() / (self.sigma * self.s * np.sqrt(self.t))

    def vega(self) -> float:
        return self.pdf() * self.s * np.sqrt(self.t)

    def theta(self) -> float:
        d2 = self.d1(self) - self.sigma * np.sqrt(self.t)
        theta1 = self.sigma * self.s * self.pdf() / (2*np.sqrt(self.t))
        theta2 = self.r *self.k*(np.exp(-self.r*self.t)) * self.cdf(d2)

        return -theta1 - theta2

    def rho(self) -> float:
        d2 = self.d1(self) - self.sigma * np.sqrt(self.t)
        return self.k * self.t * (np.exp(-self.r*self.t)) * self.cdf(d2)

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
        d2 = d1 - self.sigma * np.sqrt(self.t)

        cdf1 = self.cdf(-d1)
        cdf2 = self.cdf(-d2)

        return (self.k * np.exp(-self.r*self.t)*cdf2) - self.s*cdf1

    def delta(self) -> float:
        d1 = self.d1(self)
        cdf = self.cdf(d1)
        return cdf - 1

    def gamma(self) -> float:
        return self.pdf() / (self.sigma * self.s * np.sqrt(self.t))

    def vega(self) -> float:
        return self.pdf() * self.s * np.sqrt(self.t)

    def theta(self) -> float:
        d2 = self.d1(self) - self.sigma * np.sqrt(self.t)
        theta1 = self.sigma * self.s * self.pdf() / (2*np.sqrt(self.t))
        theta2 = self.r *self.k*(np.exp(-self.r*self.t)) * self.cdf(-d2)

        return -theta1 + theta2

    def rho(self) -> float:
        d2 = self.d1(self) - self.sigma * np.sqrt(self.t)
        return -self.k * self.t * (np.exp(-self.r * self.t)) * self.cdf(-d2)

    def summary(self):
        pass
