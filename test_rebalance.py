import unittest
from rebalance import *
from decimal import *

AAA = Instrument('AAA', 'AAA Index ETF')

class TestPortfolio(unittest.TestCase):

    def setUp(self):
        self.portfolio = Portfolio({CASH: Decimal(1200), AAA: Decimal(300)})

    def test_portfolio_creation(self):
        self.assertEqual(
            self.portfolio.positions, {CASH: Decimal(1200), AAA: Decimal(300)})

    def test_portfolio_total(self):
        self.assertEqual(self.portfolio.total, Decimal(1500))

    def test_portfolio_allocations(self):
        self.assertEqual(
            self.portfolio.allocations, {CASH: Decimal(80), AAA: Decimal(20)})

if __name__ == '__main__':
    unittest.main()
