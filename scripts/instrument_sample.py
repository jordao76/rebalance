import sys
sys.path.append('../rebalance')

from rebalance import *
import matplotlib.pyplot as plt

# instruments (ETFs)
ZAG = Instrument('ZAG', 'BMO Aggregate Bond Index EFT')

# plotting
ZAG.plot_prices()

plt.show()
