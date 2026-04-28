
import numpy as np
from base import OptionRegistry, Option

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