import json
import time
from threading import Event, Thread

from cryptocollector.utils.utils import setup_logger
from cryptocollector.websocket.websocket_monitor import WebsocketMonitor

from websocket import create_connection

logger = setup_logger(name=__name__)

class WebsocketClient(Thread):
    """

    A websocket class.

    """

    def __init__(self, url, timeout=60):
        """

        Inputs:
        ------
        url : str
            The url of the websocket.
        timeout : int
            The websocket connection timeout in seconds.

        """

        super().__init__()        
        self.url = url
        self.timeout = timeout
        self.stop = Event()
        self.name  = None

        self._count_msg = 0
        self._time_recv = None

        self.monitor = None
        self.ws = None

    def run(self):
        
        while not self.stop.is_set():
            self.__go()
        else:
            return

    def __go(self):

        try:
            self.connect()        
            self.listen()
        except Exception as e:
            self.stop.set()
            logger.critical(repr(e))
            try:
                self.disconnect()
            except Exception as e:
                logger.critical(repr(e))

    def __stop(self):
        """

        Disconnect from websocket and stop monitor thread.

        """

        try:
            self.disconnect()
        except Exception as e:
            logger.critical(repr(e))

        try:
            self.monitor.join()
        except Exception as e:
            logger.critical(repr(e))

    def connect(self):
        """

        Connect to websocket.

        """

        logger.info(f'{self.name} is connecting to: {self.url}')

        self.ws = create_connection(self.url, timeout=self.timeout)  

        self.on_open()

    def listen(self):
        """

        Receive new messages from websocket.

        """

        self.monitor = WebsocketMonitor(ws=self.ws, 
                                        time_recv=self._time_recv, 
                                        stop=self.stop)                                        
        self.monitor.daemon = True
        self.monitor.start()

        while not self.stop.is_set():

            try:

                data = self.ws.recv()
                self._time_recv = time.time()
                msg = json.loads(data)                
                self.on_message(msg)  
                self._count_msg += 1

                if self._count_msg % 100 == 0:
                    logger.info(f'Received {self._count_msg} messages.')         

            except Exception as e:

                self.stop.set()
                self.on_error(e)
                logger.critical(repr(e))
                self.monitor.join()

    def disconnect(self):
        """

        Disconnect from websocket.

        """

        if self.ws:
            self.ws.close()    

        logger.warn('Disconnected.')

    def on_open(self):
        """
        
        Called upon initialization of connection.

        Notes
        -----
        In the derived class this method 
        should send a subscription message to 
        the exchange.

        """

        pass

    def on_message(self, msg):
        """

        Called upon receipt of message

        Inputs
        ------
        msg : dict
            The message from the exchange.

        Notes
        -----
        In the derived class this method should
        parse the message and save it to storage.

        """

        pass

    def on_error(self, error):
        """

        Called when error occurs.

        Notes
        -----
        After error disconnect from websocket.

        """

        self.disconnect()    

    def on_close(self):
        """

        Called when the websocket connection closes.

        """

        logger.warn('Websocket closed.')