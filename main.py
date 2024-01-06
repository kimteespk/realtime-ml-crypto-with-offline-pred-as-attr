insert_to_db =  True

###############################################################
################### OFFLINE MODEL #############################
###############################################################

import matplotlib.pyplot as plt
import pandas_ta as ta

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay 
from sklearn.metrics import f1_score, precision_score, accuracy_score, recall_score

from get_ticker import get_ccxt_data



def process_data(df, prefix= ''):
    df[prefix+'_rsi_indi'] = df.ta.rsi(length= 14) > 50
    # df['obv'] = df.ta.obv()
    # df['obv_ma_f'] = ta.ema(df['obv'], 20)
    df[prefix+'_vol_indi'] = ta.ema(df.ta.obv(), 20) > ta.ema(df.ta.obv(), 40)

    if prefix == 'eth':
        df[prefix+'_price_chg'] = (df['close'] - df['close'].shift(-1)) / df['close'].shift(-1)
        df[prefix+'_profit'] = df[prefix+'_price_chg'] > 0 
        df = df[['open','high', 'low' ,prefix+'_rsi_indi', prefix+'_vol_indi', prefix+'_profit']]
    else:
        df[prefix+'_price_chg'] = (df['close'] - df['close'].shift(-1)) / df['close'].shift(1)
        df[prefix+'_price_up'] = df[prefix+'_price_chg'] > 0 
        df = df[[prefix+'_rsi_indi', prefix+'_vol_indi', prefix+'_price_up']]
    df_result  = df.dropna()
    return df_result

########### GET BATCH DATA ###############
df_eth = get_ccxt_data('ETHUSDT', tf= '1m', insert_db= insert_to_db).set_index('timestamp')
df_bnb = get_ccxt_data('BNBUSDT', tf= '1m', insert_db= insert_to_db).set_index('timestamp')


########### PROCESS DATA FOR MODEL ###########

df_bnb = process_data(df_bnb, 'bnb')
df_eth = process_data(df_eth, 'eth')
df = df_bnb.join(df_eth)



print('total Y == True :',len(df.loc[df['eth_profit'] == 1]))
print('total Y == False :',len(df.loc[df['eth_profit'] == 0]))

df_ml = df.copy()
df_ml = df_ml.dropna()


y = df_ml.pop('eth_profit')
X = df_ml

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, random_state= 44)

############# MODEL ############
rf = RandomForestClassifier(n_estimators= 100, max_depth= 6, random_state= 14)
# train
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

##### EVALUATION 
cm_result = confusion_matrix(y_test, y_pred)
print('CONFUSION METRIC :\n',cm_result)

# disp = ConfusionMatrixDisplay(cm_result)
# disp.plot()
# plt.show()

f1 = f1_score(y_test, y_pred)
prcision = precision_score(y_test, y_pred)
acc = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)


##### GET NEW DATA TO PREDICT FOR ONLINE ML
def get_new_data_and_pred( model= rf):
    # global get_ccxt_data
    _df_eth = get_ccxt_data('ETHUSDT', tf= '1m', limit=42).set_index('timestamp')
    _df_bnb = get_ccxt_data('BNBUSDT', tf= '1m', limit= 42).set_index('timestamp')
    _df_bnb = process_data(_df_bnb, 'bnb')
    _df_eth = process_data(_df_eth, 'eth')
    _df = _df_bnb.join(_df_eth)
    _df = df.iloc[-1:, :].drop(['eth_profit'], axis= 1)
    new_data = list(_df.values)
    result = model.predict(new_data)
    return result[0]
        
        
result = get_new_data_and_pred()
print('\n\n\nSIGNAL FOR NEXT 3min :',result)



####################################################################
###################### ONELINE MODEL ###############################
####################################################################
import pandas as pd
from time import sleep
from datetime import datetime as dt

# my module
from get_ticker import get_data
from processing import preprocessing_pipeline, MultiKeyShift# ,shift_back_data
from processing import learn_pred, create_metric, create_pipeline, create_agg, transform_agg
from db_connector import *

# from configparser import ConfigParser


## DEV MODULE
from pandas import to_datetime

################# INTPUT ##################
symbol = 'ETHUSDT'
metric_str = 'RMSE'
metric_rolling_size = 60

# insert_to_db =  False

# db param
table_name_prefix = 'ticker_'

# DUMMY DATAKEY
data_key = ['openPrice', 'highPrice', 'lowPrice', 'lastPrice', 'priceChangePercent',
            'volume',
            'hour',
            'eth_1h_vol',
            'btc_price',
            'btc_1h_vol',
            'signal_from_offline'
            ]
y_key = 'lastPrice'
window_size = 300

## READ DATA FROM CSV
# header 
# def get_data_dev(path= './dataset/realtime/raw_ethusdt_1m.csv', nrow= 100):
    
#     csv_header = ['priceChange', 'priceChangePercent', 
#                   'weightedAvgPrice', 'openPrice', 
#                   'highPrice', 'lowPrice', 
#                   'lastPrice', 'volume', 
#                   'quoteVolume', 'openTime', 
#                   'closeTime', 'firstId', 
#                   'lastId', 'count'
#                   ]

#     if nrow == 0:
#         nrow = 99999999999999999999
#     df = pd.read_csv(path, names= csv_header, nrows= nrow)
#     # df_eth.head()
#     lst_dct = df.to_dict('records')
#     print('toto record :', len(lst_dct))
#     return lst_dct


# lst_raw_data = get_data_dev(nrow= 3600)#0)

############# CONFIG ####################
# config = ConfigParser()
# config.read('config.ini')
# cfg = config['DB']
# user = cfg['user']
# pwd = cfg['pwd']
# db_name = cfg['db_name']
# host = cfg['host']
# port = cfg['port']

