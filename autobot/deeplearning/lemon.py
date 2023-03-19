import tensorflow as tf
import pandas as pd



data = pd.read_csv('lemonade.csv')
print(data.head())
print(data[['온도']])
print(data[['판매량']])
print(data['온도'])
print(data['판매량'])
# model.fit(독립, 종속, epochs=1000)
독립 = data[['온도']]
종속 = data[['판매량']]

X = tf.keras.layers.Input(shape=[1])
Y = tf.keras.layers.Dense(1)(X)

model = tf.keras.models.Model(X, Y)
model.compile(loss='mse')

model.fit(독립, 종속, epochs=1000, verbose=0)
model.fit(독립, 종속, epochs=10)

print(model.predict(독립))
print(model.predict([[15]]))