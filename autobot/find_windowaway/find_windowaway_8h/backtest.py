import keras
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
import ccxt
from sqlalchemy import create_engine
import matplotlib

with open("../api(JKBOT).txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

binance = ccxt.binance(config={
    'apiKey': api_key, #"XTpKrQGSk3GhXzqiEV4OfwGJzmTVcLh8dKGwHo4aQBH4p0mOqPDpIsxdh95tjGVf",
    'secret': secret, #"A0eqZGEWHsyL3NMM6WuDrucIanr7A2YZAnrwXVPhXpf2WGauIANwa5zsoNeNt0hs",
    'enableRateLimit' : True,
    'options': {
        'defaultType': 'future'
    }
})

jongmok= []

markets = binance.load_markets()
for market in markets.keys():
    if market.endswith("/USDT"):# and market != "BCC/USDT" and market != "TUSD/USDT":
        jongmok.append(market)

exchange = ccxt.binance()
exchange.fetch_tickers()
ticker = list(exchange.fetch_tickers().keys())

def md_connect(user, password, db, host, port=3306):
    url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
    engine = create_engine(url).connect()
    return engine

engine = md_connect('root', '1234', 'price_1h', 'localhost')


i=0
score = []
window_list = []
away_list = []
# for window in range(3, 14):
#     for away in range(2, 7):
window = 48
away = 24
# df = pd.DataFrame({"open":[1], "high":[2], "low":[3]})
# print(df)


result = []
for symbol in jongmok[40:60]:
    x_input = []
    y_target = []
    data = pd.read_sql(symbol[:-5].lower(), engine, index_col='datetime') #sql에서 db 받아오기
    data = data
    x_data = data[['open', 'high', 'low', 'close']]
    y_data = data[['close']]

    for i in range(0, len(data) - window - away): #len(data)-window
        mean = x_data[i:i+window].mean()
        std = x_data[i:i+window].std()

        x = (x_data[i:i+window] - mean) / std
        # x['volume'] = (x_data['volume'] - volume_mean) / (volume_std)
        x_input.append(x)

        if y_data['close'][i+window-1] < y_data['close'][i+window+away-1]:
            y_target.append(1)
        else:
            y_target.append(0)

    from tensorflow import keras
    model = keras.Sequential()
    model.add(keras.layers.LSTM(10, activation='relu', input_shape=(window, 4), dropout=0.3))
    model.add(keras.layers.Dense(1, activation='sigmoid'))
    model.load_weights(str(window) + "_" + str(away) + "price_1h.h5")

    x_input = np.array(x_input)
    y_target = np.array(y_target)
    #print(model.predict(x_input))

    # data = pd.read_sql(symbol[:-5].lower(), engine, index_col='datetime', parse_dates=True) #sql에서 db 받아오기
    x_data = pd.DataFrame(data)[window:-away]

    predict_data = pd.DataFrame(model.predict(x_input))
    predict_data['datetime'] = x_data.index
    predict_data.set_index('datetime', inplace=True)
    predict_data.columns = ['ind']

    test = data

    test = test.assign(rate=test['close']) #종가 복사
    test['rate'] = test['rate'].pct_change(periods=away).shift(-away) # away 기간만큼 보유시 수익률 계산
    condition2 = test['rate'] > 0 #조건문
    test = test.assign(real=condition2.map({True:1, False:-1})) # 상승하면 1, 하락하면 -1
    test = test[window+1: -away]

    predict_data = pd.DataFrame(model.predict(x_input))
    predict_data['datetime'] = x_data.index
    predict_data.set_index('datetime', inplace=True)
    predict_data.columns = ['ind']

    test = test.join(predict_data)

    condition1 = test['ind'] > 0.5
    test = test.assign(long_short=condition1.map({True: 1, False: -1}))

    test = test[(test['ind'] > 0.70) | (test['ind'] < 0.30)]

    test = test.assign(answer=test['real']*test['long_short'])
    test = test.assign(profit=test['long_short']*test['rate'])
    test['tot_profit'] = test['profit'].cumsum()

    counts = test['answer'].value_counts()
    average = test['profit'].mean()
    sum =  test['profit'].sum()
    if len(test) > 0:
        print(symbol, counts[1], len(test), counts[1] / len(test), average, sum)
        result.append([symbol, counts[1], len(test), counts[1] / len(test), average, sum])



    # if counts[1] is not None:
    #     print(symbol, len(test), average, sum)
    #     result.append([symbol, len(test), average, sum])
    # else:
    #     print(symbol, 0, 0, average, sum)
    #     result.append([symbol, 0, 0, average, sum])

result = pd.DataFrame(result)
print(result)
result.to_excel('result6535.xlsx')

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(14,10))
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
ax1.plot(test['close'], label='close')
ax2.plot(test['tot_profit'], label='tot_profit')
plt.show()


# import cufflinks as cf
# cf.set_config_file(theme='henanigans', sharing='public', offline=True)
# # test[500:600].iplot(kind="candle", keys=["open", "high", "low", "close"],
# #                     subplots=False)
# # test[500:600].iplot(y=["ind"],
# #                     subplots=False)
# # test[500:600].iplot(y=["tot_profit"],
# #                     subplots=False)
#
# qf=cf.QuantFig(test[50:120], title=symbol, legend='top')
# qf.iplot()
#%%
