from collections import namedtuple, defaultdict
from decimal import *

##############

class Instrument(namedtuple('Instrument', 'symbol, name')):
    __slots__ = ()
    def __repr__(self): return self.symbol

CASH = Instrument('CASH', 'Cash')

##############

class Portfolio:

    def __init__(self, positions):
        self.total = sum(positions.values())
        self.positions = positions

    @property
    def allocations(self):
        res = defaultdict(Decimal)
        for instrument, value in self.positions.items():
            res[instrument] += value / self.total * 100
        return dict(res)

##############
