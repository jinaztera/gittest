import requests
import pandas as pd
import matplotlib.pyplot as plt

# Binance API endpoint to get the historical price data of Bitcoin
url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=100"

# Send a request to the API endpoint to get the data
response = requests.get(url)

# Parse the response data into a Pandas dataframe
data = response.json()
df = pd.DataFrame(data, columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])

# Keep only the date and closing price columns
df = df[["Close time", "Close"]]

# Convert the Unix timestamps to dates
df["Close time"] = pd.to_datetime(df["Close time"], unit='ms')

# Set the date column as the index
df.set_index("Close time", inplace=True)

# Plot the closing price on the y-axis and date on the x-axis
plt.plot(df["Close"])
plt.xlabel("Date")
plt.ylabel("Closing Price (USDT)")
plt.title("Bitcoin Price (Past 100 Days)")
plt.show()
