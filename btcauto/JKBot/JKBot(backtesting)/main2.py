import ccxt
import pprint
import time
import datetime

import pandas as pd
import order
import telegram_bot

jongmok = []
signals = []



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

# 전체종목 조회

# print(signals)
# for symbol in signals:
#     print(symbol[0])

history_df = pd.read_excel("trade_history.xlsx")
position_df = pd.read_excel("trade_position.xlsx")


while True:
    now = datetime.datetime.now()
    signals = []

    for symbol in position_df['symbol']:
        coin = binance.fetch_ticker(symbol+"/USDT")
        cur_price = coin['last']
        pd.set_option('display.max_columns', None)
        pd.set_option('mode.chained_assignment', None)
        # print(position_df)

        position_df.loc[position_df['symbol'] == symbol, 'current_price'] = cur_price

        if position_df[position_df['symbol'] == symbol].iloc[0, 2] == 'short':
            position_df.loc[position_df['symbol'] == symbol, 'profit'] = position_df[position_df['symbol'] == symbol].iloc[0, 3] / cur_price - 1
        elif position_df[position_df['symbol'] == symbol].iloc[0, 2] == 'long':
            position_df.loc[position_df['symbol'] == symbol, 'profit'] = cur_price / position_df[position_df['symbol'] == symbol].iloc[0, 3] - 1

        if position_df[position_df['symbol'] == symbol].iloc[0, 2] == 'short':
            position_df.loc[position_df['symbol'] == symbol, 'close_amount'] = (position_df[position_df['symbol'] == symbol].iloc[0, 3] / cur_price) * 100
        elif position_df[position_df['symbol'] == symbol].iloc[0, 2] == 'long':
            position_df.loc[position_df['symbol'] == symbol, 'close_amount'] = (cur_price / position_df[position_df['symbol'] == symbol].iloc[0, 3]) * 100

    print(position_df)
    print(position_df['profit'].mean() * 100)

    position_df.to_excel('trade_position.xlsx', index=False)

    for symbol in jongmok[:50]:
        ##symbol에 대한 가격 데이터
        ## 이동평균선 함수
        def SMA(df, period, column):
            return df[column].rolling(window=period).mean()

        short_MA = SMA(ohlcv(symbol), 3, 'close')
        long_MA = SMA(ohlcv(symbol), 12, 'close')

        a = short_MA.iloc[-2]  # 1일전 단기이동평균선
        b = long_MA.iloc[-2]  # 1일전 장기이동평균선
        c = short_MA.iloc[-3]  # 2일전 단기이동평균선
        d = long_MA.iloc[-3]  # 2일전 장기이동평균선

        if a > b and c < d:
            signals.append([symbol, "매수"])
        elif a < b and c > d:
            signals.append([symbol, "매도"])

    # print(now)
    print(signals)
    # telegram_bot.talk(str(now))
    for signal in signals:
        coin = binance.fetch_ticker(signal[0])
        cur_price = coin['last']
        # print(signal[0], signal[1], cur_price)
        # telegram_bot.talk(signal[0] + signal[1] + str(cur_price))

    if now.hour == 2 and 0 <= now.minute < 60 :
        for signal in signals:
            print(signal)
            new_data = []
            df = ohlcv(signal[0])
            coin = binance.fetch_ticker(signal[0])
            cur_price = coin['last']
            position_df.reset_index(drop=True, inplace=True)  ##인덱스 초기화

            if signal[1] == "매수":

                ##엑셀 데이터 불러오기
                ## 현재 포지션 보유중 매도포지션 청산 & 매수 포지션 진입
                if len(position_df[(position_df['symbol'] == signal[0][:-5]) & (position_df['side'] == 'short')]) == 1: #position 데이터에 데이터가 있으면:
                    # 매수주문 (청산)

                    ##매도 청산(매수 주문)
                    temp_df = position_df.loc[position_df['symbol'] == signal[0][:-5]]
                    new_data = [temp_df.iloc[0, 0], now, signal[0][:-5], 'short',
                                temp_df.iloc[0, 3], cur_price,
                                temp_df.iloc[0, 3] / cur_price - 1, temp_df.iloc[0, 6],
                                temp_df.iloc[0, 6] * temp_df.iloc[0, 3] / df['close'][len(df) - 1]]
                    history_df.loc[len(history_df)] = new_data
                    #history_df.to_excel('trade_history.xlsx', index=False)

                    ## 매도포지션 삭제
                    position_df = position_df[position_df['symbol'] != signal[0][:-5]]
                    position_df.reset_index(drop=True, inplace=True) ##인덱스 초기화

                    ## 매수진입
                    new_data = [now, signal[0][:-5], 'long', cur_price, "", "", 100, ""]
                    position_df.loc[len(position_df)+1] = new_data
                    #position_df.to_excel('trade_position.xlsx', index=False)

                    print(now, signal[0], "매도청산 후 매수진입")
                    telegram_bot.talk(str(now) + signal[0] + "매도청산 후 매수진입")

                    # 매수주문
                ## 포지션 없음 -> 매도 포지션 진입
                elif len(position_df[position_df['symbol'] == signal[0][:-5]]) == 0:
                    new_data = [now, signal[0][:-5], 'long', cur_price, "", "", 100, ""]
                    position_df.loc[len(position_df)] = new_data ## 정보입력
                    #position_df.to_excel('trade_position.xlsx', index=False) ##포지션 엑셀 파일 생성
                    #매도주문

                    print(now, signal[0], "매수진입")
                    telegram_bot.talk(str(now) + signal[0] + "매수진입")

            elif signal[1] == '매도':
                ## 매수 포지션 보유중이었다면,
                if len(position_df[(position_df['symbol'] == signal[0][:-5]) & (position_df['side'] == 'long')]) == 1:  # position 데이터에 데이터가 있으면:
                    # 매수주문 (청산)
                    temp_df = position_df.loc[position_df['symbol'] == signal[0][:-5]]

                    ##매수 청산 (매도주문)
                    new_data = [temp_df.iloc[0, 0], now, signal[0][:-5], 'long',
                                temp_df.iloc[0, 3], cur_price,
                                cur_price / temp_df.iloc[0, 3] - 1, temp_df.iloc[0, 6],
                                temp_df.iloc[0, 6] * df['close'][len(df) - 1] / temp_df.iloc[0, 3]]
                    history_df.loc[len(history_df)] = new_data
                    #history_df.to_excel('trade_history.xlsx', index=False)

                    ## 매수포지션 삭제
                    position_df = position_df[position_df['symbol'] != signal[0][:-5]]
                    ## 매도진입
                    new_data = [now, signal[0][:-5], 'short', cur_price, "", "", 100, ""]
                    position_df.loc[len(position_df)+1] = new_data
                    position_df.reset_index(drop=True, inplace=True) ##인덱스 초기화
                    #position_df.to_excel('trade_position.xlsx', index=False)

                    print(now, signal[0], "매수청산 후 매도진입")
                    telegram_bot.talk(str(now) + signal[0] + "매수청산 후 매도진입")

                    # 매수주문
                ## 포지션이 없었다면
                elif len(position_df[position_df['symbol'] == signal[0][:-5]]) == 0:
                    new_data = [now, signal[0][:-5], 'short', cur_price, "", "", 100, ""]
                    position_df.loc[len(position_df)+1] = new_data  ## 정보입력
                    #position_df.to_excel('trade_position.xlsx', index=False)  ##포지션 엑셀 파일 생성
                    # 매도주문

                    print(now, signal[0], "매도진입")
                    telegram_bot.talk(str(now) + signal[0] + "매도진입")

        position_df.to_excel('trade_position.xlsx', index=False)
        history_df.to_excel('trade_history.xlsx', index=False)

        print(signals)
        time.sleep(140)

    time.sleep(10)


