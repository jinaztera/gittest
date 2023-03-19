import ccxt
import pprint

binance = ccxt.binance()
btc = binance.fetch_ticker("BTC/USDT")
# pprint.pprint(btc)
print("현재가", btc['last'])
