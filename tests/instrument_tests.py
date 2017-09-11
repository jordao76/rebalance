import unittest
from unittest.mock import MagicMock
from rebalance import Instrument, CASH, GoogleFinanceClient
from decimal import Decimal
from datetime import date, timedelta
import requests

##############

VFV = Instrument('VFV', 'Vanguard S&P 500 Index ETF')

##############

SAMPLE_GOOGLE_FINANCE_FILE_NAME = 'tests/VFV-sample.txt'

class FixedPriceService(GoogleFinanceClient):
    def get_prices(self, instrument, exchange):
        with open(SAMPLE_GOOGLE_FINANCE_FILE_NAME) as f:
            lines = [line.strip() for line in f]
        return self.parse_prices(lines)

##############

class InstrumentTest(unittest.TestCase):

    def setUp(self):
        Instrument.price_service = FixedPriceService()

    def tearDown(self):
        Instrument.price_service = GoogleFinanceClient()

    def test_instrument_defaults(self):
        AAA = Instrument('AAA')
        self.assertEqual(AAA.symbol, 'AAA')
        self.assertEqual(AAA.name, '')
        self.assertEqual(AAA.exchange, 'TSE')

    def test_get_prices(self):
        dates, prices = VFV.get_prices()
        self.assertEqual(len(dates), 248)
        self.assertEqual(len(prices), len(dates))

    def test_get_prices_cash(self):
        dates, prices = CASH.get_prices()
        self.assertEqual(len(dates), 365)
        self.assertEqual(len(prices), len(dates))
        exp_dates = [date.today() - timedelta(days=d) for d in reversed(range(365))]
        self.assertEqual(dates, exp_dates)
        exp_prices = [1 for _ in range(365)]
        self.assertEqual(prices, exp_prices)

    def test_plot_prices(self):
        fig, ax, plt = [MagicMock() for _ in range(3)]
        plt.subplots.return_value = (fig, ax)
        VFV.plot_prices(plt)
        args = ax.plot_date.call_args
        dates = args[0][0]
        prices = args[0][1]
        self.assertEqual(len(dates), 248)
        self.assertEqual(len(prices), len(dates))

##############

def check_connection(url='https://www.google.com', timeout_in_seconds=5):
    try:
        requests.head(url, timeout=timeout_in_seconds)
        return True
    except requests.ConnectionError:
        return False

class GoogleFinanceClientTest(unittest.TestCase):

    @unittest.skipIf(not check_connection(), 'no connection')
    def test_get_from_google_finance(self):
        gfc = GoogleFinanceClient()
        dates, prices = gfc.get_prices(VFV)
        self.assertTrue(len(dates) > 100)
        self.assertEqual(len(prices), len(dates))

    def test_parse_google_finance_result(self):
        with open(SAMPLE_GOOGLE_FINANCE_FILE_NAME) as f:
            lines = [line.strip() for line in f]
        gfc = GoogleFinanceClient()
        dates, prices = gfc.parse_prices(lines)
        self.assertEqual(len(dates), 248)
        self.assertEqual(dates[0], date(2016, 9, 12))
        self.assertEqual(dates[-1], date(2017, 9, 8))
        self.assertEqual(len(prices), len(dates))
        self.assertEqual(prices[0][0], Decimal('50.21'))
        self.assertEqual(prices[-1][0], Decimal('53.26'))

##############
