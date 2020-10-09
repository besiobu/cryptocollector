import time
import logging

from threading import Thread
from cryptocollector.utils.utils import setup_logger

logger = setup_logger(name=__name__)

class WebsocketMonitor(Thread):
    """

    A class to monitor the websocket class.

    """

    def __init__(self, ws, time_recv, stop, timeout=15, wait=15):
        super().__init__()
        self.ws = ws
        self.time_recv = time_recv
        self.stop = stop
        self.timeout = timeout
        self.wait = wait
        self._count_chk = 0

    def run(self):
        """

        Monitor thread to keep connection alive.

        Notes
        -----
        If there is no new message from the websocket
        send ping every `timeout` seconds and wait 
        `wait` seconds between checking if new messages
        were received.

        """

        logger.info(f'Monitor is starting.')

        try:
            while not self.stop.is_set():
                if self.time_recv is not None:
                    if time.time() - self.time_recv >= self.timeout:
                        logger.warn(f'Monitor sending ping.')                
                        self.ws.ping('ping')
                    logger.info('Monitor waiting.')
                    time.sleep(self.wait)
            else:
                logger.warn(f'Monitor is stopping.')            
                pass
        except KeyboardInterrupt:
            self.stop.set()
            return    