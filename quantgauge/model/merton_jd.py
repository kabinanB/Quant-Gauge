# quantgauge/model/merton_jd.py

from ..base import OptionRegistry, Option

# Import only when needed
def get_merton_cpp():
    from . import merton_cpp
    return merton_cpp

@OptionRegistry.register("MertonJumpDiffusionModel", "ECall")
class MertonJumpDiffusionModelECall(Option):

    def __init__(self, s, sigma, r, k, t, lam, m, s_2, n):
        super().__init__(s, sigma, r, k, t)
        self.lam = lam
        self.m = m
        self.s_2 = s_2
        self.n = n

    def price(self) -> float:
        merton_cpp = get_merton_cpp()
        call_opt = merton_cpp.MertonEuropeanCall(self.k, self.t)
        return call_opt.JDAnalyticalPrice(
            self.s, self.sigma, self.r,
            self.lam, self.m, self.s_2, self.n
        )

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


@OptionRegistry.register("MertonJumpDiffusionModel", "EPut")
class MertonJumpDiffusionModelEPut(Option):

    def __init__(self, s, sigma, r, k, t, lam, m, s_2, n):
        super().__init__(s, sigma, r, k, t)
        self.lam = lam
        self.m = m
        self.s_2 = s_2
        self.n = n

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