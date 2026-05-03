import pytest
import quantmary as qm
from quantmary.model import merton_jd
import numpy as np
import pytest


class TestKou:

    def test_price(self):
        s = 100.0
        sigma = 0.15
        r = 0.05
        k = 105.0
        t = 0.5
        lam = 1.0
        m =0.05
        s_2 = 0.30
        n = 10

        merton_class = qm.option.merton(type_name="ECall", s=s, sigma=sigma, r=r, k=k, t=t, lam=lam, m=m, s_2=s_2, n=n)
        price = merton_class.price()


        assert isinstance(price, float)

        assert pytest.approx(7.75294, rel=1e-3) == price

