# Logger settings
LOG_FORMAT = '%(asctime)s.%(msecs)03d | %(levelname)10s | %(module)25s | %(funcName)25s | %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Coinbase settings
COINBASE_CFG = {
    'url': 'wss://ws-feed.pro.coinbase.com',
    'channels':  {'trades': 'matches', 'heartbeat': 'heartbeat'},
    'symbols': ['BTC-USD', 'BTC-EUR', 'BTC-GBP',
                'LTC-USD', 'LTC-EUR', 'LTC-GBP',
                'ETH-USD', 'ETH-EUR', 'ETH-GBP',
                'ETH-BTC', 'LTC-BTC'],
    'storage': 'sqlserver',
    'table': '[staging].[coinbase]'
}

# Bitmex settings
BITMEX_CFG = {
    'url': 'wss://www.bitmex.com/realtime',    
    'channels': {'trades': 'trade'},
    'symbols': ['XBTUSD', 'LTCUSD', 'ETHUSD'],
    'storage': 'sqlserver',
    'table': '[staging].[bitmex]'
}

# SQL Server settings
SQL_CFG = {
    'driver': 'SQL Server',
    'server': r'DESKTOP-62E4RH1',
    'database': 'crypto_dev',
    'user': 'PythonScript',
    'password': r'1234',
    'table': None,
    'data_dir': r"C:/Users/Programista/Desktop/crypto_dwh/data"
}