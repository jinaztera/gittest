import sqlite3
import pandas as pd
import ccxt
import pymysql
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

exchange = ccxt.binance()
exchange.fetch_tickers()
ticker = list(exchange.fetch_tickers().keys())

"""
USDT_ticker = []
import re
p = re.compile(r'|w+[/]USDT')
for i in ticker:
    if p.match(i) and "UP" not in i and 'DOWN' not in i:
        USDT_ticker.append(i)
print(USDT_ticker)
"""

def md_connect(user, password, db, host, port=3306):
    url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
    engine = create_engine(url).connect()
    return engine

engine = md_connect('root', '0000', 'price_1d', 'localhost')
i=0
tot_profit = 0
for symbol in jongmok[:20]:
    sym = symbol + ":USDT"
    #btc_ohlcv = binance.fetch_ohlcv(symbol=symbol, timeframe='1d', since=None, limit=10000)
    df = pd.read_sql(symbol[:-5].lower(), engine, index_col='datetime') #sql에서 db 받아오기

    df['3d_ma'] = df['close'].rolling(window=3).mean()
    df['12d_ma'] = df['close'].rolling(window=12).mean()

    profit = 0
    buy = 0
    short = 0
    position = ""

    for i in range(len(df)):
        if df['3d_ma'].iloc[i] > df['12d_ma'].iloc[i] and df['3d_ma'].iloc[i-1] < df['12d_ma'].iloc[i-1]:
            if position == 'short':
                if i + 1 == len(df):
                    profit += 100 * (buy_price - df['open'].iloc[i]) / buy_price
                    buy += 1
                    break
                profit += 100 * (buy_price - df['open'].iloc[i+1]) / buy_price
                buy += 1

            buy_price = df['open'].iloc[i + 1]
            position = 'long'

        elif df['3d_ma'].iloc[i] < df['12d_ma'].iloc[i] and df['3d_ma'].iloc[i-1] > df['12d_ma'].iloc[i-1]:
            if position == 'long':
                if i + 1 == len(df):
                    profit += 100 * (df['open'].iloc[i] - buy_price) / buy_price
                    buy += 1
                    break
                profit += 100 * (df['open'].iloc[i+1] - buy_price) / buy_price
                short += 1
            buy_price = df['open'].iloc[i + 1]
            position = 'short'

    tot_profit += profit
    print(buy, short, "Profit: ", profit)
    #print(df['close'].iloc[3])

print(tot_profit)
"""
    for index, row in df.iterrows():
        if (row['3d_ma'] > row['12d_ma']) and not holding:
            #print(index)
            # Buy
            holding = True
            buy_price = row['close']
        elif (row['3d_ma'] < row['12d_ma']) and holding:
            # Sell
            holding = False
            profit += (row['close'] - buy_price) / buy_price
            count += 1
"""


