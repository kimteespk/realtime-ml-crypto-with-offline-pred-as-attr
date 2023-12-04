import ccxt
from pprint import pprint
ex = ccxt.binance()


pprint(ex.fetch_ticker('ETHUSDT'))
