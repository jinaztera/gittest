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

print(jongmok)

exchange = ccxt.binance()
exchange.fetch_tickers()
ticker = list(exchange.fetch_tickers().keys())

def md_connect(user, password, db, host, port=3306):
    url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
    engine = create_engine(url).connect()
    return engine

engine = md_connect('root', '1234', 'price_1d', 'localhost')

i=0
score = []
window_list = []
away_list = []
# for window in range(3, 14):
#     for away in range(2, 7):
window = 14
away = 7
# df = pd.DataFrame({"open":[1], "high":[2], "low":[3]})
# print(df)

x_input = []
y_target = []
for symbol in jongmok[1:2]:
    data = pd.read_sql(symbol[:-5].lower(), engine, index_col='datetime') #sql에서 db 받아오기
    x_data = data[['open', 'high', 'low', 'close']]
    y_data = data[['close']]

    for i in range(1, len(data) - window - away): #len(data)-window
        mean = x_data['low'][i:i+window].mean()
        std = x_data['high'][i:i+window].std()

        x = (x_data[i:i+window] - mean) / std
        # x['volume'] = (x_data['volume'] - volume_mean) / (volume_std)
        x_input.append(x)

        if y_data['close'][i+window-2] < y_data['close'][i+window+away-2]:
            y_target.append(1)
        else:
            y_target.append(0)
print(len(x_input))

import mplfinance as mpf

# mc = mpf.make_marketcolors(
#     up="r",
#     down="b",
#     edge="inherit",
#     wick="inherit"
# )
print(data)

mpf.plot(data=data[:60], type='candle')

# #
# from tensorflow import keras
# model = keras.Sequential()
# model.add(keras.layers.LSTM(10, activation='relu', input_shape=(window, 4), dropout=0.3))
# model.add(keras.layers.Dense(1, activation='sigmoid'))
# model.load_weights('best-dropout-model.h5')
#
# x_input = np.array(x_input)
# y_target = np.array(y_target)
# len(x_data)
# len(x_input)
# #print(model.predict(x_input))
#
# from datetime import datetime
# import backtrader as bt
#
# class SmaCross(bt.Strategy):
#     # list of parameters which are configurable for the strategy
#     params = dict(
#         pfast=10,  # period for the fast moving average
#         pslow=30  # period for the slow moving average
#     )
#
#     def __init__(self):
#         sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
#         sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
#         self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
#
#     def next(self):
#         if not self.position:  # not in the market
#             if self.crossover > 0:  # if fast crosses slow to the upside
#                 self.buy()  # enter long
#
#         elif self.crossover < 0:  # in the market & cross to the downside
#             self.close()  # close long position
#
# import backtrader as bt
# import matplotlib
# cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
#
# data = pd.read_sql(symbol[:-5].lower(), engine, index_col='datetime', parse_dates=True) #sql에서 db 받아오기
# x_data = pd.DataFrame(data)[window+1:-away]
# # print(x_data.index)
# print(len(model.predict(x_input)))
# predict_data = pd.DataFrame(model.predict(x_input))
# predict_data['datetime'] = x_data.index
# predict_data.set_index('datetime', inplace=True)
# predict_data.columns = ['ind']
# print(predict_data)
# combined_data = x_data.join(predict_data)
#
# import backtrader as bt
# import matplotlib
# cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
# # data = pd.read_sql(symbol[:-5].lower(), engine, index_col='datetime', parse_dates=True) #sql에서 db 받아오기
# # Create a data feed
# # data = bt.feeds.data[['close']]
# # predict_data = pd.DataFrame(model.predict(x_input))
# data_feed1 = bt.feeds.PandasData(dataname=combined_data)
# # data_feed2 = bt.feeds.PandasData(dataname=predict_data)
# cerebro.adddata(data_feed1)  # Add the data feed
# # cerebro.adddata(data_feed2)
#
# # cerebro.addstrategy(SmaCross)  # Add the trading strategy
# cerebro.run()  # run it all
# print(cerebro.broker.getvalue())
# cerebro.plot()
# cerebro.plot()  # and plot it with a single command