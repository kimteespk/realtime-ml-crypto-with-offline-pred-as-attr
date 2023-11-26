
import pandas as pd
import pandas_ta as ta # technical indicator
from numpy import timedelta64 # convert timezone
import ccxt #

lst_symbol = ['ETHUSDT', 'BTCUSDT']#, 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 'SOLUSDT']
start_date = '2023-01-01 00:00:00'
timeframe = '1m'

exchange = ccxt.binance()

from_ts = exchange.parse8601(start_date)#'2023-01-01 00:00:00')
from_ts

for symbol in lst_symbol:
    print('\n\nSYMBOL :', symbol)
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since= from_ts, limit=1000)
    while True:
        from_ts = bars[-1][0]
        new_bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since= from_ts, limit=1000)
        bars.extend(new_bars)
        if len(new_bars) != 1000:
            break
    
    
        

    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low','close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit= 'ms') + timedelta64(7, 'h')
    print(df.head(1))
    df.to_csv(f'./dataset/tf{timeframe}_{symbol}_{start_date.split(" ")[0]}-_{df.iloc[-1][0].date()}.csv')

# from_ts = exchange.parse8601('2023-01-01 00:00:00')
# ohlcv_list = []
# ohlcv = exchange.fetch_ohlcv('BTC/USDT', '5m', since=from_ts, limit=1000)
# ohlcv_list.append(ohlcv)
# while True:
#     from_ts = ohlcv[-1][0]
#     new_ohlcv = exchange.fetch_ohlcv('BTC/USDT', '5m', since=from_ts, limit=1000)
#     ohlcv.extend(new_ohlcv)
#     if len(new_ohlcv)!=1000:
#     	break

# str(df.iloc[-1][0].date())
    
# df.to_csv('./ethusdt_5m.csv')
# df['og_fast_ema'] = ta.ema(df['close'], 3)
# df['og_slow_ema'] = ta.ema(df['close'], 5)


# while True:
#     print(exchange.fetch_ohlcv('BTCUSDT', timeframe='1m', limit=1)[-1])


