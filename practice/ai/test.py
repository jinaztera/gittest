import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

symbol = "BTCUSDT"
interval = "1d"
url = f"https://api.binance.com/api/v1/klines?symbol={symbol}&interval={interval}"

data = requests.get(url).json()
prices = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                     'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                                     'Taker buy quote asset volume', 'Ignore'])

prices['Open time'] = pd.to_datetime(prices['Open time'], unit='ms')
prices['Open'] = prices['Open'].astype(float)

# Get the last 100 days of data
prices = prices.iloc[-100:]

plt.plot(prices['Open time'], prices['Close'])
plt.xlabel('Date')
plt.ylabel('Price (USDT)')
plt.title('Bitcoin Price (Last 100 Days)')
plt.show()
