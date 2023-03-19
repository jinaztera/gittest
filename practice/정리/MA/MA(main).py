import ccxt
import pprint
import time
import datetime

import pandas as pd
import MA
import message

import math

jongmok = []
signal = []
my_jongmok = []
my_position = []



#API 키 읽기
with open("../api(JKBOT).txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

#바이낸스 불러오기
binance = ccxt.binance(config={
    'apiKey': api_key, #"XTpKrQGSk3GhXzqiEV4OfwGJzmTVcLh8dKGwHo4aQBH4p0mOqPDpIsxdh95tjGVf",
    'secret': secret, #"A0eqZGEWHsyL3NMM6WuDrucIanr7A2YZAnrwXVPhXpf2WGauIANwa5zsoNeNt0hs",
    'enableRateLimit' : True,
    'options': {
        'defaultType': 'future'
    }
})

now = datetime.datetime.now()
markets = binance.load_markets()
for market in markets.keys():
    if market.endswith("/USDT"):
        jongmok.append(market)

print(jongmok)

## 보유종목 조회
balance = binance.fetch_balance()
positions = balance['info']['positions']
for data in positions:
    if data['entryPrice'] != "0.0":
        my_jongmok.append(data['symbol'].replace("USDT", "/USDT"))

        if float(data['positionAmt']) > 0:
            my_type = "long"
        elif float(data['positionAmt']) < 0:
            my_type = "short"
        else:
            my_type = "None"


        my_position.append([data['symbol'].replace("USDT", "/USDT"), my_type, float(data['entryPrice']), float(data['unrealizedProfit']), float(data['positionAmt'])])

print(my_jongmok)
print(my_position)

# for i in my_jongmok:
#     my_jongmok.append(my_jongmok[i])

df_position = pd.DataFrame(my_position, columns=["종목", "포지션", "진입가격", "손익", "수량"])
df_position.set_index("종목", inplace=True)
# print(df_position.loc['YFI/USDT'])
# print(df_position.at['YFI/USDT', '포지션'])

asset_jongmok = ['BCH/USDT', 'LTC/USDT', 'ADA/USDT','QTUM/USDT', 'ATOM/USDT',
                 'NEO/USDT', 'ETC/USDT', 'STORJ/USDT', 'BLZ/USDT', 'XEM/USDT']
trade_time = 0
message.talk(str(now))
while trade_time == 0:
    now = datetime.datetime.now()

    # if now.hour == 8 and 58 <= now.minute < 60 and (0 <= now.second < 60):

    for symbol in my_jongmok:

        for symbol in positions:
            if symbol['symbol'] == symbol:
                amount = symbol['positionAmt']


        position = {
            'type': df_position.at[symbol, '포지션'],
            'amount': amount
        }
        # 매수 가격
        coin = binance.fetch_ticker(symbol)
        cur_price = coin['last']
        balance = binance.fetch_balance()
        units = markets[symbol]['limits']['market']['min']
        amount = MA.cal_amount(100, cur_price, units)  # 거래가격(usdt), 상품가격, 최소 단위

        # 이동평균 매매전략
        btc_ohlcv = binance.fetch_ohlcv(symbol=symbol, timeframe='1d', since=None, limit=50)
        df = pd.DataFrame(data=btc_ohlcv, columns=["datetime", "open", "high", "low", "close", "volumns"])
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        df.set_index('datetime', inplace=True)

        def SMA(df, period, column):
            return df[column].rolling(window=period).mean()

        short_MA = SMA(df, 3, 'close')
        long_MA = SMA(df, 12, 'close')

        # print(short_MA)
        # print(long_MA)

        if (short_MA.iloc[-1]-long_MA.iloc[-1])*(short_MA.iloc[-2]-long_MA.iloc[-2]) < 0:
            trade_time = 1
            d = binance.parse8601()
            fetchTrades = binance.fetch_my_trades(symbol, d, 30, {'order': 'asc'}) # '''거래내역
            if short_MA.iloc[-1] > long_MA.iloc[-1]:
                signal.append(symbol + "매수")
            elif short_MA.iloc[-1] < long_MA.iloc[-1]:
                signal.append(symbol + "매도")

            if fetchTrades == []:
                last_trade = 0

            else:
                last_trade = position['amount']

            MA.enter_position(symbol, amount, position, short_MA, long_MA, last_trade, cur_price, binance)

        # else:
            # print(symbol + " 매매종료")
            # kakao_talk = symbol + " 매매종료"
            # message.talk(kakao_talk)

        market = binance.market(symbol)
        # # print(market)

        ## 레버리지
        resp = binance.fapiPrivate_post_leverage({
            'symbol': market['id'],
            'leverage': 1
        })





    trade_time = 1
    print(trade_time, "hello")
    time.sleep(2)




