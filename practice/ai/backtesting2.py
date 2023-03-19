import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_candles(symbol, interval):
    url = f"https://api.binance.com/api/v1/klines?symbol={symbol}&interval={interval}"
    data = requests.get(url).json()
    candles = []
    for candle in data:
        t, o, h, l, c, v, _, _ = candle
        candles.append([t/1000, o, h, l, c, v])
    return candles

def plot_candles(candles):
    df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    plt.plot(df["timestamp"], df["close"])
    plt.show()

def moving_average(data, n):
    return np.convolve(data, np.ones(n) / n, mode="valid")

def backtest(candles, n1, n2, threshold):
    df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["ma1"] = moving_average(df["close"], n1)
    df["ma2"] = moving_average(df["close"], n2)
    df["position"] = np.where(df["ma1"] > df["ma2"], 1, -1)
    df["returns"] = df["close"].pct_change() * df["position"].shift(1)
    return df["returns"].mean()

candles = get_candles("BNBBTC", "1h")
plot_candles(candles)

n1 = 12
n2 = 26
threshold = 0.01

returns = backtest(candles, n1, n2, threshold)
print(returns)
