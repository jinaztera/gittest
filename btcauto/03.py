import ccxt
import pandas as pd

binance = ccxt.binance()
markets = binance.load_markets()
jongmok = []
rename = []

for market in markets.keys():
    if market.endswith("USDT"):
        jongmok.append(market)

for name in jongmok[:3]:
    rename.append(name[:-5])
print(rename)


for name in jongmok[:3]:


    btc_ohlcv = binance.fetch_ohlcv(name, timeframe='1d', limit=10)

    #print(btc_ohlcv)
    df = pd.DataFrame(btc_ohlcv, columns = ['datetime', 'open', 'high', 'low', 'close', 'volumn'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)

    df.to_excel(name[:-5] + ".xlsx")
