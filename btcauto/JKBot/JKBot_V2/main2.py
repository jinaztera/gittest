import ccxt
import pprint
import time
import datetime

import pandas as pd
import order
import message
import math

jongmok = []
signals = []
totalposition = []
my_jongmok = []
my_position = []
initialAMT = 100

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

markets = binance.load_markets()
# 종목 리스트에다가 USDT 종목 담기
for market in markets.keys():
    if market.endswith("/USDT"):
        jongmok.append(market)

def ohlcv(symbol):
    btc_ohlcv = binance.fetch_ohlcv(symbol=symbol, timeframe='1d', since=None, limit=50)
    df = pd.DataFrame(data=btc_ohlcv, columns=["datetime", "open", "high", "low", "close", "volumns"])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    # df.set_index('datetime', inplace=True)
    return df

def SMA(df, period, column):
    return df[column].rolling(window=period).mean()

def cal_amount(usdt_balance, cur_price, units):
    amount = math.floor((usdt_balance * 1/units) / cur_price) / (1/units)
    return amount


balance = binance.fetch_balance()
positions = balance['info']['positions']


# 전체종목 조회

# print(signals)
# for symbol in signals:
#     print(symbol[0])

history_df = pd.read_excel("trade_history.xlsx")
# position_df = pd.read_excel("trade_position.xlsx")
print(history_df)

now = datetime.datetime.now()
signals = []
print(now)
my_position = []
for data in positions:
    if data['entryPrice'] != "0.0":
        my_jongmok.append(data['symbol'].replace("USDT", "/USDT"))  ##보유한 종목을 my_jongmok에 담기

        # 현재 보유한 종목의 포지션 조회하기
        if float(data['positionAmt']) > 0:
            my_type = "long"
        elif float(data['positionAmt']) < 0:
            my_type = "short"
        else:
            my_type = "None"

        my_position.append(
            [data['symbol'][:-4], my_type, float(data['entryPrice']), float(data['unrealizedProfit']),
             float(data['positionAmt']), float(data['entryPrice']) * float(data['positionAmt']), ''])

position_df = pd.DataFrame(my_position,
                           columns=['symbol', 'side', 'endtryPrice', 'profit', 'amount', 'USDT', 'verification'])
position_df.to_excel('trade_position.xlsx', index=False)
print(my_jongmok)
print(my_position)
print(position_df)

##수익률 업데이트
for symbol in position_df['symbol']:
    coin = binance.fetch_ticker(symbol + '/USDT')
    cur_price = coin['last']
    pd.set_option('display.max_columns', None)
    pd.set_option('mode.chained_assignment', None)
    # print(position_df)

    short_MA = SMA(ohlcv(symbol + '/USDT'), 3, 'close')
    long_MA = SMA(ohlcv(symbol + '/USDT'), 12, 'close')

    a = short_MA.iloc[-1]  # 1일전 단기이동평균선
    b = long_MA.iloc[-1]  # 1일전 장기이동평균선
    c = short_MA.iloc[-2]  # 2일전 단기이동평균선
    d = long_MA.iloc[-2]  # 2일전 장기이동평균선

    ##포지션 검증
    if a > b:
        if position_df[position_df['symbol'] == symbol].iloc[0, 1] == 'long':
            position_df.loc[position_df['symbol'] == symbol, 'verification'] = "True"
        elif position_df[position_df['symbol'] == symbol].iloc[0, 1] == 'short':
            position_df.loc[position_df['symbol'] == symbol, 'verification'] = "False"

    elif a < b:
        if position_df[position_df['symbol'] == symbol].iloc[0, 1] == 'short':
            position_df.loc[position_df['symbol'] == symbol, 'verification'] = "True"
        elif position_df[position_df['symbol'] == symbol].iloc[0, 1] == 'long':
            position_df.loc[position_df['symbol'] == symbol, 'verification'] = "False"


    # position_df.loc[position_df['symbol'] == symbol, 'current_price'] = cur_price


    # ## 수익률 계산
    # if position_df[position_df['symbol'] == symbol].iloc[0, 2] == 'short':
    #     position_df.loc[position_df['symbol'] == symbol, 'profit'] = position_df[position_df['symbol'] == symbol].iloc[0, 3] / cur_price - 1
    # elif position_df[position_df['symbol'] == symbol].iloc[0, 2] == 'long':
    #     position_df.loc[position_df['symbol'] == symbol, 'profit'] = cur_price / position_df[position_df['symbol'] == symbol].iloc[0, 3] - 1

    # ##수익금 계산
    # if position_df[position_df['symbol'] == symbol].iloc[0, 2] == 'short':
    #     position_df.loc[position_df['symbol'] == symbol, 'close_amount'] = (position_df[position_df['symbol'] == symbol].iloc[0, 3] / cur_price) * 100
    # elif position_df[position_df['symbol'] == symbol].iloc[0, 2] == 'long':
    #     position_df.loc[position_df['symbol'] == symbol, 'close_amount'] = (cur_price / position_df[position_df['symbol'] == symbol].iloc[0, 3]) * 100

print(position_df)
print(position_df['profit'].mean() * 100)

