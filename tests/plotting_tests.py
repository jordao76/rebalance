import requests
import unittest
from unittest.mock import MagicMock
from rebalance import Instrument, Plotter
from tests.stubs import FixedPriceService

##############

Instrument.price_service = FixedPriceService()

VFV = Instrument('VFV', 'Vanguard S&P 500 Index ETF')

##############

class PlottingTest(unittest.TestCase):

    def test_plot_prices(self):
        fig, ax, plt = [MagicMock() for _ in range(3)]
        plt.subplots.return_value = (fig, ax)
        plotter = Plotter(plt)
        exp_dates, exp_prices = VFV.get_prices()
        plotter.plot_prices(exp_dates, exp_prices)
        args = ax.plot_date.call_args
        act_dates = args[0][0]
        act_prices = args[0][1]
        self.assertTrue((act_dates == exp_dates).all())
        self.assertTrue((act_prices == exp_prices).all())

##############
