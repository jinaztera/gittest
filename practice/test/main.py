import ccxt
import pprint
import time
import datetime

import pandas as pd
import larry

import math

#API 키 읽기
with open("../api.txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

print(api_key)
print(secret)

#바이낸스 불러오기
binance = ccxt.binance(config={
    'apiKey': api_key, #"XTpKrQGSk3GhXzqiEV4OfwGJzmTVcLh8dKGwHo4aQBH4p0mOqPDpIsxdh95tjGVf",
    'secret': secret, #"A0eqZGEWHsyL3NMM6WuDrucIanr7A2YZAnrwXVPhXpf2WGauIANwa5zsoNeNt0hs",
    'enableRateLimit' : True,
    'options': {
        'defaultType': 'future'
    }
})

symbol = "BTC/USDT"
long_target, short_target = larry.car_target(binance, symbol)

# 잔고조회
balance = binance.fetch_ticker(symbol=symbol)
# usdt = balance['total']['USDT']
# amount = larry.cal_amount(usdt, cur_price)

position = {
    "type": None,
    "amount": 0
}

op_mode = True

while True:
    now = datetime.datetime.now()

    # 포지션 종료
    if now.hour == 8 and now.minute == 50 and ( 0 <= now.second < 10):
        if op_mode and position['type'] is not None:
            larry.exit_position(binance, symbol, position)
            op_mode = False

        # and position['type'] is None:
        # larry.enter_position(b inance, symbol, cur_price, long_target, short_target, amount, position):

    # 목표가 갱신
    # 09:00:20 ~ 09:00:30
    if now.hour == 9 and now.minute == 0 and (20 <= now.second < 30):
        long_target, short_target = larry.car_target(binance, symbol)
        balance = binance.fetch_balance()  #잔고조회
        op_mode = True
        time.sleep(10)



    # 현재가, 구매 가능 수량량
    btc = binance.fetch_ticker(symbol=symbol)

    cur_price = btc['last']
    balance = binance.fetch_balance()
    usdt = balance['total']['USDT']
    amount = larry.cal_amount(usdt, cur_price)


    if op_mode and position['type'] is None:
         larry.enter_position(binance, symbol, cur_price, long_target, short_target, amount, position)


    # time
    now = datetime.datetime.now()


    print(now, long_target, short_target, cur_price, op_mode, position['type'])

    time.sleep(1)

#실시간 조회





##현재시간 조회
# def car_target(symbol):
#     btc_ohlcv = binance.fetch_ohlcv(
#         symbol=symbol,
#         timeframe='1d',
#         since=None,
#         limit=10
#     )
#
#     df = pd.DataFrame(data=btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volumns'])
#     df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
#     df.set_index('datetime', inplace=True)
#
#     yesterday = df.iloc[-2]
#     today = df.iloc[-1]
#     target = today['open']+(yesterday['high']-yesterday['low'])*0.5 #(당일시가+(전일고가-전일전가)*0.5
#     return target




