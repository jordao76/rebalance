from collections import namedtuple
import numpy as np
from datetime import date
from decimal import Decimal
from rebalance.plotting import Plotter
from rebalance.utils import dates_till_target

##############

class Instrument(namedtuple('Instrument', 'symbol, name, exchange')):

    price_service = None

    __slots__ = ()

    def __repr__(self):
        return self.symbol

    def get_prices(self):
        # daily prices for a year
        return Instrument.price_service.get_prices(
            self.symbol, exchange=self.exchange)

    def get_returns(self, investment):
        # daily returns for a year with initial investment
        # note: dividends NOT accounted for
        dates, prices = self.get_prices()
        # calculate how many shares are bought on the first day (first price)
        # (using fractional shares)
        shares = investment / prices[0][0]
        returns = prices * shares
        return dates, returns

    def plot_prices(self, plotter=None):
        dates, prices = self.get_prices()
        return self.__plot(dates, prices, plotter)

    def plot_returns(self, investment, plotter=None):
        dates, returns = self.get_returns(investment)
        return self.__plot(dates, returns, plotter)

    def __plot(self, dates, prices, plotter):
        if plotter == None: plotter = Plotter()
        plotter.plot_prices(dates, prices, label=self.symbol, title=self.symbol)
        return plotter

Instrument.__new__.__defaults__ = ('', 'TSE')

##############

class Cash(Instrument):
    __slots__ = ()
    def get_prices(self):
        # daily prices for a year
        dates = dates_till_target(days=365, target=date.today())
        prices = np.full((365,1), Decimal(1))
        return dates, prices
CASH = Cash('CASH', 'Cash', None)

##############
