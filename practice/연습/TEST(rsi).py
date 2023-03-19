import pandas as pd
import numpy as np
import ta
from ta.momentum import RSIIndicator

# Load data from Binance using Binance API
df = pd.read_csv('https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&startTime=<start_time>&endTime=<end_time>')

# Clean and preprocess the data
df.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
df = df[['Open time', 'Open', 'High', 'Low', 'Close', 'Volume']]
df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
df = df.set_index('Open time')
df.dropna(inplace=True)

# Calculate RSI indicator
rsi = RSIIndicator(df["Close"], n=14)
df["RSI"] = rsi.rsi()

# Define RSI investment strategy
def rsi_strategy(row):
    if row['RSI'] > 70:
        return 'Sell'
    elif row['RSI'] < 30:
        return 'Buy'
    else:
        return 'Hold'

# Apply RSI investment strategy to the data
df['Signal'] = df.apply(rsi_strategy, axis=1)

# Calculate returns
df['Returns'] = np.log(df['Close'] / df['Close'].shift(1))
df['Strategy'] = df['Returns'] * (df['Signal'].shift(1) == 'Buy').astype(int)

# Calculate cumulative returns
df['Cumulative Returns'] = (df['Strategy'] + 1).cumprod()

# Plot cumulative returns
df['Cumulative Returns'].plot(figsize=(10, 5))
