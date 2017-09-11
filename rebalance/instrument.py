from collections import namedtuple
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
from matplotlib.ticker import StrMethodFormatter
from datetime import date, timedelta

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

    def plot_prices(self, plt=plt):
        dates, prices = self.get_prices()
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
        dates = range(365)
        today = date.today()
        dates = [today - timedelta(days=d) for d in reversed(range(365))]
        prices = [1 for _ in range(365)]
        return dates, prices
CASH = Cash('CASH', 'Cash', None)

##############
