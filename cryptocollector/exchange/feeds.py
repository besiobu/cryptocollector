from cryptocollector.exchange.coinbase import Coinbase
from cryptocollector.exchange.bitmex import Bitmex

from cryptocollector.cfg.config import COINBASE_CFG, BITMEX_CFG

class Feeds(object):

    def __init__(self):
        pass

    @staticmethod
    def coinbase():
        return Coinbase(**COINBASE_CFG)

    @staticmethod
    def bitmex():
        return Bitmex(**BITMEX_CFG)        