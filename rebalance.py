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

ZERO = Decimal(0)

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

    def is_balanced(self, model_portfolio, threshold=ZERO):
        for _, value_offset, target_value in self.__diff(model_portfolio):
            # check that the difference to the target_value is beyond the threshold
            if abs(value_offset) / target_value > threshold / 100:
                return False
        return True

    def rebalance(self, model_portfolio, threshold=ZERO):
        if self.is_balanced(model_portfolio, threshold): return []
        orders = []
        for instrument, value_offset, _ in self.__diff(model_portfolio):
            if instrument != CASH:
                action = (BUY if value_offset > 0 else SELL)
                orders.append(Order(action, instrument, abs(value_offset)))
        return sorted(orders)

    def __diff(self, model_portfolio):
        target_allocations = self.__resolve_target_allocations(model_portfolio)
        res = []
        for instrument, target_alloc in target_allocations.items():
            curr_alloc = self.allocations[instrument]
            alloc_offset = target_alloc - curr_alloc
            value_offset = self.total * alloc_offset / 100
            if value_offset != 0:
                value = self.positions.get(instrument, ZERO)
                target_value = value + value_offset
                # the instrument is off by value_offset to its target_value
                res.append((instrument, value_offset, target_value))
        return res

    def __resolve_target_allocations(self, model_portfolio):
        # so that all relevant instruments are covered,
        # start with the model portfolio allocations,
        # then add the instruments not present there,
        # but present in this portfolio, with a ZERO allocation
        res = dict(model_portfolio.allocations)
        for instrument in self.positions.keys():
            if instrument not in res:
                res[instrument] = ZERO
        return res

##############
