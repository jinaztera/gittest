import ccxt
import pprint
import time
import datetime

import pandas as pd
import math

def car_target(exchange, symbol):
    # 거래소에서 symbol에 대한 ohlcv 일봉을 얻기
    data_ohlcv = exchange.fetch_ohlcv(
        symbol=symbol,
        timeframe='1d',
        since=None,
        limit=10
    )

    # 일봉 데이터를 데이터프레임 객체로 변환
    df = pd.DataFrame(data=data_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volumns'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)



    # 전일 데이터와 금일 데이터로 목표가 계산
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    long_target = today['open'] + (yesterday['high'] - yesterday['low']) * 0.3 #(당일시가+(전일고가-전일전가)*0.5
    short_target = today['open'] - (yesterday['high'] - yesterday['low']) * 0.3  # (당일시가+(전일고가-전일전가)*0.5
    return long_target, short_target

def cal_amount(usdt_balance, cur_price):
    portion = 0.1
    usdt_trade = usdt_balance * portion
    amount = math.floor((usdt_trade * 1000000) / cur_price) / 1000000
    return amount

def enter_position(binance, symbol, cur_price, long_target, short_target, amount, position):
    if cur_price > long_target:
        position['type'] = 'long'
        position['amount'] = amount
        binance.create_market_buy_order(symbol=symbol, amount=amount)

    elif cur_price < short_target:
        position['type'] = 'short'
        position['amount'] = amount
        binance.create_market_sell_order(symbol=symbol, amount=amount)

def exit_position(binance, symbol, position):
    if position['type'] == 'long':
        binance.create_market_sell_order(symbol=symbol, amount=amount)
        position['type'] = None
    elif position['type'] == 'short':
        binance.create_market_buy_order(symbol=symbol, amount=amount)
        position['type'] = None