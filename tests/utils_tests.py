import numpy as np
from datetime import date
import unittest
from rebalance.utils import dates_till_target, fill_price_gaps

##############

class DatesPricesTest(unittest.TestCase):

    def test_dates_till_target(self):
        act_dates = dates_till_target(days=2, target=date(2016,1,1))
        exp_dates = np.array([[date(2015,12,31)],[date(2016,1,1)]])
        self.assertTrue((exp_dates == act_dates).all())

    def test_fill_price_gaps(self):
        dates = np.array([[date(2016,1,1)],[date(2016,1,3)]])
        prices = np.array([[42],[44]])
        act_dates, act_prices = fill_price_gaps(dates, prices)
        exp_dates = np.array([[date(2016,1,1)],[date(2016,1,2)],[date(2016,1,3)]])
        exp_prices = np.array([[42],[42],[44]])
        self.assertTrue((exp_dates == act_dates).all())
        self.assertTrue((exp_prices == act_prices).all())

##############
