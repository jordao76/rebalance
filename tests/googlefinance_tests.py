import requests
import unittest
from rebalance import GoogleFinanceClient

##############

def check_connection(url='https://www.google.com', timeout_in_seconds=5):
    try:
        requests.head(url, timeout=timeout_in_seconds)
        return True
    except requests.ConnectionError:
        return False

##############

class GoogleFinanceClientTest(unittest.TestCase):

    @unittest.skipIf(not check_connection(), 'no connection')
    def test_get_from_google_finance(self):
        gfc = GoogleFinanceClient()
        dates, prices = gfc.get_prices('VFV')
        self.assertTrue(len(dates) > 100)
        self.assertEqual(len(prices), len(dates))

##############
