from rebalance.instrument import *
from rebalance.portfolio import *
from rebalance.googlefinance import *

# default price service
Instrument.price_service = GoogleFinanceClient()
