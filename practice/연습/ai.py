import tensorflow as tf
import numpy as np

# Load the data and split it into training and testing sets
data = np.loadtxt('stock_data.csv', delimiter=',')
train_data = data[:int(0.8*len(data))]
test_data = data[int(0.8*len(data)):]

# Normalize the data
def normalize(data):
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    return (data - mean) / std, mean, std

train_data, mean, std = normalize(train_data)
test_data = (test_data - mean) / std

# Split the data into input features and target variable
x_train = train_data[:, :-1]
y_train = train_data[:, -1:]
x_test = test_data[:, :-1]
y_test = test_data[:, -1:]

# Create the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(x_train.shape[1],)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(x_train, y_train, epochs=100, batch_size=32)

# Evaluate the model on the test data
test_loss = model.evaluate(x_test, y_test)
print('Test Loss: ', test_loss)
