import requests
import pandas as pd
from numpy import timedelta64
from datetime import datetime

from pprint import pprint

df = pd.DataFrame()
start = datetime.now()
while True:
    # response = requests.get('https://api.binance.com/api/v3/ticker?symbol=ETHUSDT&windowSize=1m').json()
    
    response = requests.get('https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT').json()
    
    data = pd.DataFrame([response])
    df = pd.concat([df,data])
    stop = datetime.now()
    if (stop - start).seconds > 60:
        break

df['openTime'] = pd.to_datetime(df['openTime'],unit='ms') + timedelta64(7,'h')
df['closeTime'] = pd.to_datetime(df['closeTime'],unit='ms') + timedelta64(7,'h')


df

