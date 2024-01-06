import requests
from time import sleep
from datetime import datetime as dt

from ccxt import binance

from pandas import to_datetime, DataFrame
from numpy import timedelta64



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


def get_ccxt_data(symbol= 'ETHUSDT', tf= '1m', limit= None):
    exchange = binance()
    if limit == None:
        limit = 999999999
    bars = exchange.fetch_ohlcv(symbol, tf, limit= limit)
    df = DataFrame(bars, columns= ['timestamp', 'open', 'high', 'low','close', 'volume'])
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


# dct = {'test': 'value1', 'key2': 'value2'}
# ','.join(str(value) for value in dct.values())
# str(dct)