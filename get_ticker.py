import requests
from time import sleep
from datetime import datetime as dt

from ccxt import binance

from pandas import to_datetime, DataFrame
from numpy import timedelta64

# FOR INSERT TO DB
from db_connector import *

# from configparser import ConfigParser

# config = ConfigParser()
# config.read('config.ini')
# cfg = config['DB']
# user = cfg['user']
# pwd = cfg['pwd']
# db_name = cfg['db_name']
# host = cfg['host']
# port = cfg['port']



# get data 1m 5m 15m 1h 1d 
def get_data(symbol= 'ETHUSDT', tf= '1m'):
    symbol = symbol.upper()
    endpoint = f'https://api.binance.com/api/v3/ticker?symbol={symbol}&windowSize={tf}'
    res = requests.get(endpoint).json()
    res = {k: float(v) for k, v in res.items() if k != 'symbol'}
    
    return res
    
    
def append_to_file(row_data: str, symbol, window, base_path= './dataset/realtime/raw_'):
    if isinstance(row_data, dict):
        row_data = ','.join(str(value) for value in row_data.values())
        
    if row_data[-1] != '\n':
        row_data += '\n'
    path = base_path + f'{symbol.lower()}_{window}.csv'
    with open(path, 'a') as f:
        f.write(row_data)
    print(f'{dt.now().time()} append {symbol} data to {path}')
    return True


def get_ccxt_data(symbol= 'ETHUSDT', tf= '1m', limit= None, insert_db= False):
    exchange = binance()
    if limit == None:
        limit = 999999999
    bars = exchange.fetch_ohlcv(symbol, tf, limit= limit)
    df = DataFrame(bars, columns= ['timestamp', 'open', 'high', 'low','close', 'volume'])
    if symbol == 'ETHUSDT':
        my_orm_table = OhlcvETH
    elif symbol == 'BNBUSDT':
        my_orm_table = OhlcvBNB
    if insert_db == True:
        # my_orm_table = OhlcvETH
        table_name = 'ohlcv_' + symbol.lower()
        my_orm_table.__tablename__ = table_name
        print('Ohlcv.__tablename__\t\t',my_orm_table.__tablename__)
        
        engine = my_engine()#user, pwd, host, port, db_name)
        col, lst_row = db_select(table_name, engine= engine)
        
        # SELECT ONLY NEW DATA TO INSERT
        if len(lst_row) > 0:
            newest_db_data_ts = lst_row[-1][0] 
            new_data_for_db = df.loc[df['timestamp'] > newest_db_data_ts].to_dict('records')
        else:
            new_data_for_db = df.to_dict('records')
        # print(new_data_for_db)
        # print(new_data_for_db[0])
    
            
        db_insert(new_data_for_db, engine= engine, ORMclass= my_orm_table)
        
    df['timestamp'] = to_datetime(df['timestamp'], unit= 'ms') + timedelta64(7, 'h')
    
    return df
    


if __name__ == '__main__':
    # garbage collector
    import gc
    gc.enable()
    gc.collect()
    import sys
    # print(f'RUNNING :{sys.argv[0]}')
    args = sys.argv
    symbol = args[1]
    window = args[2]
    print(f'Start get ticker :{symbol} window size :{window}')
    while True:
        try:
            res = get_data(symbol= symbol, tf= window)
            append_to_file(row_data= res, symbol= symbol, window= window)
            del res
        except Exception as e:
            print(e)
            pass
        sleep(1)

