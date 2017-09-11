from datetime import datetime
from decimal import Decimal
import requests
from rebalance.instrument import *

ONE_DAY_IN_SECONDS = 24 * 60 * 60

class GoogleFinanceClient:

    def get_prices(self, instrument, exchange='TSE', interval=ONE_DAY_IN_SECONDS):
        # http://www.networkerror.org/component/content/article/1-technical-wootness/44-googles-undocumented-finance-api.html
        period = '1Y' # 1 year
        fields = 'd,c' # d=datetime, c=closing price
        params = {'q':instrument,'x':exchange,'p':period,'i':interval,'f':fields}
        price_data = requests.get("https://www.google.com/finance/getprices", params=params)
        lines = price_data.text.splitlines()
        return self.parse_prices(lines)

    def parse_prices(self, lines):
        dates, prices = [], []
        startdatetime = 0
        for price in lines:
            cols = price.split(",")
            if cols[0][0] == 'a':
                startdatetime = int(cols[0][1:])
                dates.append(datetime.fromtimestamp(startdatetime).date())
                prices.append([Decimal(cols[1])])
            elif cols[0][0].isdigit():
                date = startdatetime + (int(cols[0])*ONE_DAY_IN_SECONDS)
                dates.append(datetime.fromtimestamp(date).date())
                prices.append([Decimal(cols[1])])
        return dates, prices
