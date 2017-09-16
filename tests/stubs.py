from rebalance import GoogleFinanceClient

##############

class FixedPriceService(GoogleFinanceClient):
    def get_prices(self, instrument, exchange='TSE'):
        with open('tests/{}-sample.txt'.format(instrument)) as f:
            lines = [line.strip() for line in f]
        return self.parse_prices(lines)

##############
