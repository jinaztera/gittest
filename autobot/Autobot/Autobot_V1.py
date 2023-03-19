import ccxt
import pandas as pd
import math
from datetime import datetime, timedelta
import time

#API 키 읽기
with open("../api(JKBOT).txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

binance = ccxt.binance(config={
    'apiKey': api_key, #"XTpKrQGSk3GhXzqiEV4OfwGJzmTVcLh8dKGwHo4aQBH4p0mOqPDpIsxdh95tjGVf",
    'secret': secret, #"A0eqZGEWHsyL3NMM6WuDrucIanr7A2YZAnrwXVPhXpf2WGauIANwa5zsoNeNt0hs",
    'enableRateLimit' : True,
    'options': {
        'defaultType': 'future'
    }
})

today_date = ""

def ohlcv(symbol, limit=2000):
    btc_ohlcv = binance.fetch_ohlcv(symbol=symbol, timeframe='1d', since=None, limit=limit)
    df = pd.DataFrame(data=btc_ohlcv, columns=["datetime", "open", "high", "low", "close", "volumns"])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')


    return df
# def cal_amount(usdt_balance, cur_price, units):
#     amount = math.floor((usdt_balance * 1/units) / cur_price) / (1/units)
#     return amount
jongmok = []
markets = binance.load_markets() #마켈로드
balance = binance.fetch_balance() #계좌로드

# 선물종목 담아오기
# for market in markets.keys():
#     if market.endswith(":USDT"):
#         jongmok.append(market)

jongmok = ['BTC', 'ETH', 'STX', 'OP', 'XEM', 'MATIC', 'DYDX', 'SOL', 'APT', 'XRP', 'FIL', 'LDO', 'BNB', 'DOGE', 'AGIX', 'LTC', 'NEO', 'FTM', 'BNX', 'LINK', 'ANKR', 'CFX', 'ADA', 'GTC', 'GMT', 'FET', 'AVAX', 'ETC', '1000SHIB', 'DOT', 'GALA', 'SAND', 'STG', 'SSV', 'GRT', 'CRV', 'NEAR', 'EOS', 'YFI', 'APE', 'SNX', 'ACH', 'KLAY', 'MAGIC', 'MANA', 'AXS', 'BCH', 'MASK', 'FXS', 'OCEAN', 'HOOK', 'RNDR', 'ATOM', 'OMG', 'HIGH', 'AUDIO', 'DASH', 'AR', 'LINA', 'MKR', 'SUSHI', 'LIT', 'INJ', 'DUSK', 'TRX', 'BLZ', 'VET', 'KNC', 'REN', 'CHZ', 'IMX', 'THETA', 'AAVE', 'UNI', 'HBAR', 'ICP', 'WAVES', 'MINA', 'KAVA', 'ROSE', 'ZEC', 'ENS', 'QTUM', 'XTZ', 'COCOS', '1000LUNC', 'FLOW', 'ENJ', 'RLC', 'XLM', 'LRC', 'CELO', 'JASMY', 'IOTA', 'EGLD', 'UNFI', 'ONT', '1INCH', 'RUNE', 'ZIL', 'WOO', 'XMR', 'BEL', 'ALPHA', 'ICX', 'BAT', 'BAKE', 'ALGO', 'API3', 'C98', 'SXP', 'TRB', 'RSR', 'ONE', 'PEOPLE', 'COMP', 'PHB', 'STMX', 'SKL', 'LUNA2', 'KSM', 'STORJ', 'GAL', 'BAND', 'ALICE', 'ZRX', 'QNT', 'IOST', 'ZEN', 'CELR', 'MTL', 'REEF', 'COTI', 'ATA', 'HOT', 'FLM', 'DENT', 'IOTX', 'SFP', 'ASTR', 'RVN', 'CVX', 'ANT', 'TOMO', 'OGN', 'BAL', 'GMX', 'LPT', 'NKN', 'T', 'HNT', 'DAR', 'CTSI', 'DGB', 'CTK', 'ARPA', '1000XEC', 'SPELL', 'BTCDOM', 'FOOTBALL', 'DEFI', 'BLUEBIRD']


# 거래 최소단위

min_units = {}
for sym in jongmok:
    min_units[sym] = markets[sym+'/USDT']['limits']['market']['min']

#보유종목 조회
def account():
    global account_df
    print("계좌를 조회합니다.")
    balance = binance.fetch_balance()
    positions = balance['info']['positions'] # 포지션 조회
    df = pd.DataFrame(positions, columns = list(positions[0].keys()))
    account_df = df[df['initialMargin'] != "0"]
    position_tot = (pd.to_numeric(account_df['entryPrice']) * abs(pd.to_numeric(account_df['positionAmt']))).sum()
    cur_tot = pd.to_numeric(account_df['initialMargin']).sum()
    # unrealizedProfit = pd.to_numeric(account_df['unrealizedProfit']).sum()
    unrealizedProfit = balance['info']['assets'][6]['unrealizedProfit']
    marginBalance = balance['info']['assets'][6]['marginBalance'].split('.')[0].strip()
    print("보유금액: " +str(marginBalance) + " USDT", "매수금액: " + str(int(cur_tot)) + " USDT", "  미실현손익: " + str(int(round(float(unrealizedProfit)))) +" USDT")
    return account_df

# 현재가 조회
def cur_price(symbol):
    cur_price = binance.fetch_ticker(symbol+'/USDT')['last']
    # print(symbol +"의 현재가는 " + str(cur_price) + "입니다.")
    return cur_price
# 주문
def order(symbol, usdt, side):

    print(symbol + "을 " + str(usdt) + "USD "+ side +"합니다.")
    amount = math.floor((usdt/cur_price(symbol))/min_units[symbol])*min_units[symbol]
    # binance.create_market_order(symbol=symbol+'/USDT', amount=amount, side=side)

# 청산
# 청산
def close_order(symbol):
    print(symbol +"을 모두 청산합니다.")
    balance = binance.fetch_balance()
    positions = balance['info']['positions'] # 포지션 조회
    df = pd.DataFrame(positions, columns = list(positions[0].keys()))
    amount = float(df.loc[df.loc[:, 'symbol'] == symbol.replace("/USDT", "USDT")]['positionAmt'].iloc[0])
    if amount > 0:
        side = 'SELL'
    elif amount <0:
        side = 'BUY'
    binance.create_market_order(symbol=symbol+'/USDT', amount=abs(amount), side=side)

#거래내역 조회
def history():
    history= []
    print("거래내역을 조회합니다.")
    for sym in jongmok:
        d = binance.parse8601()
        fetchTrades = binance.fetch_my_trades(symbol=sym+'/USDT', since=d, limit=4000, params={'order': 'asc'})
        if len(fetchTrades) != 0:
            for k in range(len(fetchTrades)):
                fetchTrades[k]['fee'] = fetchTrades[k]['fee']['cost']
                fetchTrades[k]['realizedPnl'] = fetchTrades[k]['info']['realizedPnl']
                del fetchTrades[k]['info']
                del fetchTrades[k]['fees']
                history.append(fetchTrades[k])

    col = list(history[0].keys())
    col.append('realizedPnl')
    df = pd.DataFrame(history, columns=list(history[0].keys()))
    df['symbol'] = df['symbol'].str.slice(stop=-5)
    df['datetime'] = df['datetime'].str.slice(stop=-5)
    history_df = df.sort_values('datetime', ascending=True)
    history_df['realizedPnl'] = pd.to_numeric(history_df['realizedPnl'])
    history_df = history_df[['datetime', 'order', 'symbol', 'side', 'price', 'amount', 'cost', 'fee', 'realizedPnl']].reset_index(drop=True)
    history_df = history_df.groupby('order', as_index=False).agg({
        'datetime' : 'first',
        'order' : 'first',
        'symbol' : 'first',
        'side' : 'first',
        'price' : 'mean',
        'amount' : 'sum',
        'cost' : 'sum',
        'fee' : 'sum',
        'realizedPnl' : 'sum'
    })
    history_df = history_df.sort_values('datetime', ascending=True).reset_index(drop=True)
    print("조회하였습니다.")
    return history_df

#스캔
def end_order(symbol, amount, side):
    print(symbol + "을 " + str(amount) + " "+ side +"합니다.")
    # binance.create_market_order(symbol=symbol+'/USDT', amount=amount, side=side)

def scan():
    window = 28
    away = 7
    print("지표를 생성중입니다.")
    from tensorflow import keras
    import numpy as np
    model = keras.Sequential()
    model.add(keras.layers.LSTM(30, activation='relu', input_shape=(window, 4), dropout=0.3))
    model.add(keras.layers.Dense(1, activation='sigmoid'))
    model.load_weights('1d_28_7_(30).h5')
    global signal, ind_dict, ind_df
    x_data = {}
    ind_dict = {}
    ind = []
    ticker = []
    global today_date
    for symbol in jongmok:

        btc_ohlcv = binance.fetch_ohlcv(symbol=symbol+'/USDT', timeframe='1d', since=None, limit=window+1)
        df = pd.DataFrame(data=btc_ohlcv, columns=["datetime", "open", "high", "low", "close", "volumns"])
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')

        df.set_index('datetime', inplace=True)
        x_data[symbol] = df[['open', 'high', 'low', 'close']][:-1]

        ## 전처리
        mean = x_data[symbol].mean()
        std = x_data[symbol].std()
        x = (x_data[symbol] - mean) / std

        ticker.append(symbol)
        ind.append(model.predict(np.array([x]), verbose=0)[0][0].tolist())

    ind_df = pd.DataFrame([], columns=['symbol', 'ind'])
    ind_df['symbol']=ticker
    ind_df['ind']=ind
    ind_df = ind_df.sort_values('ind', ascending=False)
    print(str(df.iloc[-2].name)[:-9] + "기준으로 지표를 조회하였습니다.")
    today_date = df.index[-2]
    return ind_df

def signal(buy_std, sell_std):
    print("매수조건: " + str(buy_std) + " 매수조건: " + str(sell_std) + " 종목을 검색합니다.")
    global signal_list
    condition = (ind_df['ind'] > buy_std) | (ind_df['ind'] < sell_std)
    selected_rows = ind_df[condition]
    signal_list = selected_rows.values.tolist()
    return signal_list, ind_df

trade = False

while True:
    now = datetime.now()
    print(now, " 대기중입니다")
    if now.hour == 0 and now.minute > 0 and trade == False:
        '''청산'''
        trade = True
        print("dashboard 파일을 불러옵니다.")
        dashboard = pd.read_excel('dashboard.xlsx', index_col='날짜')

        condition = (dashboard['만료일'] == today_date )
        #
        close_sym = dashboard[condition]
        print(str(len(close_sym)) + "개의 종목을 청산합니다")
        for i in range(len(close_sym)):
            if close_sym['side'][i] == 'SELL':
                side = 'BUY'
            if close_sym['side'][i] == 'BUY':
                side = 'SELL'
            end_order(close_sym['symbol'][i], close_sym['amount'][i], side)
            print(close_sym['symbol'][i] + "종목을" + str(close_sym['amount'][i]) + "개 청산하였습니다.")
        # 만료일인 경우 statue를 open에서 close로 변경
        dashboard.loc[condition, 'statue'] = 'close'

        usdt = 200
        scan()
        signal(0.9, 0.1)
        print("매매를 진행합니다.")
        for i in range(len(signal_list)):
            # dashboard = pd.DataFrame('dashboard.xlsx')
            symbol = signal_list[i][0]
            if signal_list[i][1] > 0.5:
                side = 'BUY'
            if signal_list[i][1] < 0.5:
                side = 'SELL'
            amount = math.floor((usdt/cur_price(symbol))/min_units[symbol])*min_units[symbol]
            new_row = pd.DataFrame({
                'symbol' : [symbol], 'ind' : [signal_list[i][1]], 'side' : [side], 'amount' : [amount], 'statue' : ['open'], '만료일' : [today_date  + timedelta(days=7)]}, columns=dashboard.columns, index=[str(today_date)])
            dashboard = pd.concat([dashboard, new_row], ignore_index=False)
            order(signal_list[i][0], usdt, side)
        dashboard.to_excel('dashboard.xlsx', index_label='날짜')
        print("매매를 종료합니다")

        # Put your code here that you want to run at 9 am
        print("It's 9 am, time to run my code!")
        break
    else:
        time.sleep(2) # Wait for 1 minute and check again