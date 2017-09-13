from datetime import datetime
from decimal import Decimal
import requests
import numpy as np
from rebalance.instrument import *

ONE_DAY_IN_SECONDS = 24 * 60 * 60

class GoogleFinanceClient:

    # http://www.networkerror.org/component/content/article/1-technical-wootness/44-googles-undocumented-finance-api.html

    def get_prices(self, instrument, exchange='TSE', interval=ONE_DAY_IN_SECONDS):
        period = '1Y' # 1 year
        fields = 'd,c' # d=datetime, c=closing price
        params = {'q':instrument,'x':exchange,'p':period,'i':interval,'f':fields}
        price_data = requests.get("https://www.google.com/finance/getprices", params=params)
        lines = price_data.text.splitlines()
        return self.parse_prices(lines, interval)

    def parse_prices(self, lines, interval=ONE_DAY_IN_SECONDS):
        dates, prices = [], []
        start_epoch = 0
        for price in lines:
            cols = price.split(",")
            curr_epoch = 0
            if cols[0][0] == 'a':
                curr_epoch = start_epoch = int(cols[0][1:])
            elif cols[0][0].isdigit():
                curr_epoch = start_epoch + int(cols[0]) * interval
            if curr_epoch > 0:
                dates.append([datetime.fromtimestamp(curr_epoch).date()])
                prices.append([Decimal(cols[1])])
        return np.array(dates), np.array(prices)
