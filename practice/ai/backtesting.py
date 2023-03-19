import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Get historical price data for the symbol
symbol = "BNBBTC"
interval = "1h"
url = f"https://api.binance.com/api/v1/klines?symbol={symbol}&interval={interval}"
data = requests.get(url).json()

# Convert the data into a pandas DataFrame
prices = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                     'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                                     'Taker buy quote asset volume', 'Ignore'])
prices['Open time'] = pd.to_datetime(prices['Open time'], unit='ms')
prices['Open'] = prices['Open'].astype(float)

# Calculate the moving averages
short_ma = prices['Close'].rolling(window=3).mean()
long_ma = prices['Close'].rolling(window=12).mean()


# Define a function to calculate the strategy's performance
def calculate_performance(prices, short_ma, long_ma):
    # Create a DataFrame to store the strategy's signals
    signals = pd.DataFrame(index=prices.index)
    signals['price'] = prices['Close']
    signals['short_ma'] = short_ma
    signals['long_ma'] = long_ma
    signals['signal'] = 0.0

    # Generate the signals
    signals['signal'][3:] = np.where(short_ma[3:] > long_ma[3:], 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()

    # Create a DataFrame to store the strategy's trades
    trades = pd.DataFrame(index=signals.index)
    trades['price'] = signals['price']
    trades['returns'] = trades['price'].pct_change()
    trades['strategy'] = signals['positions'] * trades['returns']

    # Calculate the strategy's performance metrics
    strategy_return = trades['strategy'].cumsum().iloc[-1]
    strategy_return_pct = (1 + strategy_return) * 100
    max_dd = (trades['strategy'].cumsum().cummax() - trades['strategy'].cumsum()).max()
    max_dd_pct = (1 + max_dd) * 100
    sharpe_ratio = np.sqrt(365) * (trades['strategy'].mean() / trades['strategy'].std())

    # Return the performance metrics
    return strategy_return_pct, max_dd_pct, sharpe_ratio


# Backtest the strategy
strategy_return_pct, max_dd_pct, sharpe_ratio = calculate_performance(prices, short_ma, long_ma)

# Print the results
print