# print(position_df.loc[position_df['symbol'] == 'SNX/USDT', 'amount'])

position_df.to_excel('trade_position.xlsx', index=False)

k = 0

##종목 찾기
for symbol in jongmok[:20]:
    k = k + 1
    ##symbol에 대한 가격 데이터
    ## 이동평균선 함수

    short_MA = SMA(ohlcv(symbol), 3, 'close')
    long_MA = SMA(ohlcv(symbol), 12, 'close')

    a = short_MA.iloc[-2]  # 1일전 단기이동평균선
    b = long_MA.iloc[-2]  # 1일전 장기이동평균선
    c = short_MA.iloc[-3]  # 2일전 단기이동평균선
    d = long_MA.iloc[-3]  # 2일전 장기이동평균선

    if a > b and c < d:
        signals.append([symbol, "매수", k])
    elif a < b and c > d:
        signals.append([symbol, "매도", k])

    if a > b:
        totalposition.append([symbol, "long"])
    elif a < b:
        totalposition.append([symbol, "short"])
# print(totalposition)
# print(now)
print(signals)
# telegram_bot.talk(str(now))
for signal in signals:
    coin = binance.fetch_ticker(signal[0])
    cur_price = coin['last']
    # print(signal[0], signal[1], cur_price)
    # telegram_bot.talk(signal[0] + signal[1] + str(cur_price))

# if now.hour == 18 and 0 <= now.minute < 60:
print('거래진입')


