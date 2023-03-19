import requests
import pandas as pd
import matplotlib.pyplot as plt

# Get the data
symbol = "BTCUSDT"
interval = "1d"
url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=1000"
data = requests.get(url).json()

# Convert the data into a pandas DataFrame
prices = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
prices['Open time'] = pd.to_datetime(prices['Open time'], unit='ms')
prices['Close'] = prices['Close'].astype(float)

# Plot the data
plt.plot(prices['Open time'], prices['Close'])
plt.xlabel('Date')
plt.ylabel('Closing price')
plt.title('Bitcoin price data from Binance')
plt.show()
