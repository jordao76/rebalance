import sys
sys.path.append('../rebalance')

from rebalance import *
from decimal import Decimal
import matplotlib.pyplot as plt

# instruments (ETFs)
ZAG = Instrument('ZAG', 'BMO Aggregate Bond Index EFT')
VCN = Instrument('VCN', 'Vanguard FTSE Canada All Cap Index ETF')
XAW = Instrument('XAW', 'iShares Core MSCI All Country World ex Canada Index ETF')

my_portfolio = Portfolio({
    CASH: Decimal(500),
    ZAG: Decimal(1000),
    VCN: Decimal(3000),
    XAW: Decimal(5500)})
assert my_portfolio.total == Decimal(10000)

# canadian couch potato assertive model portfolio (2016)
model_portfolio = Portfolio({
    ZAG: Decimal(25),
    VCN: Decimal(25),
    XAW: Decimal(50)})
assert model_portfolio.total == Decimal(100)

# rebalancing
orders = my_portfolio.rebalance(model_portfolio)
assert orders == [
    Order(action=SELL, instrument=VCN, amount=Decimal('500.00')),
    Order(action=SELL, instrument=XAW, amount=Decimal('500.00')),
    Order(action=BUY, instrument=ZAG, amount=Decimal('1500.00'))]

# plotting
my_portfolio.plot()

plt.show()
