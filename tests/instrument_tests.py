from decimal import Decimal
from datetime import date, timedelta
import unittest
from unittest.mock import MagicMock
from rebalance import Instrument, CASH, Plotter
from tests.stubs import FixedPriceService

##############

Instrument.price_service = FixedPriceService()

VFV = Instrument('VFV', 'Vanguard S&P 500 Index ETF')

##############

class InstrumentTest(unittest.TestCase):

    def test_instrument_defaults(self):
        AAA = Instrument('AAA')
        self.assertEqual(AAA.symbol, 'AAA')
        self.assertEqual(AAA.name, '')
        self.assertEqual(AAA.exchange, 'TSE')

    def test_get_prices(self):
        act_dates, act_prices = VFV.get_prices()
        self.assertEqual(len(act_dates), 251)
        self.assertEqual(act_dates[0][0], date(2016, 9, 13))
        self.assertEqual(act_dates[-1][0], date(2017, 9, 12))
        self.assertEqual(len(act_prices), len(act_dates))
        self.assertEqual(act_prices[0][0], Decimal('28.89'))
        self.assertEqual(act_prices[-1][0], Decimal('30.69'))

    def test_plot_prices(self):
        plotter = MagicMock()
        VFV.plot_prices(plotter)
        args = plotter.plot_prices.call_args
        act_dates = args[0][0]
        act_prices = args[0][1]
        exp_dates, exp_prices = VFV.get_prices()
        self.assertTrue((act_dates == exp_dates).all())
        self.assertTrue((act_prices == exp_prices).all())

    def test_get_returns(self):
        investment = Decimal(50000)
        act_dates, act_returns = VFV.get_returns(investment)
        self.assertEqual(len(act_dates), 251)
        self.assertEqual(len(act_returns), len(act_dates))
        shares = investment / Decimal('28.89')
        self.assertEqual(act_returns[0][0], investment)
        self.assertEqual(act_returns[-1][0], shares * Decimal('30.69'))

    def test_plot_returns(self):
        investment = Decimal('12345.34')
        plotter = MagicMock()
        VFV.plot_returns(investment, plotter)
        args = plotter.plot_prices.call_args
        act_dates = args[0][0]
        act_returns = args[0][1]
        exp_dates, exp_returns = VFV.get_returns(investment)
        self.assertTrue((act_dates == exp_dates).all())
        self.assertTrue((act_returns == exp_returns).all())

    def test_get_prices_cash(self):
        dates, prices = CASH.get_prices()
        self.assertEqual(len(dates), 365)
        self.assertEqual(len(prices), len(dates))
        exp_dates = [[date.today() - timedelta(days=d)] for d in reversed(range(365))]
        self.assertTrue((dates == exp_dates).all())
        self.assertTrue((prices == 1).all())

    def test_get_returns_cash(self):
        dates, returns = CASH.get_returns(50000)
        self.assertEqual(len(returns), len(dates))
        exp_dates = [[date.today() - timedelta(days=d)] for d in reversed(range(365))]
        self.assertTrue((dates == exp_dates).all())
        self.assertTrue((returns == 50000).all())

##############
