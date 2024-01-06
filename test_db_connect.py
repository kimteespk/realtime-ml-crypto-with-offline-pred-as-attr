from get_ticker import get_data
from db_connector import *


data = get_data()
db_insert(data)

col, row = db_select('ticker_ethusdt')

print(len(row))