for signal in signals:
    print(signal)
    new_data = []
    df = ohlcv(signal[0])
    coin = binance.fetch_ticker(signal[0])
    cur_price = coin['last']
    # position_df.reset_index(drop=True, inplace=True)  ##인덱스 초기화

    d = binance.parse8601()
    fetchTrades = binance.fetch_my_trades(symbol=signal[0], since=d, limit=1000, params={'order': 'asc'})

    if signal[1] == "매수":

        ##엑셀 데이터 불러오기
        ## 현재 포지션 보유중 매도포지션 청산 & 매수 포지션 진입
        if len(position_df[(position_df['symbol'] == signal[0][:-5]) & (position_df['side'] == 'short')]) == 1: #position 데이터에 데이터가 있으면:
            # 매수주문 (청산)
            # print(signal[0])

            ##매도 청산(매수 주문)
            amount = float(position_df.loc[position_df['symbol'] == signal[0][:-5], 'amount'])
            binance.create_market_buy_order(symbol=signal[0], amount=abs(amount))

            usdt = float(fetchTrades[-1]['price']) * float(fetchTrades[-1]['amount'])
            new_data = [fetchTrades[-1]['datetime'][:16], signal[0][:-5], 'long', fetchTrades[-1]['price'],
                        fetchTrades[-1]['amount'], usdt]
            history_df.loc[len(history_df)] = new_data
            history_df.to_excel('trade_history.xlsx', index=False)

            telegram_bot.talk(str(now) + signal[0] + str(amount) + " " + str(cur_price) + "매도청산")
            history_df


            # history_df.to_excel('trade_history.xlsx', index=False)
            # ## 매도포지션 삭제

            if balance['USDT']['free'] < initialAMT:
                print(signal[0] + "잔고가 부족합니다.")
                telegram_bot.talk("거래잔고가 부족합니다")
            else:
                ## 매수진입
                units = markets[signal[0]]['limits']['market']['min']  ##symbol의 최소 거래 단위 조회
                amount = cal_amount(initialAMT, cur_price, units)  ##usdt 가격을 symbol단위로 환산# 거래가격(usdt), 상품가격, 최소 단위
                binance.create_market_buy_order(symbol=signal[0], amount=amount)
                usdt = float(fetchTrades[-1]['price']) * float(fetchTrades[-1]['amount'])
                new_data = [fetchTrades[-1]['datetime'][:16], signal[0][:-5], 'long', fetchTrades[-1]['price'],
                            fetchTrades[-1]['amount'], usdt]
                history_df.loc[len(history_df)] = new_data
                history_df.to_excel('trade_history.xlsx', index=False)

            #position_df.to_excel('trade_position.xlsx', index=False)

                print(now, signal[0], "매도청산 후 매수진입")
                telegram_bot.talk(str(now) + signal[0] + str(amount) + " " + str(cur_price) + "매수진입")

            # 매수주문
        ## 포지션 없음 -> 매도 포지션 진입
        elif len(position_df[position_df['symbol'] == signal[0][:-5]]) == 0:
            if balance['USDT']['free'] < initialAMT:
                print(signal[0] + "잔고가 부족합니다.")
                telegram_bot.talk("거래잔고가 부족합니다")
            else:
                units = markets[signal[0]]['limits']['market']['min']  ##symbol의 최소 거래 단위 조회
                amount = cal_amount(initialAMT, cur_price, units)  ##usdt 가격을 symbol단위로 환산# 거래가격(usdt), 상품가격, 최소 단위
                binance.create_market_buy_order(symbol=signal[0], amount=amount)

                usdt = float(fetchTrades[-1]['price']) * float(fetchTrades[-1]['amount'])
                new_data = [fetchTrades[-1]['datetime'][:16], signal[0][:-5], 'long', fetchTrades[-1]['price'], fetchTrades[-1]['amount'], usdt]
                history_df.loc[len(history_df)] = new_data
                history_df.to_excel('trade_history.xlsx', index=False)

                #position_df.to_excel('trade_position.xlsx', index=False) ##포지션 엑셀 파일 생성
                #매도주문

                print(now, signal[0], "매수진입")
                telegram_bot.talk(str(now) + signal[0] + str(amount) + " " + str(cur_price) + "매수진입")

    elif signal[1] == '매도':
        ## 매수 포지션 보유중이었다면,
        if len(position_df[(position_df['symbol'] == signal[0][:-5]) & (position_df['side'] == 'long')]) == 1:  # position 데이터에 데이터가 있으면:
            # 매수주문 (청산)
            amount = float(position_df.loc[position_df['symbol'] == signal[0][:-5], 'amount'])
            binance.create_market_sell_order(symbol=signal[0], amount=abs(amount))

            usdt = float(fetchTrades[-1]['price']) * float(fetchTrades[-1]['amount'])
            new_data = [fetchTrades[-1]['datetime'][:16], signal[0][:-5], 'short', fetchTrades[-1]['price'],
                        fetchTrades[-1]['amount'], usdt]
            history_df.loc[len(history_df)] = new_data
            history_df.to_excel('trade_history.xlsx', index=False)

            telegram_bot.talk(str(now) + signal[0] + amount + " " + cur_price + "매수청산")


            # #position_df.to_excel('trade_position.xlsx', index=False)
            if balance['USDT']['free'] < initialAMT:
                print(signal[0] + "잔고가 부족합니다.")
                telegram_bot.talk("거래잔고가 부족합니다")
            else:
                units = markets[signal[0]]['limits']['market']['min']  ##symbol의 최소 거래 단위 조회
                amount = cal_amount(initialAMT, cur_price, units)  ##usdt 가격을 symbol단위로 환산# 거래가격(usdt), 상품가격, 최소 단위
                binance.create_market_sell_order(symbol=signal[0], amount=amount)

                usdt = float(fetchTrades[-1]['price']) * float(fetchTrades[-1]['amount'])
                new_data = [fetchTrades[-1]['datetime'][:16], signal[0][:-5], 'short', fetchTrades[-1]['price'],
                            fetchTrades[-1]['amount'], usdt]
                history_df.loc[len(history_df)] = new_data
                history_df.to_excel('trade_history.xlsx', index=False)

                print(now, signal[0], "매수청산 후 매도진입")
                telegram_bot.talk(str(now) + signal[0] + str(amount) + " " + str(cur_price) + "매도진입")

            # 매수주문
        ## 포지션이 없었다면
        elif len(position_df[position_df['symbol'] == signal[0][:-5]]) == 0:
            if balance['USDT']['free'] < initialAMT:
                print(signal[0] + "잔고가 부족합니다.")
                telegram_bot.talk("거래잔고가 부족합니다")
            else:
                units = markets[signal[0]]['limits']['market']['min']  ##symbol의 최소 거래 단위 조회
                amount = cal_amount(initialAMT, cur_price, units)  ##usdt 가격을 symbol단위로 환산# 거래가격(usdt), 상품가격, 최소 단위
                binance.create_market_sell_order(symbol=signal[0], amount=amount)

                usdt = float(fetchTrades[-1]['price']) * float(fetchTrades[-1]['amount'])
                new_data = [fetchTrades[-1]['datetime'][:16], signal[0][:-5], 'short', fetchTrades[-1]['price'],
                            fetchTrades[-1]['amount'], usdt]
                history_df.loc[len(history_df)] = new_data
                history_df.to_excel('trade_history.xlsx', index=False)

                #position_df.to_excel('trade_position.xlsx', index=False)  ##포지션 엑셀 파일 생성
                # 매도주문

                print(now, signal[0], "매도진입")
                telegram_bot.talk(str(now) + signal[0] + str(amount) + " " + str(cur_price) + "매도진입")

time.sleep(10)

my_position = []
for data in positions:
    if data['entryPrice'] != "0.0":
        my_jongmok.append(data['symbol'].replace("USDT", "/USDT"))  ##보유한 종목을 my_jongmok에 담기

        # 현재 보유한 종목의 포지션 조회하기
        if float(data['positionAmt']) > 0:
            my_type = "long"
        elif float(data['positionAmt']) < 0:
            my_type = "short"
        else:
            my_type = "None"

        my_position.append(
            [data['symbol'][:-4], my_type, float(data['entryPrice']), float(data['unrealizedProfit']),
             float(data['positionAmt']), float(data['entryPrice']) * float(data['positionAmt']), ''])

position_df = pd.DataFrame(my_position,
                           columns=['symbol', 'side', 'endtryPrice', 'profit', 'amount', 'USDT', 'verification'])
position_df.to_excel('trade_position.xlsx', index=False)

print(my_position)
print(position_df)

position_df.to_excel('trade_position.xlsx', index=False)
history_df.to_excel('trade_history.xlsx', index=False)

print(signals)



