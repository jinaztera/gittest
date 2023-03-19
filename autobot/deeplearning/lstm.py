import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# Load and preprocess the data
df = pd.read_csv('../../../Users/tomkj/DataspellProjects/study/project_1/stock_price.csv')
print(df)
training_data = df.iloc[:500, 1:2].values
sc = MinMaxScaler(feature_range=(0, 1))
scaled_data = sc.fit_transform(training_data)

# Define the training data
X_train = []
y_train = []
for i in range(60, len(training_data)):
    X_train.append(scaled_data[i-60:i, 0])
    y_train.append(scaled_data[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Define the LSTM model architecture
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(units=50, return_sequences=True))
model.add(LSTM(units=50))
model.add(Dense(units=1))

# Train the model
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=30, batch_size=32)

# Make predictions on new data
test_data = df.iloc[500:, 1:2].values
scaled_test_data = sc.transform(test_data)
X_test = []
for i in range(60, len(test_data)):
    X_test.append(scaled_test_data[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = model.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

# Plot the results
import matplotlib.pyplot as plt
plt.plot(test_data, color='red', label='Actual Stock Price')
plt.plot(predicted_stock_price, color='blue', label='Predicted Stock Price')
plt.title('Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()
