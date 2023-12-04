# ref websocket and realtinme plot
# https://www.youtube.com/watch?v=qSTOoGustUc&ab_channel=AndreyIvanov%7CPython

# * This write from git remote
# test2 from main with only save and commit
from time import sleep
import websocket, json
import pandas as pd
import pandas_ta as ta
from numpy import timedelta64

# import talib
# from talib import stream

# websocket doc
# https://pypi.org/project/websocket-client/


bars_timestamp, bars_open, bars_close, bars_high, bars_low, bars_vol= [], [], [], [], [], []
bars = [bars_timestamp, bars_open,bars_high, bars_low, bars_close, bars_vol]
df = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'EMA'])
symbol_bnb_ws = 'btcusdt'
tf = '1m'
# Binance

# https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md
# socket =  'wss://stream.binance.com:9443/ws/@kline_1m'
socket =  f'wss://stream.binance.com:9443/ws/{symbol_bnb_ws}@kline_{tf}'

def calculate_signal(closed_bar):
    # Here, you can use the "closed_bar" data to calculate your signal
    # For example, you can access the candle data as follows:
    cd_time, cd_o, cd_h, cd_l, cd_c, cd_v = closed_bar
    # Perform your signal calculation based on the candle data and any other required variables

    # For demonstration purposes, let's just print a message
    print('Signal calculated for:', cd_time, 'Close price:', cd_c)

def on_message(ws, message):
    global i
    json_msg = json.loads(message)
    candle = json_msg['k']
    is_candle_closed = candle['x']
    cd_time = candle['t'] # t for start, T close time (be careful when use with bitkub)
    cd_o = candle['o']
    cd_h = candle['h']
    cd_l = candle['l']
    cd_c = candle['c']
    cd_v = candle['v']

    cd_time = pd.to_datetime(cd_time, unit='ms') + timedelta64(7, 'h')
    print(cd_time)
    print('Is candle close: ',is_candle_closed)
    print('Current price :',cd_c)
    # ani = FuncAnimation(plt.gcf(), animate, interval= 1000)
    # if is_candle_closed:
    if True:
        # if data is enough, use this array to be an arg for calculate technical indiactor
        # ex,  ta.ema(np.array(bars_close))

        # dont forget to cenvert timestamp withtimedelta before append
        # bars_timestamp.append(int(cd_time))
        # bars_open.append(float(cd_o))
        # bars_high.append(float(cd_h))
        # bars_low.append(float(cd_l))
        # bars_close.append(float(cd_c))
        # bars_vol.append(float(cd_v))
        # print(type(cd_time))
        # print('close candle type :', type(cd_c))
        closed_bar = [cd_time, cd_o, cd_h, cd_l, cd_c, cd_v]

        print('Call closed_bar()')
        calculate_signal(closed_bar)


    # print(bars)
    # print(message)  # print all return msg, no need to loads json
def on_close(ws, close_status_code ,message):
    print('Connection Closed')
    print(df)


print(df)
ws = websocket.WebSocketApp(socket, on_message= on_message, on_close= on_close)

ws.run_forever()


'''
{
  "e": "kline",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "k": {
    "t": 123400000, // Kline start time
    "T": 123460000, // Kline close time
    "s": "BNBBTC",  // Symbol
    "i": "1m",      // Interval
    "f": 100,       // First trade ID
    "L": 200,       // Last trade ID
    "o": "0.0010",  // Open price
    "c": "0.0020",  // Close price
    "h": "0.0025",  // High price
    "l": "0.0015",  // Low price
    "v": "1000",    // Base asset volume
    "n": 100,       // Number of trades
    "x": false,     // Is this kline closed? <<<<<< can query only true to make candle
    "q": "1.0000",  // Quote asset volume
    "V": "500",     // Taker buy base asset volume
    "Q": "0.500",   // Taker buy quote asset volume
    "B": "123456"   // Ignore
  }
}

'''

# making candlesticks



# # Bitkub
# https://github.com/bitkub/bitkub-official-api-docs/blob/master/websocket-api.md
# socket = 'wss://api.bitkub.com/websocket-api/'






# streamname = 'market.trade.thb_btc'
# streamname2 = 'market.ticker.thb_btc'






'''
Fetch btc price from gemini example with "rel" lib for dispatcher to provide
automatic reconnect and keyboard Interrupt
'''

# import websocket
# import _thread
# import time
# import rel

# def on_message(ws, message):
#     print(message)

# def on_error(ws, error):
#     print(error)

# def on_close(ws, close_status_code, close_msg):
#     print("### closed ###")

# def on_open(ws):
#     print("Opened connection")

# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp("wss://api.gemini.com/v1/marketdata/BTCUSD",
#                               on_open=on_open,
#                               on_message=on_message,
#                               on_error=on_error,
#                               on_close=on_close)

#     ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
#     rel.signal(2, rel.abort)  # Keyboard Interrupt
#     rel.dispatch()