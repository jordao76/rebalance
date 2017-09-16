import sys
sys.path.append('../rebalance')

from decimal import Decimal
from rebalance import *
from tests.googlefinance_tests import check_connection
from tests.stubs import FixedPriceService

if not check_connection():
    Instrument.price_service = FixedPriceService()

# instruments (ETFs)
ZAG = Instrument('ZAG', 'BMO Aggregate Bond Index EFT')
XAW = Instrument('XAW', 'iShares Core MSCI All Country World ex Canada Index ETF')
VFV = Instrument('VFV', 'Vanguard S&P 500 Index ETF')

my_portfolio = Portfolio({
    CASH: Decimal(500),
    ZAG: Decimal(1000),
    VFV: Decimal(3000),
    XAW: Decimal(5500)})
assert my_portfolio.total == Decimal(10000)

model_portfolio = Portfolio({
    ZAG: Decimal(25),
    VFV: Decimal(25),
    XAW: Decimal(50)})
assert model_portfolio.total == Decimal(100)

# rebalancing
orders = my_portfolio.rebalance(model_portfolio)
assert orders == [
    Order(action=SELL, instrument=VFV, amount=Decimal('500.00')),
    Order(action=SELL, instrument=XAW, amount=Decimal('500.00')),
    Order(action=BUY, instrument=ZAG, amount=Decimal('1500.00'))]

# plotting
my_portfolio.plot()
my_portfolio.plot_returns()
Plotter.show()
