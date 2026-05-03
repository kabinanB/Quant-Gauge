
import numpy as np
from ..base import OptionRegistry, Option

import merton_cpp

@OptionRegistry.register("MertonJumpDiffusionModel", "ECall")
class MertonJumpDiffusionModelECall(Option):

    def price(self) -> float:
        call_opt = merton_cpp.EuropeanCall(self.k, self.t)
        return call_opt.JDAnalyticalPrice(self.s, self.sigma, self.r, self.lam, self.m, self.s_2, self.n)

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

    def summary(self) -> str:
        pass

    def __init__(self, s, sigma, r, k, t, lam, m, s_2, n):
        super().__init__(s, sigma, r, k, t)
        self.lam = lam
        self.m = m
        self.s_2 = s_2
        self.n = n

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

    def summary(self) -> str:
        pass