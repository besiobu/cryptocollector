from cryptocollector.cfg.config import SQL_CFG
from cryptocollector.persistance.sqlserver import SqlServer
from cryptocollector.websocket.websocket_client import WebsocketClient

class ExchangeFeed(WebsocketClient):
    """

    A class to create exchange feeds.

    """

    def __init__(self, url, storage, channels, symbols, *args, **kwargs):        
        """

        Parameters
        ----------
        url : str
            The url of the websocket.
        storage : str
            The type of storage to use.
        channels : dict
            The channels the websocket will subscribe to.
        symbols : list of str
            Symbols the weboscket will subscribe to.

        """
        super().__init__(url=url)
        self.channels = channels
        self.symbols = symbols
        self.storage = storage
        self.table = None
    
        if storage == 'sqlserver':
            self.storage = storage
            if 'table' in kwargs:
                self.table = kwargs['table']
                SQL_CFG['table'] = self.table 
            else:
                raise RuntimeError(f'Table not specified.')
            self.persistance = SqlServer(**SQL_CFG)
        else:
            raise ValueError(f'{storage} is not supported.')
