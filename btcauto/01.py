import ccxt
import pprint

binance = ccxt.binance()
markets = binance.load_markets()
jongmok = []
#print(markets)
#print(type(markets))
#print(markets.keys())
#for market in markets.keys():
#    print(market)

#print(len(markets))

for market in markets.keys():
    if market.endswith("USDT"):
        jongmok.append(market)

print(jongmok)
print(jongmok[:10])

# print(markets.keys())
# print(len(markets))
#
# binance = ccxt.binance()
# btc = binance.fetch_ticker("BTC/USDT")
# pprint.pprint(btc)