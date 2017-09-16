import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
from matplotlib.ticker import StrMethodFormatter

##############

class Plotter:

    def __init__(self, plt=plt):
        self.plt = plt
        self.fig, self.ax = None, None

    def plot_prices(self, dates, prices, label=None, title=None):
        fig, ax = self.fig, self.ax
        if (fig, ax) == (None, None):
            fig, ax = self.plt.subplots(figsize=(10,3))
            self.plt.subplots_adjust(
                top=0.92, bottom=0.1, left=0.1, right=0.98)
            ax.yaxis.set_major_formatter(StrMethodFormatter('${x:,.2f}'))
            ax.xaxis.set_major_locator(MonthLocator(interval=2))
            ax.xaxis.set_major_formatter(DateFormatter("%b-%Y"))
            ax.autoscale_view()
            ax.grid(True)
        ax.plot_date(dates, prices, '-', label=label)
        if title != None: ax.set_title(title)
        self.fig, self.ax = fig, ax

    def show():
        plt.show()

##############
