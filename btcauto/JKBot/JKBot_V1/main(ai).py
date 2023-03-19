import ccxt
import numpy as np
import talib
import matplotlib.pyplot as plt

# Initialize the Binance exchange object
exchange = ccxt.binance()

# Define the symbol and timeframe for the price data
symbol = 'BTC/USDT'
timeframe = '1d'

# Retrieve the historical price data from Binance
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

# Convert the data to a NumPy array
ohlcv = np.array(ohlcv)
print(ohlcv)
# Extract the close prices from the ohlcv data
close_prices = ohlcv[:, 4]

# Calculate the RSI using the close prices
rsi = talib.RSI(close_prices, timeperiod=14)

# Define the buy and sell thresholds for the RSI strategy
buy_threshold = 30
sell_threshold = 70

# Initialize a variable to keep track of the investment balance
balance = 10000

# Initialize the btc and buy_price variables with default values
btc = None
buy_price = None

# Iterate over the RSI values and simulate the investment strategy
for i in range(1, len(rsi)):
    # If the RSI is below the buy threshold, buy some Bitcoin
    if rsi[i - 1] < buy_threshold:
        # Calculate the amount of Bitcoin to buy
        btc = balance / close_prices[i]

        # Update the balance
        balance = balance

        # Store the price at which the Bitcoin was bought
        buy_price = close_prices[i]

    # If the RSI is above the sell threshold, sell the Bitcoin
    if btc is not None and rsi[i - 1] > sell_threshold:
        # Calculate the profit from selling the Bitcoin
        profit = btc * close_prices[i] - buy_price * btc

        # Update the balance
        balance += balance + profit

        # Reset the buy_price and btc variables
        buy_price = None
        btc = None

# Print the final balance
print(f'Final balance: {balance}')


# Create a list to store the balance over time
balances = [100]

# Iterate over the RSI values and simulate the investment strategy
btc = None
for i in range(1, len(rsi)):
    # If the RSI is below the buy threshold, buy some Bitcoin
    if rsi[i - 1] < buy_threshold:
        # Calculate the amount of Bitcoin to buy
        btc = balance / close_prices[i]

        # Update the balance
        balance = balance

        # Store the price at which the Bitcoin was bought
        buy_price = close_prices[i]

    # If the RSI is above the sell threshold, sell the Bitcoin
    if rsi[i - 1] > sell_threshold:
        # Calculate the profit from selling the Bitcoin
        if btc is not None:
            profit = btc * close_prices[i] - buy_price * btc

        # Update the balance
        balance += balance + profit

        # Reset the buy_price and btc variables
        buy_price = None
        btc = None

    # Add the balance to the balances list
    balances.append(balance)

# Plot the balance over time
plt.plot(balances)
plt.xlabel('Time (days)')
plt.ylabel('Balance (USDT)')
plt.show()

