from rebalance.instrument import *
from rebalance.portfolio import *
from rebalance.googlefinance import *
from rebalance.plotting import *

# default price service
Instrument.price_service = GoogleFinanceClient()
