import ccxt
import pprint
import time
import datetime
import numpy as np
import pandas as pd
import order
import telegram_bot

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


def cur_price(symbol):
    return binance.fetch_ticker(symbol)['last']

#
now = datetime.datetime.now()
# 마켓 불러오기
markets = binance.load_markets()

# 종목 리스트에다가 USDT 종목 담기
for market in markets.keys():
    if market.endswith("/USDT"):
        jongmok.append(market)

print(jongmok)

## 보유종목 및 포지션 조회
balance = binance.fetch_balance()
positions = balance['info']['positions']
for data in positions:
    if data['entryPrice'] != "0.0":
        my_jongmok.append(data['symbol'].replace("USDT", "/USDT")) ##보유한 종목을 my_jongmok에 담기

        # 현재 보유한 종목의 포지션 조회하기
        if float(data['positionAmt']) > 0:
            my_type = "long"
        elif float(data['positionAmt']) < 0:
            my_type = "short"
        else:
            my_type = "None"

        my_position.append([data['symbol'].replace("USDT", "/USDT"), my_type, abs(float(data['positionAmt'])), float(data['entryPrice']),
                            cur_price(data['symbol']), float(data['unrealizedProfit']), abs(float(data['entryPrice']) * float(data['positionAmt'])),
                            abs(1 + float(data['unrealizedProfit'])/100) * abs(float(data['entryPrice']) * float(data['positionAmt']))])

print(my_jongmok)
print(my_position)

# for i in my_jongmok:
#     my_jongmok.append(my_jongmok[i])

df_position = pd.DataFrame(my_position, columns=["종목", "포지션", "수량", "진입가격", "현재가", "손익", "진입금액", "현재추정금액"])
df_position.set_index("종목", inplace=True)

# df_position = np.around(df_position)
# df['진입가격'] = np.

print(df_position)
print(df_position['진입금액'].sum(), df_position['현재추정금액'].sum(), df_position['현재추정금액'].sum() - df_position['진입금액'].sum())
# print(df_position.loc['YFI/USDT'])
# print(df_position.at['YFI/USDT', '포지션'])

# asset_jongmok = ['BCH/USDT', 'LTC/USDT', 'ADA/USDT','QTUM/USDT', 'ATOM/USDT',
#                  'NEO/USDT', 'ETC/USDT', 'STORJ/USDT', 'BLZ/USDT', 'XEM/USDT']
trade_time = 0
telegram_bot.talk(str(now))

###symbol의 현재가 조회


# 트레이드 실시하기
while trade_time == 0:
    now = datetime.datetime.now()

    # if now.hour == 8 and 58 <= now.minute < 60 and (0 <= now.second < 60):
    for symbol in my_jongmok:
        # for symbol in positions:
        #     if symbol['symbol'] == symbol:
        #         amount = symbol['positionAmt']

        position = {
            'type': df_position.at[symbol, '포지션'],
            'amount': df_position.loc[symbol, '수량']
        }

        print(position)

        # 거래 가격
        coin = binance.fetch_ticker(symbol)
        cur_price = coin['last']               ###symbol의 현재가 조회

        units = markets[symbol]['limits']['market']['min']  ##symbol의 최소 거래 단위 조회

        # position['amount'] =
        # print(position['amount'])
        ## 주문양
        amount = order.cal_amount(100, cur_price, units)  ##usdt 가격을 symbol단위로 환산# 거래가격(usdt), 상품가격, 최소 단위

        # 이동평균 매매전략
        ## 가격데이터 불러오기
        btc_ohlcv = binance.fetch_ohlcv(symbol=symbol, timeframe='1d', since=None, limit=50)
        df = pd.DataFrame(data=btc_ohlcv, columns=["datetime", "open", "high", "low", "close", "volumns"])
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        df.set_index('datetime', inplace=True)

        ## 이동평균선 함수
        def SMA(df, period, column):
            return df[column].rolling(window=period).mean()

        short_MA = SMA(df, 3, 'close')
        long_MA = SMA(df, 12, 'close')

        i = 2
        ## 이동평균선 교차했을 경우
        if (short_MA.iloc[-i]-long_MA.iloc[-i])*(short_MA.iloc[-i-1]-long_MA.iloc[-i-1]) < 0:
            # d = binance.parse8601()
            # fetchTrades = binance.fetch_my_trades(symbol, d, 30, {'order': 'asc'}) # 최근 거래내역
            if short_MA.iloc[-i] > long_MA.iloc[-i]:
                signal.append(symbol + "매수") ##단기이평이 장기이평보다 높은 경우 signal 리스트에 표시
            elif short_MA.iloc[-i] < long_MA.iloc[-i]:
                signal.append(symbol + "매도")  ##장기이평이 장기이평보다 높은 경우 signal 리스트에 표시

            # if fetchTrades == []:
            #     last_trade = 0
            # else:
            #     last_trade = position['amount'] ##현재 symbol의 보유하고 있는 최근 보유량

            ##거래실시

            print(signal)
            # order.enter_position(symbol, amount, position, short_MA, long_MA, cur_price, binance)

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




