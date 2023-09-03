import pandas as pd
import ccxt
import pymysql
from sqlalchemy import create_engine

# with open("../api(JKBOT).txt") as f:
#     lines = f.readlines()
#     api_key = lines[0].strip()
#     secret = lines[1].strip()

binance = ccxt.binance(config={
    'apiKey': 'GCgiv4vJVqgTLTfKGOWcg00489WyxOWrTFxg5KdiBGLKlyJvhd2SZAQUAV5J0aOB',
    'secret': 'M6B6MkZNQxUqtLptdh9et948fw0PDlzATYLTVtxoT5tni1WPA1H6kCZMmPu2vqya',
    'enableRateLimit' : True,
    'options': {
        'defaultType': 'future'
    }
})

jongmok = []

markets = binance.load_markets()
for market in markets.keys():
    if market.endswith("/USDT"):
        jongmok.append(market)


database = "price_1d"

def md_connect(user, password, db, host, port=3306):
    url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
    engine = create_engine(url)
    return engine

engine = md_connect('root', '1234', database, 'localhost')
i=0
for symbol in jongmok:
    print(symbol)
    btc_ohlcv = binance.fetch_ohlcv(symbol=symbol, timeframe='1d', since=None, limit=3000)

    df = pd.DataFrame(data=btc_ohlcv, columns=["datetime", "open", "high", "low", "close", "volume"])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    i += 1
    print(i)
    print(df)
    df.to_sql(symbol[:-5].lower(), engine, if_exists="replace", index=True)
    conn = pymysql.connect(user='root', password='1234', host='localhost', database=database, charset='utf8')
    cur = conn.cursor()
    # cur.execute("CREATE TABLE temp_append as SELECT DISTINCT datetime from "+symbol[:-5].lower())
    # cur.execute("DROP TABLE " + symbol[:-5].lower())
    # cur.execute("ALTER TABLE temp_append RENAME TO " + symbol[:-5].lower())


cursor = conn.cursor(pymysql.cursors.DictCursor)
conn.commit()
conn.close()