import json

from cryptocollector.exchange.exchange_feed import ExchangeFeed
from cryptocollector.utils.utils import setup_logger

logger = setup_logger(name=__name__)

class Bitmex(ExchangeFeed):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = type(self).__name__ + '_feed'
        
    def on_open(self):

        symbols = list(map(lambda x: 'trade:' + str(x), self.symbols))

        sub_msg = {'op': 'subscribe', 'args': symbols}
                
        self.ws.send(json.dumps(sub_msg))

    def on_message(self, msg):

        if 'table' in msg and 'action' in msg:
            if msg['table'] == 'trade' and msg['action'] == 'insert':
                self.__handler_trade_insert(msg)
            else:
                pass
        elif 'subscribe' in msg:
            if msg['success'] == True:
                logger.info(f'Subscribed to {msg["subscribe"]}.')
            else:
                logger.info(f'Subscription failed.')
        elif 'error' in msg:
            for k,v in msg.items():
                logger.info(f'{k}: {v}')
        else:
            for k,v in msg.items():
                logger.info(f'{k}: {v}')

    def __handler_trade_insert(self, msg):        
        """

        Handle trade insert messages.

        Notes
        -----
        This is an example message from the 
        exchanges documentation.

        {'table': 'trade', 
        'action': 'insert', 
        'data': [{'timestamp': '2019-11-05T08:09:26.587Z', 
                  'symbol': 'XBTZ19', 
                  'side': 'Sell', 
                  'size': 2000, 
                  'price': 9386.5, 
                  'tickDirection': 'ZeroPlusTick', 
                  'trdMatchID': '48405459-36fc-6eea-87a6-8139753927aa', 
                  'grossValue': 21308000, 
                  'homeNotional': 0.21308, 
                  'foreignNotional': 2000}]}
        """

        for trade in msg['data']:
            self.persistance.write(msg=trade)
