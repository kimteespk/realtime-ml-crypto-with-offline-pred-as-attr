# from river.tree import DecisionTreeClassifier
from river.tree import ExtremelyFastDecisionTreeClassifier 
from river import compose
from river.preprocessing import StandardScaler
from numpy import timedelta64
import pandas as pd
import websocket
import json

# model = compose.Pipeline(
#     ('scale', StandardScaler()),
#     ('clf', ExtremelyFastDecisionTreeClassifier())
# )

model = ExtremelyFastDecisionTreeClassifier(
    grace_period=100,
    delta=1e-5,
    # nominal_attributes=['elevel', 'car', 'zipcode'],
    min_samples_reevaluate=100
)

# Initialize your historical data DataFrame
# Assuming df is your historical DataFrame with features and labels
# Replace 'your_label_column' with the actual column containing your labels (buy/sell signals)
df = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'label'])

symbol_bnb_ws = 'btcusdt'
tf = '1m'
socket = f'wss://stream.binance.com:9443/ws/{symbol_bnb_ws}@kline_{tf}'

def calculate_signal(closed_bar):
    # Assuming your label is in the 'label' column
    if closed_bar[4] > closed_bar[2]:
        return 1
    else:
        return 0 
    # return closed_bar[-1]

def on_message(ws, message):
    json_msg = json.loads(message)
    candle = json_msg['k']
    is_candle_closed = candle['x']
    cd_time = pd.to_datetime(candle['t'], unit='ms') + timedelta64(7, 'h')
    cd_o = float(candle['o'])
    cd_h = float(candle['h'])
    cd_l = float(candle['l'])
    cd_c = float(candle['c'])
    cd_v = float(candle['v'])

    closed_bar = [cd_time, cd_o, cd_h, cd_l, cd_c, cd_v, ]
    print('current bar :', closed_bar)

    # Calculate signal and update model
    label = calculate_signal(closed_bar)
    xi_dict = dict(enumerate(closed_bar[:-1]))  # Exclude the label for training
    model.learn_one(xi_dict, label)

    # Real-time prediction example
    new_data_point_dict = dict(enumerate(closed_bar[:-1]))  # Exclude the label for prediction
    prediction = model.predict_one(new_data_point_dict)

    print('Real-time Prediction:', prediction)
    
def on_close(ws, close_status_code ,message):
    print('Connection Closed')
    print(df)

# Other functions remain unchanged

ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)
ws.run_forever()
