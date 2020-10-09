import json

from cryptocollector.exchange.exchange_feed import ExchangeFeed
from cryptocollector.utils.utils import setup_logger

logger = setup_logger(name=__name__)

class Coinbase(ExchangeFeed):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)                         
        self.name = type(self).__name__  + '_feed'
        self.sequences = {}

    def on_open(self):

        sub_msg = {'type': 'subscribe',
                   'product_ids': self.symbols, 
                   'channels': ['matches']}

        self.ws.send(json.dumps(sub_msg))

    def on_message(self, msg):

        msg_type = msg["type"]                    

        if msg_type == "match":
            self.__handler_match(msg)
        
        elif msg_type == "last_match":
            logger.info(f"Ignoring {msg_type} message.")

        elif msg_type == "error":
            logger.info(f'Received error message {msg["message"]}.')

        elif msg_type == "subscriptions":
            self.__handler_subscriptions(msg)

        elif msg_type == "heartbeat":
            self.__heartbeat_handler(msg)
        else:
            logger.info(f'Received unsupported message {msg_type}.')

    def __handler_subscriptions(self, msg):
        """

        Hanlde subscription messages.

        Notes
        -----
        This is an example message from the 
        exchanges documentation.

        {
            "type": "subscriptions",
            "channels": [
                {
                    "name": "level2",
                    "product_ids": [
                        "ETH-USD",
                        "ETH-EUR"
                    ],
                },
                {
                    "name": "heartbeat",
                    "product_ids": [
                        "ETH-USD",
                        "ETH-EUR"
                    ],
                },
                {
                    "name": "ticker",
                    "product_ids": [
                        "ETH-USD",
                        "ETH-EUR",
                        "ETH-BTC"
                    ]
                }
            ]
        }        
        """

        for ch in msg['channels']:
            for product in ch['product_ids']:
                channel = ch['name']
                logger.info(f'subscribed to {channel} for {product}')            

    def __heartbeat_handler(self, msg):
        """

        Handle heartbeat messages.

        Notes
        -----
        This is an example message from the 
        exchanges documentation.

        {
            "type": "heartbeat",
            "sequence": 90,
            "last_trade_id": 20,
            "product_id": "BTC-USD",
            "time": "2014-11-07T08:19:28.464459Z"
        }
        """

        self.sequences[msg['product_id']] = {"seq": int(msg['sequence']), 
                                             "tid": int(msg['last_trade_id'])}                

    def __handler_match(self, msg):
        """

        Handle match (trade) messages.

        Notes
        -----
        This is an example message from the 
        exchanges documentation.

        {
            "type": "match",
            "trade_id": 10,
            "sequence": 50,
            "maker_order_id": "ac928c66-ca53-498f-9c13-a110027a60e8",
            "taker_order_id": "132fb6ae-456b-4654-b4e0-d681ac05cea1",
            "time": "2014-11-07T08:19:27.028459Z",
            "product_id": "BTC-USD",
            "size": "5.23512",
            "price": "400.23",
            "side": "sell"
        }        
        """

        self.persistance.write(msg=msg)
