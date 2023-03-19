import pandas as pd
import openpyxl
import numpy as np
import tensorflow as tf

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

data = pd.read_excel("Test.xlsx")

# x_data = []
# y_data = []
#
# X = np.array(data["Input"])
# Y = np.array(data["Output"])
# for i, rows in data.iterrows():
#     x_data.append([rows["Input"]])
#     y_data.append([rows["Output"]])
#
# print(x_data, y_data)

독립 = data[['Input']]
종속 = data[['Output']]

X = tf.keras.layers.Input(shape=[1])

H = tf.keras.layers.Dense(20)(X)
H = tf.keras.layers.BatchNormalization()(X)
H = tf.keras.layers.Activation('swish')(X)

H_2 = tf.keras.layers.Dense(20)(H)
H_2 = tf.keras.layers.BatchNormalization()(H)
H_2 = tf.keras.layers.Activation('swish')(H)

Y = tf.keras.layers.Dense(1)(H_2)

model = tf.keras.models.Model(X, Y)
model.compile(loss='mae', metrics=['accuracy'])

model.fit(독립, 종속, epochs=1000)
# model.fit(독립, 종속, epochs=10,)

print(model.predict(독립))
print(model.predict([[-3], [-10]]))