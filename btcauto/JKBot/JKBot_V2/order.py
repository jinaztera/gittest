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

    # (symbol : 종목, amount : 매수량, position : 'long' or 'short' or 'None, cur_price :현재가, binance : 클래스):
def enter_position(symbol, amount, position, short_MA, long_MA, cur_price, binance):
    ##단기이평이 장기이평보다 높은 경우
    if short_MA.iloc[-1] > long_MA.iloc[-1]:

        if position['type'] == 'None':
            position['type'] = 'long' ##포지션이 없는 경우 포지션을 롱으로 진입
            # amount = position['amount']
            binance.create_market_buy_order(symbol=symbol, amount=position['amount']) ## symbol을 amount 만큼 주문
            print(symbol + "매수진입, " + "매수량: " + str(amount*cur_price)) ##
            telegram_bot.talk(symbol + "매수진입, " + "매수금: " + str(amount*cur_price))


        elif position['type'] == 'short':
            position['type'] = 'long' ##포지션이 숏인 경우 숏을 청산하고 롱으로 진입
            # amount = position['amount'] ##현재 보유하고 있는 보지션의 수량

            ## 숏 청산
            binance.create_market_buy_order(symbol=symbol, amount=position['amount'])
            print(symbol + "매도청산", position['amount'])
            telegram_bot.talk(symbol + "매도청산 " + str(position['amount']))

            ## 롱 진입
            binance.create_market_buy_order(symbol=symbol, amount=amount)
            print(symbol + "매수진입, ", "매수량: " + str(amount))
            telegram_bot.talk(symbol + "매수진입, " + "매수량: " + str(amount))


    ## 단기이평이 장기이평보다 낮은 경우
    elif short_MA.iloc[-1] < long_MA.iloc[-1]:
        if position['type'] == 'None':
            position['type'] = 'short' ## 포지션이 없는 경우 숏으로 반환
            # amount = position['amount'] ##

            ## 매도진입
            binance.create_market_sell_order(symbol=symbol, amount=amount)
            print(symbol + "매도진입", "매도량: " + str(amount * cur_price))
            telegram_bot.talk(symbol + "매도진입, " + "매도금: " + str(amount * cur_price))

        elif position['type'] == 'long':
            position['type'] = 'short' ## 포지션이 롱인 경우 청산하고 롱으로 반환

            ## 현재 매수 포지션 정리
            binance.create_market_sell_order(symbol=symbol, amount=position['amount'])
            print(symbol + "매수청산", amount)
            telegram_bot.talk(symbol + "매수청산, " + str(position['amount']))

            ## 매도 진입
            binance.create_market_sell_order(symbol=symbol, amount=amount)
            print(symbol + "매도진입",  "매도량: " + str(amount))
            telegram_bot.talk(symbol + "매도진입, " + "매도량: " + str(amount))

