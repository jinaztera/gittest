import requests
import pandas as pd
import matplotlib.pyplot as plt

# Define the symbol, interval and number of days
symbol = "BTCUSDT"
interval = "1d"
days = 1000

# Construct the URL for the API request
url = f"https://api.binance.com/api/v1/klines?symbol={symbol}&interval={interval}&limit={days}"

# Retrieve the data
data = requests.get(url).json()

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                                 'Taker buy quote asset volume', 'Ignore'])
df['Date'] = pd.to_datetime(df['Close time'], unit='ms')
df.set_index('Date', inplace=True)

# Plot the data
plt.plot(df.index, df['Close'].astype(float), label='Close price')
plt.xlabel('Date')
plt.ylabel('Price (USDT)')
plt.title(f"{symbol} closing price in the past {days} days")
plt.legend()
plt.show()
