import pandas as pd

# my module
from get_ticker import get_data
from processing import preprocessing_pipeline, MultiKeyShift# ,shift_back_data
from processing import learn_pred, create_metric, create_pipeline



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


lst_raw_data = get_data_dev()


######  EXCLUDE FROM CLASS METHOD
# get data key key
rec = lst_raw_data[0].copy()
data_key = list(rec.keys())

# DUMMY DATAKEY
data_key = ['openPrice', 'highPrice', 'lowPrice', 'lastPrice', 'quoteVolume', 'priceChangePercent']
y_key = 'lastPrice'

## INIT MULTISHEY SHIFT 
multi_key_shift = MultiKeyShift(keys= data_key, window_size= 2, key_exclude= y_key)
## INIT PIPELINE
model_pl = create_pipeline()
## INIT METRIC
model_metric = create_metric()

# CREAT LIST TO COLLECT RESULT
lst_result = []
dct_result = {}

for record in lst_raw_data:
    print(record)
    # print('brefore preprocess :', record)
    prep_rec = preprocessing_pipeline(record)
    data_ = {}
    data_['openPrice'] = prep_rec['openPrice']
    data_['highPrice'] = prep_rec['highPrice']
    data_['lowPrice'] = prep_rec['lowPrice']
    data_['lastPrice'] = prep_rec['lastPrice']
    data_['quoteVolume'] = prep_rec['quoteVolume']
    data_['priceChangePercent'] = prep_rec['priceChangePercent']
    prep_rec = data_
    
    prep_rec = multi_key_shift.update(prep_rec)
    prep_rec = multi_key_shift.get()
    print('\n after preprocess :', prep_rec)
    y = prep_rec.pop(y_key)
    
    # LEARN AND PREDICT
    print('### ', model_pl)
    x, y, y_pred, model_pl, model_metric = learn_pred(x= prep_rec, y= y, pl= model_pl, metric= model_metric)

    # print(prep_rec['closeTime'])
    dct_result = {
        'y_actual': y,
        'y_predict': y_pred,
        'MAE': model_metric
    }
    
    lst_result.append(dct_result)

print(lst_result)

############################# REF ##############################
# #BEFORE EXCLUDE Y
# get x key
# rec = lst_raw_data[0].copy()
# rec.pop('lastPrice')
# data_key = list(rec.keys())

# multi_key_shift = MultiKeyShift(keys= data_key, window_size= 2)

# for record in lst_raw_data:
#     # print('brefore preprocess :', record)
#     prep_rec = preprocessing_pipeline(record)
#     lst_price = prep_rec.pop('lastPrice')
#     print('last price :', lst_price)
    
#     prep_rec = multi_key_shift.update(prep_rec)
#     prep_rec = multi_key_shift.get()
#     prep_rec['lastPrice'] = lst_price
#     print('\n after preprocess :', prep_rec)
    

