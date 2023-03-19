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

def md_connect(user, password, db, host, port=3306):
    url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
    engine = create_engine(url).connect()
    return engine

engine = md_connect('root', '0000', 'price_1d', 'localhost')
i=0
for symbol in jongmok[:5]:
    sym = symbol + ":USDT"
    btc_ohlcv = binance.fetch_ohlcv(symbol=symbol, timeframe='1d', since=None, limit=10000)
    df = pd.read_sql(symbol[:-5].lower(), engine, index_col='datetime') #sql에서 db 받아오기

    df['3d_ma'] = df['close'].rolling(window=3).mean()
    df['12d_ma'] = df['close'].rolling(window=12).mean()

    holding = False
    profit = 0
    count = 0


    for index, row in df.iterrows():
        if (row['3d_ma'] > row['12d_ma']) and not holding:
            print(index)
            # Buy
            holding = True
            buy_price = row['close']
        elif (row['3d_ma'] < row['12d_ma']) and holding:
            # Sell
            holding = False
            profit += (row['close'] - buy_price) / buy_price
            count += 1

    print(index, count, "Profit: ", profit)

#conn = pymysql.connect(user='root', password='0000', host='localhost', database='price_1d', charset='utf8')
#cursor = conn.cursor(pymysql.cursors.DictCursor)
#conn.commit()
#conn.close()