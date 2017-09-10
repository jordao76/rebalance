from collections import namedtuple

##############

class Instrument(namedtuple('Instrument', 'symbol, name')):
    __slots__ = ()
    def __repr__(self): return self.symbol
CASH = Instrument('CASH', 'Cash')

##############
