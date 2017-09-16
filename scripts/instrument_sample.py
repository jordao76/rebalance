import sys
sys.path.append('../rebalance')

from rebalance import *
from tests.googlefinance_tests import check_connection
from tests.stubs import FixedPriceService

if not check_connection():
    Instrument.price_service = FixedPriceService()

# instruments (ETFs)
VFV = Instrument('VFV', 'Vanguard S&P 500 Index ETF')

# plotting
VFV.plot_prices()
VFV.plot_returns(Decimal(1000))
Plotter.show()
