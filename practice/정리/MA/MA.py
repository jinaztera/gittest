import ccxt
import pprint
import time
import datetime

import pandas as pd
import math

import message


def cal_amount(usdt_balance, cur_price, units):
    amount = math.floor((usdt_balance * 1/units) / cur_price) / (1/units)
    return amount

def enter_position(symbol, amount, position, short_MA, long_MA, last_trade, cur_price, binance):  # (binance, symbol, amount, position):

    if short_MA.iloc[-1] > long_MA.iloc[-1]:
        if position['type'] == 'None':
            position['type'] = 'long'
            amount = position['amount']
            print(symbol + "매수진입, " + "매수량: " + str(amount*cur_price))
            message.talk(symbol + "매수진입, " + "매수금: " + str(amount*cur_price))

            binance.create_market_buy_order(symbol=symbol, amount=amount)
        elif position['type'] == 'short':
            position['type'] = 'long'
            amount = position['amount']
            print(symbol + "매도청산", last_trade)
            message.talk(symbol + "매도청산 " + str(last_trade))
            binance.create_market_buy_order(symbol=symbol, amount=last_trade)
            print(symbol + "매수진입, ", "매수량: " + str(amount))
            message.talk(symbol + "매수진입, " + "매수량: " + str(amount))
            binance.create_market_buy_order(symbol=symbol, amount=amount)

    elif short_MA.iloc[-1] < long_MA.iloc[-1]:
        if position['type'] == 'None':
            position['type'] = 'short'
            amount = position['amount']
            print(symbol + "매도진입", "매도량: " + str(amount*cur_price))
            message.talk(symbol + "매도진입, " + "매도금: " + str(amount*cur_price))
            binance.create_market_sell_order(symbol=symbol, amount=amount)
        elif position['type'] == 'long':
            position['type'] = 'short'
            amount = position['amount']
            print(symbol + "매수청산", last_trade)
            message.talk(symbol + "매수청산, " + str(last_trade))
            binance.create_market_sell_order(symbol=symbol, amount=last_trade)
            print(symbol + "매도진입",  "매도량: " + str(amount))
            message.talk(symbol + "매도진입, " + "매도량: " + str(amount))
            binance.create_market_sell_order(symbol=symbol, amount=amount)
