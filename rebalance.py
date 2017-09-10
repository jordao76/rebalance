from collections import namedtuple, defaultdict
from decimal import Decimal
import matplotlib.pyplot as plt

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

    def plot(self):
        symbols = list(self.positions.keys())
        values = list(self.positions.values())
        index = 0
        def get_label(pct):
            nonlocal values, index
            value = values[index]
            index += 1
            return '${:,.2f} ({:.2f}%)'.format(value, pct)
        fig, ax = plt.subplots()
        ax.pie(values, labels=symbols, autopct=get_label)
        ax.axis('equal')

##############

if __name__ == '__main__':

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
