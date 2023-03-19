import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
import ccxt
from sqlalchemy import create_engine

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

database = 'price_8h'

def md_connect(user, password, db, host, port=3306):
    url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
    engine = create_engine(url).connect()
    return engine

engine = md_connect('root', '1234', database, 'localhost')

print("database :" + database + " 에 접속중 입니다")

score = []
window_list = []
away_list = []

for window in range(21, 30, 3):
    for away in range(6, 10, 3):
        print("window : " + str(window), "away : " + str(away))
        x_input = []
        y_target = []
        for symbol in jongmok[0:40]:
            data = pd.read_sql(symbol[:-5].lower(), engine, index_col='datetime') #sql에서 db 받아오기
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

        x_input = np.array(x_input)
        y_target = np.array(y_target)

        train_input, test_input, train_target, test_target = train_test_split(x_input, y_target, test_size=0.5)

        from tensorflow import keras
        model = keras.Sequential()
        model.add(keras.layers.LSTM(10, activation='relu', input_shape=(window, 4), dropout=0.3))
        # model.add(keras.layers.LSTM(10, activation = 'relu'))
        # model.add(keras.layers.Dropout(0, 1))
        # model.add(keras.layers.LSTM(8))
        model.add(keras.layers.Dense(1, activation='sigmoid'))

        # rmsprop = keras.optimizers.RMSprop(learning_rate=1e-4)
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics='accuracy')
        checkpoint_cb = keras.callbacks.ModelCheckpoint(str(window) + '_' +str(away) + database +'.h5', save_best_only=True)
        early_stopping_cb = keras.callbacks.EarlyStopping(patience=20, restore_best_weights=True)
        epochs = 50
        print("window : " + str(window), "away : " + str(away), "에 대해 "+ str(epochs) +"회 학습시작")

        model.fit(train_input, train_target, validation_data=(test_input, test_target), epochs=epochs, verbose=0, callbacks=[checkpoint_cb, early_stopping_cb])
        print(window, away, symbol, model.evaluate(test_input, test_target)[1])

        away_list.append([window, away, model.evaluate(test_input, test_target)[1]])
        tot_score = pd.DataFrame(away_list)
        tot_score.to_excel(str(window) + '_' + str(away) + '_8h.xlsx', index=False)
# print(pd.DataFrame(model.predict(x_input)))
# data.to_excel(symbol[:-5].lower()+'.xlsx', index=False)
# predict.to_excel('predict.xlsx', index=False)