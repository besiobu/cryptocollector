import sys
import time 

from cryptocollector.exchange.feeds import Feeds
from cryptocollector.utils.utils import setup_logger

logger = setup_logger(name=__name__)

def run_forever(exchange_name, delay=2):
    """

    Keep connecting to exchange websocket.

    """

    def run_once():
        """

        Connect to exchange websocket.

        """
        feed = Feeds()

        try:
            # Get exchange feed.
            exchange = getattr(feed, exchange_name)()
        except Exception:
            print(f'{sys.argv[1]} is not supported.')
            return

        exchange.daemon = True
        exchange.start()

        try:            
            # Run until exchange feed stops.
            while not exchange.stop.is_set():
                time.sleep(delay)        
            else:
                if exchange.monitor is not None:
                    exchange.monitor.join()
                exchange.join()                
        except KeyboardInterrupt as e:            

            logger.critical(repr(e))            

            # Stop threads and close db connection
            exchange.stop.set()
            if exchange.monitor is not None:
                exchange.monitor.join()
            exchange.join()         

            return True

    stop = False
    while not stop:
        try:
            logger.info('Started.')
            stop = run_once()
        except KeyboardInterrupt as e:
            logger.critical(repr(e))
            stop = True
        time.sleep(delay)
    logger.info('Stopped.')            

if __name__ == '__main__':
    run_forever(sys.argv[1])