import ccxt
import pprint
import math
import pandas as pd
from datetime import datetime

with open("api(JKBOT).txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

print(api_key)
print(secret)

binance = ccxt.binance(config={
    'apiKey': api_key, #"XTpKrQGSk3GhXzqiEV4OfwGJzmTVcLh8dKGwHo4aQBH4p0mOqPDpIsxdh95tjGVf",
    'secret': secret, #"A0eqZGEWHsyL3NMM6WuDrucIanr7A2YZAnrwXVPhXpf2WGauIANwa5zsoNeNt0hs",
    'enableRateLimit' : True,
    'options': {
        'defaultType': 'future'
    }
})
markets = binance.load_markets()
# usdt_balance = 100
# symbol = "SOL/USDT"
# coin = binance.fetch_ticker(symbol)
# cur_price = coin['last']
# min_units = markets[symbol]['limits']['market']['min']
# # print(math.floor(100 * 1000) / cur_price / 1000)
# print(symbol, cur_price, min_units, 1/min_units, math.floor(100 * 1000 / cur_price) / 1000)
# print(1/min_units)
# print(math.floor((100 * 1000 / cur_price) / 1000))
# def cal_amount(usdt_balance, cur_price):
#     amount = math.floor((usdt_balance * 1/min_units) / cur_price) / (1/min_units)
#     return amount
#
# print(cal_amount(usdt_balance, cur_price))
# amount = cal_amount(usdt_balance, cur_price)
#
# def cal_amount(usdt_balance, cur_price):
#     # portion = 0.1
#     # usdt_trade = usdt_balance * portion
#     amount = math.floor((usdt_trade * 1000000) / cur_price) / 1000000
# history_df = pd.read_excel("trade_history.xlsx")
# d = binance.parse8601()
# fetchTrades = binance.fetch_my_trades(symbol='BTC/USDT', since=d, limit=1000, params={'order':'asc'})
# pprint.pprint(fetchTrades)
# #     return amount
# pprint.pprint(fetchTrades[-1]['cost'])
# pprint.pprint(fetchTrades[-1]['datetime'][:16])
#
# new_data = [fetchTrades[-1]['datetime'][:16], 'BTC/USDT', 'long', fetchTrades[-1]['price'],
#                                 fetchTrades[-1]['amount'], float(fetchTrades[-1]['price']) * float(fetchTrades[-1]['amount'])]
# history_df.loc[len(history_df)] = new_data
#
# print(new_data)
#
#
jongmok = []
markets = binance.load_markets()
#
# 종목 리스트에다가 USDT 종목 담기
for market in markets.keys():
    if market.endswith("/USDT"):
        jongmok.append(market)
# #
tot_df = pd.DataFrame([['timestamp', 'symbol', 'side', 'price', 'amount', 'cost']], columns=['timestamp', 'symbol', 'side', 'price', 'amount', 'cost'])
tot_df.set_index('timestamp', inplace=True)
print(tot_df)
# 거래내역 조회
for symbol in jongmok:

    d = binance.parse8601()
    fetchTrades = binance.fetch_my_trades(symbol=symbol, since=d, limit=1000, params={'order':'asc'})
    pprint.pprint(fetchTrades)

    if fetchTrades != []:
        pprint.pprint(fetchTrades)
    # if fetchTrades != []:
#         pprint.pprint(fetchTrades)
        print('Total ' + str(len(fetchTrades)) + ' rows.')

        df = pd.DataFrame(fetchTrades)
        print(df.columns)
        print(df.info())
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d')
        df = df.astype({'timestamp': 'str'})
        df['timestamp'] = df['timestamp'].str[:-4]
#
        df = df.loc[:, ['timestamp', 'symbol', 'side', 'price', 'amount', 'cost']]
        # df.set_index('timestamp', inplace=True)
        df_price = df.groupby(['timestamp', 'symbol', 'side']).mean()
        df = df.groupby(['timestamp', 'symbol', 'side']).sum()
        df['price'] = df_price['price']
        tot_df = pd.concat([tot_df, df], axis=0)
        print(tot_df)
        # print(df.info())
        print(df)

print(type(tot_df))
tot_df.to_excel("history.xlsx")
#
# #dataframe 생성
# date, symbol, side, price, amount, commission, realized = [], [], [], [], [], [], []
#
# for time in fetchTrades:
#     # print(type(time))
#     date.append(time["datetime"][:10])
#     symbol.append(time["symbol"][:-5])
#     side.append(time["side"])
#     price.append(time["price"])
#     amount.append(time["amount"])
#     commission.append(time["info"]["commission"])
#     realized.append(time["info"]["realizedPnl"])
#
# print(date)
# data = { "date": date, "symbol": symbol, "side": side, "price": price, "amount": amount, "commision": commission, "realized": realized}
# df = pd.DataFrame(data)
# df.set_index("date", inplace=True)
# print(df)
# df.to_excel("history.xlsx")



#
# df.set_index('datetime', inplace=True)
# 마켓
# markets = binance.load_markets()
# for i in markets:
#
#     print(i)
#
# symbol = 'ROSE/USDT'
# # pprint.pprint(markets['XRP/USDT'])
# # pprint.pprint(markets['TRX/USDT'])
# print(markets[symbol]['limits']['market']['min'])
#
# ## 레버리지
# # market = binance.load_markets()
#)

# symbol = "ETH/USDT"
# market = binance.market(symbol)
# # # print(market)
# # pprint.pprint(market)
# #
# # ## 레버리지
# resp = binance.fapiPrivate_post_leverage({
#     'symbol': market['id'],
#     'leverage': 1
# })
# pprint.pprint(resp)
#
# #
#
# 잔고조회
balance = binance.fetch_balance()

for bal in balance['info']:
    pprint.pprint(balance['info'])


# pprint.pprint(balance)
print(balance.keys())
print(type(balance['USDT']['free']))
print(balance['timestamp'])
print(balance['datetime'])
print(balance['free'])
print(balance['used'])
print(balance['total'])


# ## 포지션 조회
# positions = balance['info']['positions']
# # print(type(len(positions)))
# pprint.pprint(positions)
#
# for symbol in positions:
#     if symbol['symbol'] == 'FTMUSDT':
#         print(symbol['positionAmt'])
#
#
# print(float(positions[0]['positionAmt']))
# for data in positions:
# #     # print(data['symbol'])
#     if data['entryPrice'] != "0.0":
#         print(data['symbol'])
#
#     print(data.keys())


#
# for position in positions:
#     if position['symbol'] == 'BTCUSDT':
#         print(position.keys())
#         pprint.pprint(position)
#         print(position['initialMargin'],
#               position['entryPrice'],
#               position['unrealizedProfit'])

#현재가
# btc = binance.fetch_ticker("BTC/USDT")
# pprint.pprint(btc["last"])

#가격데이터
# btc_ohlcv = binance.fetch_ohlcv(symbol="BAL/USDT", timeframe='1h', since=None, limit=500)
# df = pd.DataFrame(data=btc_ohlcv, columns=["datetime", "open", "high", "low", "close", "volumns"])
# df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
# df.set_index('datetime', inplace=True)
# print(df)
#
# #이동평균
# def SMA(df, period, column):
#     return df[column].rolling(window=period).mean()
#
# print(type(SMA(df, 12, 'close')))
# # MA = SMA(df, 20, )
#
# print(SMA(df, 12, 'close'))
# print(SMA(df, 3, 'close'))

##매수호가
# orderbook = binance.fetch_order_book("BTC/USDT")
# pprint.pprint(orderbook)
# asks = orderbook['asks']
# bids = orderbook['bids']

# #진입
# binance.create_market_buy_order(symbol=symbol, amount=amount)


# pprint.pprint(fetchTrades)
# #청산
# binance.create_market_sell_order(symbol=symbol, amount=fetchTrades[1]['amount'])
# pprint(pprint(order))

# 대기주문
# open_orders = binance.fetch_acc(symbol="BTC/USDT")
# print(open_orders)

#이동평균
# df['close'].rolling(window=2).mean()

