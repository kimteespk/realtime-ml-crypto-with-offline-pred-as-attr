import pandas as pd
from time import sleep

# my module
from get_ticker import get_data
from processing import preprocessing_pipeline, MultiKeyShift# ,shift_back_data
from processing import learn_pred, create_metric, create_pipeline


## DEV MODULE
from pandas import to_datetime

################# INTPUT ##################
symbol = 'ETHUSDT'
metric_str = 'MSE'
metric_rolling_size = 60

# DUMMY DATAKEY
data_key = ['openPrice', 'highPrice', 'lowPrice', 'lastPrice', 'priceChangePercent',
            'volume']
y_key = 'lastPrice'
window_size = 60

## READ DATA FROM CSV
# header 
def get_data_dev(path= './dataset/realtime/raw_ethusdt_1m.csv', nrow= 100):
    
    csv_header = ['priceChange', 'priceChangePercent', 
                  'weightedAvgPrice', 'openPrice', 
                  'highPrice', 'lowPrice', 
                  'lastPrice', 'volume', 
                  'quoteVolume', 'openTime', 
                  'closeTime', 'firstId', 
                  'lastId', 'count'
                  ]

    if nrow == 0:
        nrow = 99999999999999999999
    df = pd.read_csv(path, names= csv_header, nrows= nrow)
    # df_eth.head()
    lst_dct = df.to_dict('records')
    print('toto record :', len(lst_dct))
    return lst_dct


# lst_raw_data = get_data_dev(nrow= 0)


## INIT MULTISHEY SHIFT 

multi_key_shift = MultiKeyShift(keys= data_key, window_size= window_size, key_exclude= y_key)
## INIT PIPELINE
model_pl = create_pipeline()
## INIT METRIC
model_metric = create_metric(metric_str, metric_rolling_size)

# CREAT LIST TO COLLECT RESULT
lst_result = []
dct_result = {}

c = 0
# for record in lst_raw_data:
while True: # use when get real data
    record = get_data(symbol, tf= '1m')
    # print(record)
    # print('\nopenPrice brefore preprocess :', record['openPrice'])
    prep_rec = preprocessing_pipeline(record)
    data_ = {key: prep_rec[key] for key in data_key}
    data_['lastPrice'] = record['lastPrice']
    
    prep_rec = data_
    
    prep_rec = multi_key_shift.update(prep_rec)
    prep_rec = multi_key_shift.get()

    y = prep_rec.pop(y_key)

    
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
        metric_str: model_metric
    }
    if  y_pred != None:
        # continue
        lst_result.append(dct_result)
        # print(dct_result['MAE'])
        print(dct_result)
    
    sleep(1)
    c+=1
    if c > window_size + 120:
        break
    
    
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
    mae_values = [result[metric_str].get() for result in lst_result]

    # Plot the line graph with each second as a data point
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot actual and predicted values
    ax1.plot(close_times, y_actual_values, label='Actual', marker='o', linestyle='-', markersize=5)
    ax1.plot(close_times, y_predict_values, label='Predicted', marker='x', linestyle='-', markersize=5)

    # Set labels and title for the first y-axis
    ax1.set_xlabel('Close Time')
    ax1.set_ylabel('Values', color='black')
    ax1.set_title('Actual vs Predicted Values over Time')

    # Show legend for the first y-axis
    ax1.legend(loc='upper left')

    # Create a second y-axis for MAE values
    ax2 = ax1.twinx()
    ax2.plot(close_times, mae_values, label=metric_str, marker='x', linestyle='-', color='red', markersize=5)

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

    
plot_result(lst_result)

############################################################################################################
