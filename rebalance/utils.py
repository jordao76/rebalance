from datetime import date, timedelta
import numpy as np

##############

def dates_till_target(days=365, target=date.today()):
    factors = np.arange(days-1,-1,step=-1).reshape(days,1)
    return target - factors * timedelta(days=1)

def all_dates(first_date, last_date):
    days_including_last = (last_date - first_date).days + 1
    return dates_till_target(days=days_including_last, target=last_date)

def fill_price_gaps(dates, prices):
    i, new_dates, new_prices = 0, [], []
    for date in all_dates(dates[0][0], dates[-1][0]):
        new_dates.append(date)
        if dates[i] == date:
            curr_price = prices[i]
            new_prices.append(curr_price)
            i += 1
        else:
            new_prices.append(curr_price)
    return np.array(new_dates), np.array(new_prices)

##############
