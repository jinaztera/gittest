import sqlite3
import pandas as pd
import ccxt
import pymysql
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import sys
import logging
import numpy as np
from keras.models import Sequential
# layers는 모델을 구성하는 층, 신경망
from keras.layers import Dense, LSTM, BatchNormalization

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

def md_connect(user, password, db, host, port=3306):
    url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
    engine = create_engine(url).connect()
    return engine

engine = md_connect('root', '0000', 'price_1d', 'localhost')
i=0
tot_profit = 0
for symbol in jongmok[:1]:
    sym = symbol + ":USDT"
    #btc_ohlcv = binance.fetch_ohlcv(symbol=symbol, timeframe='1d', since=None, limit=10000)
    df = pd.read_sql(symbol[:-5].lower(), engine, index_col='datetime') #sql에서 db 받아오기

df_temp = df[['volume', 'close']].values
scaler = MinMaxScaler()
sc_df = scaler.fit_transform(df_temp)
print(sc_df)

N_STEPS = 10

X=[]
Y=[]

for i in range(len(sc_df)-N_STEPS):
    X.append(sc_df[i:i+N_STEPS])
    Y.append(sc_df[i+N_STEPS, [1]])
print(X)
print(Y)

X = np.array(X)
Y = np.array(Y)
print(X)
print(Y)

X_train, X_test, Y_train, Y_test = \
    train_test_split(X, Y, test_size=0.2, shuffle=False)

model = Sequential()
model.add(LSTM(units=32, input_shape=X_train.shape[1:]))
# Dense : 출력층 값이 1개가 나온다. 우리가 예측한 주가, 이것을 통해서 오차를 구하고 학습을 해서 모델을 만드는 것
model.add(Dense(units=1))


model.compile(loss='mae', optimizer='adam')
# X_train, y_train은 train할 데이터, X_test, y_test는 실제로 테스트 할 데이터
# epochs : 몇번 테스트를 할 것인지
# batch_size: 각 학습 반복에 사용할 데이터 샘플 수
#             ex) 1000개 데이터를 batch_size =10로 설정하면, 100개의 step을 통해 1epoch를 도는 것
#                 즉, 1epoch(학습1번) = 10(batch_size) * 100(step)
#               batch_size가 커지면 한번에 많은 양을 학습하기 때문에 train 과정이 빨라진다. 그러나 컴퓨터 메모리 문제로 나눠서 학습하는 것
h=model.fit(X_train, Y_train, batch_size=32, epochs = 100, validation_data= (X_test, Y_test), verbose=1)

# 위에서 만든 모델로 예측 (3차원 데이터를 넣어줘야함)
pred_y = model.predict(X_test)

plt.figure(figsize=[15,6])
# ravel() 1차원으로 변경
# pred_y는 예측한 값
plt.plot(pred_y.ravel(), 'r-', label = 'pred_y')
# y_test는 실제 값
plt.plot(Y_test.ravel(), 'b-', label = 'y_test')
# plt.plot((pred_y-y_test).ravel(), 'g-', label = 'diff*10')

plt.legend() # 범례 표시
plt.title("BTC")
plt.show()

# history : 학습한 history를 저장하고 있음
plt.plot(h.history['loss'], label = 'loss')
plt.legend()
plt.title('Loss')
# x축이 epochs / y축이 loss
plt.show()
