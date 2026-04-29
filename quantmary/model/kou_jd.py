import numpy as np
from ..base import OptionRegistry, Option



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

    def summary(self) -> str:
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

    def summary(self) -> str:
        pass