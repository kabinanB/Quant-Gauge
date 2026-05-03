import pytest
import quantmary as qm
from quantmary.model import kou_jd
import numpy as np


class TestKou:

    def test_price(self):
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0
        lam = 1.0
        eta1 = 20
        eta2 = 30
        p = 0.5
        count = 10

        kou_class = qm.option.kou(type_name="ECall", s=s, sigma=sigma, r=r, k=k, t=t, lam=lam, eta1=eta1, eta2=eta2, p=p, count=count)
        price = kou_class.price()


        assert isinstance(price, float)

        assert price > 0

    def test_price_put(self):
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0
        lam = 1.0
        eta1 = 20
        eta2 = 30
        p = 0.5
        count = 10

        kou_class = qm.option.kou(type_name="EPut", s=s, sigma=sigma, r=r, k=k, t=t, lam=lam, eta1=eta1, eta2=eta2, p=p, count=count)
        price = kou_class.price()


        assert isinstance(price, float)

        assert price > 0