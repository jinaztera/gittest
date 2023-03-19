import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

lr = LinearRegression()

data = pd.read_excel("Test.xlsx")

x_data = np.array(data["Input"])
y_data = np.array(data["Output"])

train_input, test_input, train_target, test_target = train_test_split(
    x_data, y_data, random_state=42)

print(train_input)

# print(type(x_data))
train_poly = np.column_stack((train_input ** 3, train_input ** 2, train_input))
test_poly = np.column_stack((test_input ** 3, test_input ** 2, test_input))
print(train_poly)

lr.fit(train_poly, train_target)
# print(lr.score(test_poly, test_target))
# print(lr.predict(test_poly), test_target)
# print(lr.coef_, lr.intercept_)

print(lr.predict([[-27, 9, -3]]))
