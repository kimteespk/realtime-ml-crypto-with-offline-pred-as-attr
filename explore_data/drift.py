import pandas as pd


def get_data_dev(path= './dataset/realtime/raw_ethusdt_1m.csv', nrow= 100, result= 'dict'):
    
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
    if result == 'df':
        return df
    # df_eth.head()
    lst_dct = df.to_dict('records')
    print('total record :', len(lst_dct))
    return lst_dct


path = r'E:\DADS\DADS6005_Realtime_Analytics\realtime-ml-kafka-crypto\dataset\realtime\raw_ethusdt_1m.csv'
df_raw = get_data_dev(path, nrow=0, result= 'df')
# df_raw.head(1)

lst_data = df_raw[['priceChangePercent', 'openPrice', 'highPrice', 'lowPrice', 'lastPrice', 'volume']].to_dict('records')


import matplotlib.pyplot as plt
from matplotlib import gridspec

import matplotlib.pyplot as plt
from matplotlib import gridspec

def plot_data(data, dist_a, drifts=None):
    fig = plt.figure(figsize=(7, 3), tight_layout=True)
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
    ax1, ax2 = plt.subplot(gs[0]), plt.subplot(gs[1])
    ax1.grid()
    ax1.plot(data, label='Stream')
    ax2.grid(axis='y')
    ax2.hist(dist_a, label=r'$dist_a$')
    
    if drifts is not None:
        for drift_detected in drifts:
            ax1.axvline(drift_detected, color='r', linestyle='--')

    # Additional settings for better visualization
    ax1.legend()
    ax1.set_xlabel('Data Point')
    ax1.set_ylabel('Feature Values')
    ax1.set_title('Stream Data with Drift Detection')
    
    ax2.legend()
    ax2.set_xlabel('Histogram')
    ax2.set_title('Distribution of dist_a')

    plt.show()

    
from river import drift


drift_detector = drift.ADWIN()
drifts = []

for i, val in enumerate(lst_data):
    drift_detector.update(val['lastPrice'])   # Data is processed one sample at a time
    if drift_detector.drift_detected:
        # The drift detector indicates after each sample if there is a drift in the data
        print(f'Change detected at index {i} lastPrice :{val["lastPrice"]}')
        drifts.append(i)
        drift_detector._reset()  # As a best practice, we reset the detector

data = [x['lastPrice'] for x in lst_data]
plot_data(data, data ,drifts)