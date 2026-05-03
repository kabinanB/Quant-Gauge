import numpy as np
from quantmary.base import OptionRegistry, Option
import kou_cpp


@OptionRegistry.register("KouJumpDiffusionModel", "ECall")
class KouJumpDiffusionModelECall(Option):

    def price(self) -> float:
        call_opt = kou_cpp.create_european_call(self.t, self.k)
        return call_opt.priceByKouJumpDiffusion(self.s, self.r, self.sigma, self.lam,self.p,  self.eta1, self.eta2, self.count )

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

    def __init__(self, s, sigma, r, k, t, lam, eta1, eta2, p, count):
        super().__init__(s, sigma, r, k, t)

        self.lam = lam
        self.eta1 = eta1
        self.eta2 = eta2
        self.p = p
        self.count = count

@OptionRegistry.register("KouJumpDiffusionModel", "EPut")
class KouJumpDiffusionModelEPut(Option):

    def price(self) -> float:
        call_opt = kou_cpp.create_european_call(self.t, self.k)
        return call_opt.priceByKouJumpDiffusion(self.s, self.r, self.sigma, self.lam, self.p, self.eta1, self.eta2,
                                                self.count)

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

    def __init__(self, s, sigma, r, k, t, lam, eta1, eta2, p, count):
        super().__init__(s, sigma, r, k, t)

        self.lam = lam
        self.eta1 = eta1
        self.eta2 = eta2
        self.p = p
        self.count = count