import unittest
from rebalance import Instrument, CASH, Portfolio, BUY, SELL
from decimal import Decimal

##############

AAA = Instrument('AAA', 'AAA Index ETF')
BBB = Instrument('BBB', 'BBB Index ETF')
CCC = Instrument('CCC', 'CCC Index ETF')
DDD = Instrument('DDD', 'DDD Index ETF')

##############

class PortfolioBasicTest(unittest.TestCase):

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

##############

class PortfolioRebalanceTest(unittest.TestCase):

    def setUp(self):
        self.model_portfolio = Portfolio({
            CASH: Decimal(10),
            AAA: Decimal(40),
            BBB: Decimal(50)})

    def test_rebalance_cash(self):
        portfolio = Portfolio({CASH: Decimal(5000)})
        orders = portfolio.rebalance(self.model_portfolio)
        self.assertEqual(orders, [
            (BUY, AAA, Decimal(2000)),
            (BUY, BBB, Decimal(2500))])

    def test_rebalance_balanced(self):
        portfolio = Portfolio({
            CASH: Decimal(500),
            AAA: Decimal(2000),
            BBB: Decimal(2500)})
        orders = portfolio.rebalance(self.model_portfolio)
        self.assertEqual(orders, [])

    def test_rebalance_unbalanced(self):
        portfolio = Portfolio({
            AAA: Decimal(2000),
            BBB: Decimal(8000)})
        orders = portfolio.rebalance(self.model_portfolio)
        self.assertEqual(orders, [
            (SELL, BBB, Decimal(3000)),
            (BUY, AAA, Decimal(2000))])

    def test_rebalance_reinvest(self):
        portfolio = Portfolio({
            CCC: Decimal(2000),
            DDD: Decimal(8000)})
        orders = portfolio.rebalance(self.model_portfolio)
        self.assertEqual(orders, [
            (SELL, CCC, Decimal(2000)),
            (SELL, DDD, Decimal(8000)),
            (BUY, AAA, Decimal(4000)),
            (BUY, BBB, Decimal(5000))])

##############

class PortfolioIsBalancedTest(unittest.TestCase):

    def setUp(self):
        self.model_portfolio = Portfolio({
            AAA: Decimal(10),
            BBB: Decimal(90)})

    def make_portfolio(self, aaa, bbb):
        return Portfolio({
            AAA: Decimal(aaa),
            BBB: Decimal(bbb)})

    def test_balanced(self):
        portfolio = self.make_portfolio(1000, 9000)
        balanced = portfolio.is_balanced(self.model_portfolio)
        self.assertTrue(balanced)

    def test_unbalanced(self):
        portfolio = self.make_portfolio('999.99', '9000.01')
        balanced = portfolio.is_balanced(self.model_portfolio)
        self.assertFalse(balanced)

    def test_within_threshold(self):
        portfolio = self.make_portfolio(900, 9100)
        balanced = portfolio.is_balanced(
            self.model_portfolio, threshold=Decimal(10))
        self.assertTrue(balanced)

    def test_beyond_threshold(self):
        portfolio = self.make_portfolio(900, 9100)
        balanced = portfolio.is_balanced(
            self.model_portfolio, threshold=Decimal(9))
        self.assertFalse(balanced)

##############

from unittest.mock import MagicMock

class PortfolioPlotTest(unittest.TestCase):

    def setUp(self):
        self.portfolio = Portfolio({
            CASH: Decimal(129),
            AAA: Decimal(4034)})

    def test_plot(self):
        # mock matplotlib.pyplot pie chart
        fig, ax, plt = [MagicMock() for _ in range(3)]
        plt.subplots.return_value = (fig, ax)
        self.portfolio.plot(plt)

        # check arguments to ax.pie(...)
        args = ax.pie.call_args
        values = args[0][0]
        labels = args[1]['labels']

        pos, allocs = self.portfolio.positions, self.portfolio.allocations
        self.assertEqual(values, [pos[CASH], pos[AAA]])
        self.assertEqual(labels, [CASH, AAA])

        # call autopct function for the pie wedge texts
        autopct = args[1]['autopct']
        text1 = autopct(allocs[CASH])
        text2 = autopct(allocs[AAA])
        self.assertEqual(text1, '$129.00 (3.10%)')
        self.assertEqual(text2, '$4,034.00 (96.90%)')
