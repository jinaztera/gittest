import tensorflow as tf
import numpy as np

# Generate some data with power relationship
x = np.linspace(0, 100, 100)
y = 2 * x ** 2

# Create a TensorFlow model with a single dense layer
model = tf.keras.Sequential([
    tf.keras.layers.Dense(1, input_shape=[1])
])

# Compile the model with mean squared error loss and adam optimizer
model.compile(loss='mse', optimizer='adam')

# Fit the model to the data
model.fit(x, y, epochs=50, verbose=0)

# Predict output values for the input data
y_pred = model.predict(x)

print(x, y, y_pred)

# Plot the input and output data, as well as the predicted output values
import matplotlib.pyplot as plt
plt.plot(x, y, 'bo', label='Original Data')
plt.plot(x, y_pred, 'r', label='Predicted Data')
plt.legend()
plt.show()
