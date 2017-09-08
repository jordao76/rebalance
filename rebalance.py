from collections import namedtuple, defaultdict
from decimal import *

##############

class Instrument(namedtuple('Instrument', 'symbol, name')):
    __slots__ = ()
    def __repr__(self): return self.symbol
CASH = Instrument('CASH', 'Cash')

##############

class Action(namedtuple('Action', 'direction, name')):
    __slots__ = ()
    def __repr__(self): return self.name
# when sorting, SELL comes before BUY
# first sell, then buy
SELL = Action(-1, 'Sell')
BUY = Action(1, 'Buy')

##############

Order = namedtuple('Order', 'action, instrument, amount')

##############

class Portfolio:

    def __init__(self, positions):
        self.total = sum(positions.values())
        self.positions = positions
        self.allocations = self.__calc_allocations()

    def __calc_allocations(self):
        res = defaultdict(Decimal)
        for instrument, value in self.positions.items():
            res[instrument] += value / self.total * 100
        return res

    def rebalance(self, model_portfolio):
        target_allocations = self.__resolve_target_allocations(model_portfolio)
        orders = []
        for instrument, target_alloc in target_allocations.items():
            alloc = self.allocations[instrument]
            alloc_offset = target_alloc - alloc
            value_offset = self.total * alloc_offset / 100
            if instrument != CASH and value_offset != 0:
                action = (BUY if value_offset > 0 else SELL)
                orders.append(Order(action, instrument, abs(value_offset)))
        orders.sort()
        return orders

    def __resolve_target_allocations(self, model_portfolio):
        # so that all relevant instruments are covered,
        # start with the model portfolio allocations,
        # then add the instruments not present there,
        # but present in this portfolio, with a ZERO allocation
        res = dict(model_portfolio.allocations)
        for instrument in self.positions.keys():
            if instrument not in res:
                res[instrument] = Decimal(0)
        return res

##############
