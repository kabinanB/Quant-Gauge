import pytest
import quantgauge as qg
import numpy as np


class TestOption:

    def test_price(self):

        # market & trade data
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        call = qg.option.blackscholes(type_name="ECall", s=s, sigma=sigma, r=r, k=k, t=t)
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

        call = qg.option.blackscholes(type_name="ECall", s=s, sigma=sigma, r=r, k=k, t=t)
        call_price = call.price()

        put = qg.option.blackscholes(type_name="EPut", s=s, sigma=sigma, r=r, k=k, t=t)
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

        call = qg.option.blackscholes(type_name="ECall", s=s, sigma=sigma, r=r, k=k, t=t)
        delta = call.delta()

        assert isinstance(delta, float)
        assert 0.48612 == pytest.approx(float(delta), rel=1e-3)

    def test_delta_put(self):
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        put = qg.option.blackscholes(type_name="EPut", s=s, sigma=sigma, r=r, k=k, t=t)
        delta = put.delta()

        assert isinstance(delta, float)

        assert -0.51388 == pytest.approx(float(delta), rel=1e-3)

    def test_gamma_call(self):
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        call = qg.option.blackscholes(type_name="ECall", s=s, sigma=sigma, r=r, k=k, t=t)
        gamma = call.gamma()

        assert isinstance(gamma, float)
        assert 0.01994 == pytest.approx(float(gamma), rel=1e-3)


    def test_gamma_put(self):
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        put = qg.option.blackscholes(type_name="EPut", s=s, sigma=sigma, r=r, k=k, t=t)
        gamma = put.gamma()

        assert isinstance(gamma, float)
        assert 0.01994 == pytest.approx(float(gamma), rel=1e-3)

    def test_theta_call(self):
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        call = qg.option.blackscholes(type_name="ECall", s=s, sigma=sigma, r=r, k=k, t=t)
        theta = call.theta()

        assert isinstance(theta, float)
        assert -6.07854 == pytest.approx(float(theta), rel=1e-3)


    def test_theta_put(self):
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        put = qg.option.blackscholes(type_name="EPut", s=s, sigma=sigma, r=r, k=k, t=t)
        theta = put.theta()

        assert isinstance(theta, float)
        assert -0.94190 == pytest.approx(float(theta), rel=1e-3)

    def test_vega_call(self):
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        call = qg.option.blackscholes(type_name="ECall", s=s, sigma=sigma, r=r, k=k, t=t)
        vega = call.vega()

        assert isinstance(vega, float)
        assert 39.87007 == pytest.approx(float(vega), rel=1e-3)

    def test_vega_put(self):
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        put = qg.option.blackscholes(type_name="EPut", s=s, sigma=sigma, r=r, k=k, t=t)
        vega = put.vega()

        assert isinstance(vega, float)
        assert 39.87007 == pytest.approx(float(vega), rel=1e-3)

    def test_rho_call(self):
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        call = qg.option.blackscholes(type_name="ECall", s=s, sigma=sigma, r=r, k=k, t=t)
        rho = call.rho()

        assert isinstance(rho, float)
        assert 41.83073 == pytest.approx(float(rho), rel=1e-3)


    def test_rho_put(self):
        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        put = qg.option.blackscholes(type_name="EPut", s=s, sigma=sigma, r=r, k=k, t=t)
        rho = put.rho()

        assert isinstance(rho, float)
        assert -60.90204 == pytest.approx(float(rho), rel=1e-3)

    def test_summary(self):

        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        call = qg.option.blackscholes(type_name="ECall", s=s, sigma=sigma, r=r, k=k, t=t)
        summary = call.summary()

        assert isinstance(summary, str)

        test_summary = """
           -----------------------------------------------------------------
            price   |   delta   |   gamma   |   vega   |   theta   |   rho  
           -----------------------------------------------------------------
             6.78   |   0.49    |   0.02   |   39.87   |   -6.08   |   41.83
           -----------------------------------------------------------------
        """
        assert test_summary == summary

    def test_summary_put(self):

        s = 100.0
        sigma = 0.2
        r = 0.05
        k = 108.0
        t = 1.0

        put = qg.option.blackscholes(type_name="EPut", s=s, sigma=sigma, r=r, k=k, t=t)
        summary = put.summary()

        assert isinstance(summary, str)

        test_summary = """
           -----------------------------------------------------------------
            price   |   delta   |   gamma   |   vega   |   theta   |   rho  
           -----------------------------------------------------------------
             9.51   |   -0.51    |   0.02   |   39.87   |   -0.94   |   -60.90
           -----------------------------------------------------------------
        """
        assert test_summary == summary

