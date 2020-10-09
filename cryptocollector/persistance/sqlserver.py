import time
import urllib
import datetime
from json import dump
from random import randint

from sqlalchemy import create_engine

from cryptocollector.persistance.persistor import Persistor
from cryptocollector.utils.utils import setup_logger

logger = setup_logger(name=__name__)

class SqlServer(Persistor):
    """

    A class to persist messages to SQL Server database.

    """

    def __init__(self, 
                 driver, 
                 server, 
                 database, 
                 user,
                 password, 
                 table,
                 data_dir):
        """

        Parameters
        ----------
        database : str
            Name of SQL Server database.
        driver : str
            Microsoft driver.
        user : str
            SQL Server user with data writer permissions.
        password : str
            SQL Server user password.
        server : str
            _name of SQL Server server.
        data_dir : str
            Path to use if write to database fails.     

        Notes
        ------
        Inputs must make a valid connection string.

        """

        super().__init__()

        self.driver = driver
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.table = table
        self.data_dir = data_dir
        self.engine = self.__make_engine()

    def __del__(self):
        
        if self.engine is not None:
            logger.warn('Disposing of connection pool.')
            try:
                self.engine.dispose()
            except KeyError as e:
                logger.warn(e)

    def __make_engine(self):
        """
        
        Create SQL Server engine.

        """

        conn_string = self.__create_conn_string()

        # logger.info(f'connection string: {conn_string}.')        
        logger.info(f'Will write to database: {self.database}.')
        logger.info(f'Will write to table: {self.table}.')

        engine = create_engine(conn_string)

        return engine

    def __create_conn_string(self):
        """

        Create connection string to sql server.

        """

        conn_params =  'DRIVER={' + self.driver +'};'
        conn_params += 'SERVER=' + self.server + ';'
        conn_params += 'DATABASE=' + self.database + ';'
        conn_params += 'UID=' + self.user + ';'
        conn_params += 'PWD=' + self.password 

        conn_params = urllib.parse.quote_plus(conn_params)
        conn_string = f'mssql+pyodbc:///?odbc_connect={conn_params}'

        return conn_string        

    def write(self, msg):
        """

        Persist message from websocket.

        Parameters
        ----------
        msg : dict
            Message from exchange.
        table : str
            name of table in database.

        Notes
        -----
        1. Try to write to sql database.
        2. In case of error write to json on disk.

        """

        try:
            self._write_msg_to_db(msg=msg)
        except Exception as e:
            logger.critical(e)
            try:
                self._write_msg_to_json(msg=msg)
            except Exception as e:
                logger.critical(e)

    def _write_msg_to_db(self, msg):
        """

        Write message from websocket to database.

        Parameters
        ----------
        msg : dict
            Message from exchange.
        table : str
            name of table in database.        

        Notes
        -----
        The messages from the websocket a received as 
        dictionaries and are converted into a 
            `INSERT INTO (cols) VALUES (values)`
        transact sql query.

        """

        msg['timestamp_script'] = str(datetime.datetime.now())

        columns = list()
        values = list()

        for k,v in msg.items():
            columns.append(str(k))
            values.append("'" + str(v) + "'")

        columns = ', '.join(columns)        
        values = ', '.join(values)
        query = f""" INSERT INTO {self.table} ({columns}) VALUES ({values}) """

        self.engine.execute(query)

    def _write_msg_to_json(self, msg):
        """

        Write message from websocket to json.

        Parameters
        ----------
        msg : dict
            Message from exchange.
            
        """

        path = self.__make_path_file()

        with open(path, 'w') as f:
            dump(msg, f)

    def __make_path_file(self):
        """

        Create path to file.

        Notes
        -----
        The file name is constructed in 3 steps:
        1. The name of the table.
        2. A unix timestamp with milisecond precision.
        3. A random integer to minimize collisions.

        """

        table = self.table.replace('.', '')

        path = f'{self.data_dir}/{table}_'
        path += f'{str(int(time.time() * 1000))}_'
        path += f'{str(randint(1, 10 ** 6))}.txt'

        return path        
