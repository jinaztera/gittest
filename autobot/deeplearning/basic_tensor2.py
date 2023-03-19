import tensorflow as tf
import pandas as pd
import numpy as np

data = pd.read_csv("gpascore.csv")

data = data.dropna()
# print(df.isnull().sum())
# print(data['gre'])
# exit()
# print(data)

y데이터 = data['admit'].values #리스트로 담기
print(y데이터)

x데이터 = []
for i, rows in data.iterrows():
    x데이터.append([rows['gre'], rows['gpa'], rows['rank']])

print(x데이터)



# 딥러닝 모델 만드는 법
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='tanh'), # 레이어 개수, 함수
    tf.keras.layers.Dense(128, activation='tanh'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#binary_crossentropy 확률

model.fit(np.array(x데이터), np.array(y데이터), epochs=1000)

예측값 = model.predict([[750, 3.70, 3]])
print(예측값)