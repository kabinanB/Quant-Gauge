# quantgauge/model/kou_jd.py

import numpy as np
from ..base import OptionRegistry, Option
from . import kou_cpp


@OptionRegistry.register("KouJumpDiffusionModel", "ECall")
class KouJumpDiffusionModelECall(Option):

    def __init__(self, s, sigma, r, k, t, lam, p, eta1, eta2, count):
        """Initialize Kou Jump Diffusion Call Option"""
        super().__init__(s, sigma, r, k, t)
        self.lam = lam      # Jump intensity
        self.p = p          # Probability of up jump
        self.eta1 = eta1    # Up jump decay rate
        self.eta2 = eta2    # Down jump decay rate
        self.count = count  # Number of terms in series

    def price(self) -> float:
        """Calculate price using Kou Jump Diffusion model"""
        call_opt = kou_cpp.create_european_call(self.t, self.k)
        return call_opt.priceByKouJumpDiffusion(
            self.s, self.r, self.sigma, 
            self.lam, self.p, self.eta1, self.eta2, self.count
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


@OptionRegistry.register("KouJumpDiffusionModel", "EPut")
class KouJumpDiffusionModelEPut(Option):

    def __init__(self, s, sigma, r, k, t, lam, p, eta1, eta2, count):
        """Initialize Kou Jump Diffusion Put Option"""
        super().__init__(s, sigma, r, k, t)
        self.lam = lam
        self.p = p
        self.eta1 = eta1
        self.eta2 = eta2
        self.count = count

    def price(self) -> float:
        """Calculate price using Kou Jump Diffusion model"""
        put_opt = kou_cpp.create_european_put(self.t, self.k)
        return put_opt.priceByKouJumpDiffusion(
            self.s, self.r, self.sigma,
            self.lam, self.p, self.eta1, self.eta2, self.count
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