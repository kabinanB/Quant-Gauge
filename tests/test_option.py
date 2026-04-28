import pytest
import quantmary as qm
from quantmary.option import Option
import numpy as np


class TestOption:

    def test_price(self):
        # market & trade data
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        call = qm.create_option(model="BS", type_name="ECall", s=s, sigma=sigma, r=r, k=k, t=t )
        call_price = call.price()



        assert isinstance(call_price, float)
        assert 6.78101 == pytest.approx(float(call_price), rel=1e-3)

    def test_put(self):
        """
            Test put price by put-call parity
        """
        # market & trade data
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        call = qm.create_option(model="BS", type_name="ECall", s=s, sigma=sigma, r=r, k=k, t=t )
        call_price = call.price()

        put = qm.create_option(model="BS", type_name="EPut", s=s, sigma=sigma, r=r, k=k, t=t)
        put_price = put.price()

        put_pcp = call_price - s + k * np.exp(-r*t)
        assert isinstance(call_price, float)
        assert pytest.approx(put_price) == pytest.approx(put_pcp)

    def test_delta_call(self):
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        call = qm.create_option(model="BS", type_name="ECall", s=s, sigma=sigma, r=r, k=k, t=t)
        delta = call.delta()

        assert isinstance(delta, float)
        assert 0.48612 == pytest.approx(float(delta), rel=1e-3)

    def test_delta_put(self):
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        put = qm.create_option(model="BS", type_name="EPut", s=s, sigma=sigma, r=r, k=k, t=t)
        delta = put.delta()

        assert isinstance(delta, float)

        assert -0.51388 == pytest.approx(float(delta), rel=1e-3)
