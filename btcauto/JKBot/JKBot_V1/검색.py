import ccxt
import pprint
import time
import datetime

import pandas as pd
import order
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

#
now = datetime.datetime.now()
# 마켓 불러오기
markets = binance.load_markets()

print(markets.keys())

# 종목 리스트에다가 USDT 종목 담기
for market in markets.keys():
    if market.endswith("/USDT"):
        jongmok.append(market)

print(jongmok)

## 보유종목 및 포지션 조회
balance = binance.fetch_balance()

# asset_jongmok = ['BCH/USDT', 'LTC/USDT', 'ADA/USDT','QTUM/USDT', 'ATOM/USDT',
#                  'NEO/USDT', 'ETC/USDT', 'STORJ/USDT', 'BLZ/USDT', 'XEM/USDT']
trade_time = 0
message.talk(str(now))

# 트레이드 실시하기
while trade_time == 0:
    now = datetime.datetime.now()

    # if now.hour == 8 and 58 <= now.minute < 60 and (0 <= now.second < 60):
    for symbol in jongmok:

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

        i = 1
        ## 이동평균선 교차했을 경우
        if (short_MA.iloc[-i]-long_MA.iloc[-i])*(short_MA.iloc[-i-1]-long_MA.iloc[-i-1]) < 0:
            # d = binance.parse8601()
            print(symbol)
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
        # resp = binance.fapiPrivate_post_leverage({
        #     'symbol': market['id'],
        #     'leverage': 1
        # })

    trade_time = 1
    print(trade_time, "hello")
    time.sleep(2)




