import pandas as pd
import numpy as np 
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
df_eth = get_ccxt_data('ETHUSDT', tf= '1m').set_index('timestamp')
df_bnb = get_ccxt_data('BNBUSDT', tf= '1m').set_index('timestamp')


########### PROCESS DATA FOR MODEL ###########

df_bnb = process_data(df_bnb, 'bnb')
df_eth = process_data(df_eth, 'eth')
df = df_bnb.join(df_eth)

del df_bnb
del df_eth

print('total Y == True :',len(df.loc[df['eth_profit'] == 1]))
print('total Y == False :',len(df.loc[df['eth_profit'] == 0]))

df_ml = df.copy()
df_ml = df_ml.dropna()

del df

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
print('\nSIGNAL FOR NEXT 3min :',result)
