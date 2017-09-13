from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
from matplotlib.ticker import StrMethodFormatter
from datetime import date, timedelta
from decimal import Decimal

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

    def plot_prices(self, plt=plt):
        dates, prices = self.get_prices()
        self.__plot(dates, prices, plt)

    def plot_returns(self, investment, plt=plt):
        dates, returns = self.get_returns(investment)
        self.__plot(dates, returns, plt)

    def __plot(self, dates, prices, plt):
        fig, ax = plt.subplots()
        fig.autofmt_xdate()
        ax.set_title(self.symbol)
        ax.plot_date(dates, prices, '-')
        ax.yaxis.set_major_formatter(StrMethodFormatter('${x:,.2f}'))
        ax.xaxis.set_major_locator(MonthLocator())
        ax.xaxis.set_major_formatter(DateFormatter("%b-%Y"))
        ax.autoscale_view()
        ax.grid(True)

Instrument.__new__.__defaults__ = ('', 'TSE')

##############

class Cash(Instrument):
    __slots__ = ()
    def get_prices(self):
        # daily prices for a year
        DAYS = 365
        factors = np.arange(DAYS-1,-1,step=-1).reshape(DAYS,1)
        dates = date.today() - factors * timedelta(days=1)
        prices = np.full((DAYS,1), Decimal(1))
        return dates, prices
CASH = Cash('CASH', 'Cash', None)

##############
