import pandas as pd
import openpyxl
import numpy as np
import tensorflow as tf

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

df = pd.read_excel("Test.xlsx")
# x_data = df['Input'].values
# y_data = df['Output'].values
# print(df['Input'].values)
# print(df['Output'].values)
# print(np.array(df["Input"]))
# print(type(np.array(df["Input"])))
x_data = []
y_data = []

X = np.array(df["Input"])
Y = np.array(df["Output"])
for i, rows in df.iterrows():
    x_data.append([rows["Input"]])
    y_data.append([rows["Output"]])

print(x_data, y_data)

# model = Sequential()
#
# model.add(LSTM(units=32, input_shape=(1, 1)))
# model.add(Dense(units=1))
#
# model.compile(loss='mae', optimizer='adam')
#
# model.fit(X[:, np.newaxis], Y, epochs=100, verbose=1)
#
# predict = model.predict(np.array([10]).reshape(1, 3, 1))

model = tf.keras.models.Sequential([
    # tf.keras.layers.Dense(4), #activation='relu'), # 레이어 개수, 함수
    # tf.keras.layers.Dense(4),
    tf.keras.layers.Dense(1)#, activation='relu')
])

model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
#binary_crossentropy 확률

print(np.array(x_data))
model.fit(np.array((x_data)), np.array((y_data)), epochs=50)

예측값 = model.predict([[2], [8], [10]])
print(예측값)