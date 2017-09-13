import sys
sys.path.append('../rebalance')
sys.path.append('../tests')

import matplotlib.pyplot as plt
from rebalance import *
from tests.instrument_tests import FixedPriceService, check_connection

if not check_connection():
    Instrument.price_service = FixedPriceService()

# instruments (ETFs)
VFV = Instrument('VFV', 'Vanguard S&P 500 Index ETF')

# plotting
VFV.plot_prices()
VFV.plot_returns(Decimal(1000))

plt.show()
