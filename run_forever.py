import sys

from time import sleep
from cryptocollector.exchange.feeds import Feeds
from cryptocollector.utils.utils import setup_logger

logger = setup_logger(name=__name__)

def run_forever(exchange_name, delay=2):

    def run_once():

        feed = Feeds()

        # Get exchange feed.
        try:
            exchange = getattr(feed, exchange_name)()
        except Exception:
            print(f'{sys.argv[1]} is not supported.')
            return

        # Run until exchange feed stops.
        exchange.daemon = True
        exchange.start()

        while not exchange.stop.is_set():
            sleep(2)        
        else:
            if exchange.monitor is not None:
                exchange.monitor.join()
            exchange.join()

    stop = False
    while not stop:
        try:
            logger.info('Started.')
            run_once()
        except KeyboardInterrupt as e:
            logger.critical(repr(e))
            stop = True
        sleep(2)
    logger.info('Stopped.')            

if __name__ == '__main__':
    run_forever(sys.argv[1])