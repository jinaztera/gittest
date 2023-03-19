import ccxt
import pandas as pd
from openpyxl import Workbook
from openpyxl import load_workbook
import jongmok

base_file = "alpha_v5(0109)당일청산.xlsm"
file_name = "Alldata2.xlsx"
data_count = 5
data_day = 1000
#
jongmok.Create_file(base_file, file_name, data_count)

binance = ccxt.binance(config={
    # 'apiKey': api_key, #"XTpKrQGSk3GhXzqiEV4OfwGJzmTVcLh8dKGwHo4aQBH4p0mOqPDpIsxdh95tjGVf",
    # 'secret': secret, #"A0eqZGEWHsyL3NMM6WuDrucIanr7A2YZAnrwXVPhXpf2WGauIANwa5zsoNeNt0hs",
    'enableRateLimit' : True,
    'options': {
        'defaultType': 'future'
    }
})
markets = binance.load_markets()
jongmok = []
rename = []

for market in markets.keys():
    if market.endswith("/USDT"):
        jongmok.append(market)

# for name in jongmok[:10]:
#     rename.append(name[:-5])
print(len(jongmok))

# writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
# #
# for name in jongmok:#[:data_count]:
#     btc_ohlcv = binance.fetch_ohlcv(name, timeframe='1d', since=None, limit=data_day)
#     print(name)
#
#     #print(btc_ohlcv)
#     df = pd.DataFrame(btc_ohlcv, columns = ['datetime', 'open', 'high', 'low', 'close', 'volumn'])
#     df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
#     df.set_index('datetime', inplace=True)
#     print(df)
#
#     with pd.ExcelWriter(file_name, mode='a', engine='openpyxl') as writer:
#         df.to_excel(writer, sheet_name=name[:-5])
#
#
#
#     # df.to_excel("test1.xl")
#     # with pd.ExcelWriter('inventors.xlsx') as writer:
#
#
#
#     # df.to_excel(name[:-5] + ".xlsx")