############# INITIAL INSTANCE ################
## INIT MULTISHEY SHIFT 
multi_key_shift = MultiKeyShift(keys= data_key, window_size= window_size, key_exclude= y_key)
## INIT PIPELINE
model_pl = create_pipeline()
## INIT METRIC
model_metric = create_metric(metric_str, metric_rolling_size)
## INIT AGG FUNCTION
transformer_agg = create_agg()

_current_min = None

####### DATABASE
table_name = table_name_prefix + symbol.lower()
TickerEthusdt.__tablename__ = table_name

engine = my_engine()#user, pwd, host, port, db_name)


# CREAT LIST TO COLLECT RESULT
lst_result = []
dct_result = {}

# for model improvement
lst_x_y = []

c = 0
# for record in lst_raw_data: # from dataframe
while True: # use when get real data
    print(str(dt.now()))
    print('#'*70)
    print('time :',str(dt.now()))
    
    # GET ETH DATA 1m
    record = get_data(symbol, tf= '1m')
    # INSERT RAW DATA TO DB
    if insert_to_db == True:
        db_insert(record, engine= engine)
        
    # GET ETH DATA 1h
    record['eth_1h_vol'] = get_data(symbol, tf= '1h')['volume']
    # GET BTC DATA
    btc_record = get_data('BTCUSDT', tf= '1h')
    record['btc_price'] = btc_record['lastPrice']
    record['btc_1h_vol'] = btc_record['volume']
    # ADD SIGNAL FROM OFFLINE MODEL
    record['signal_from_offline'] = result
    

        
    # print(record)
    # print('\nopenPrice brefore preprocess :', record['openPrice'])
    prep_rec = preprocessing_pipeline(record)
    data_ = {key: prep_rec[key] for key in data_key}
    data_['lastPrice'] = record['lastPrice']
    
    prep_rec = data_
    
    prep_rec = multi_key_shift.update(prep_rec)
    prep_rec = multi_key_shift.get()

    y = prep_rec.pop(y_key)
    ## AGGREGATE DATA
    prep_rec = transform_agg(prep_rec, transformer_agg)
    print('\nDATA AFTER PROCESS :\n',prep_rec)
    
    ## LEARN AND PREDICT
    try:
        _x, y, y_pred, model_pl, model_metric = learn_pred(x= prep_rec, y= y, pl= model_pl, metric= model_metric)
    except Exception as e:
        print(e)
        continue
    

    dct_result = {
        'closeTime': record['closeTime'],
        'y_actual': y,
        'y_predict': y_pred,
        metric_str: model_metric.get()
    }
    if  y_pred != None:
        # continue
        lst_result.append(dct_result)
        # print(dct_result['MAE'])
        print(dct_result)
    
    x_clone = _x.copy()
    x_clone.update(dct_result)
    lst_x_y.append(x_clone)
    
    sleep(1)
    c+=1
    if c > window_size + 600:
        break
    
    # if (c % 60) == 0:
    #     result = get_new_data_and_pred()
    #     print('\nSIGNAL FOR NEXT 3min :',result)
        
    
    _new_min = dt.now().minute
    if _current_min != _new_min:
        _current_min = _new_min
        result = get_new_data_and_pred()
        print('\n NEW ATTRIBUTE FROM OFFLINE MODEL FOR NEXT 3min , -> :',result)
        # break
    # else:
    #     if 
        
    
    
############################ END MODEL ##############################
#--------------------------------------------------------------------#
 
########################## PLOT ######################################

import matplotlib.pyplot as plt
from pandas import to_datetime
import matplotlib.dates as mdates

def plot_result(result):
    global window_size
    # Assuming lst_result is a list of dictionaries
    # Extract 'closeTime', 'y_actual', 'y_predict', and 'MAE' from each dictionary
    close_times = [to_datetime(result['closeTime'], unit='ms') for result in lst_result]
    y_actual_values = [result['y_actual'] for result in lst_result]
    # y_predict_values = pd.Series([x['y_predict'] for x in lst_result]).shift(window_size).tolist()
    y_predict_values = [result['y_predict'] for result in lst_result]
    mae_values = [result[metric_str] for result in lst_result]

    # Plot the line graph with each second as a data point
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot actual and predicted values
    ax1.plot(close_times, y_actual_values, label='Actual', marker='o', linestyle='-', markersize=1)
    ax1.plot(close_times, y_predict_values, label='Predicted', marker='x', linestyle='-', markersize=1)

    # Set labels and title for the first y-axis
    ax1.set_xlabel('Close Time')
    ax1.set_ylabel('Values', color='black')
    ax1.set_title('Actual vs Predicted Values over Time')

    # Show legend for the first y-axis
    ax1.legend(loc='upper left')

    # Create a second y-axis for MAE values
    ax2 = ax1.twinx()
    ax2.plot(close_times, mae_values, label=metric_str, marker='x', linestyle=(0, (1, 1)), color='red', markersize=1, alpha= 0.5)

    # Set labels and title for the second y-axis
    ax2.set_ylabel(metric_str, color='red')

    # Show legend for the second y-axis
    ax2.legend(loc='upper right')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Set the x-axis format to show date and time
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

    # Show the plot
    plt.show()

# CALCULATE ERROR
lst_error = [x[metric_str] for x in lst_result]
avg_error = sum(lst_error) / len(lst_error)


# WRITE RESULT TO CSV
# import csv

# keys = lst_x_y[0].keys()

# with open('result/amf_n10_step5.csv', 'w', newline='') as output_file:
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(lst_x_y)

print(f'AVERAGE ERROR :{avg_error:.6f}')
plot_result(lst_result)

############################################################################################################
