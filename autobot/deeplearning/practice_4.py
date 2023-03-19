import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


ss = StandardScaler()

data = pd.read_excel("Test.xlsx")

x_data = np.array(data["Input"])
y_data = np.array(data["Output"])

x_data = x_data.reshape(-1, 1)
y_data = y_data.reshape(-1, 1)
# print(x_data, y_data)

train_input, test_input, train_target, test_target = train_test_split(
    x_data, y_data, random_state=20)

# print(train_input, train_target)

poly = PolynomialFeatures(degree=5, include_bias=False)

# print(train_input)
poly.fit(train_input)
train_poly = poly.transform(train_input)
test_poly = poly.transform(test_input)

print(train_poly.shape)

ss.fit(train_poly)
train_scaled = ss.transform(train_poly)
test_scaled = ss.transform(test_poly)

# print(train_poly)
# print(train_scaled.shape, train_target.shape)
ridge = Ridge()
ridge.fit(train_poly, train_target)
print(ridge.score(train_poly, train_target))
print(ridge.score(test_poly, test_target))

print(poly.transform([[3]]))
print(ridge.predict(poly.transform([[9]])))

#
#

#
#
#
# print(train_input)
# print(type(x_data))
# train_poly = np.column_stack((train_input ** 3, train_input ** 2, train_input))
# test_poly = np.column_stack((test_input ** 3, test_input ** 2, test_input))
# print(train_poly)
#
# lr.fit(train_poly, train_target)
# print(lr.score(test_poly, test_target))
# print(lr.predict(test_poly), test_target)
# print(lr.coef_, lr.intercept_)
#
# print(lr.predict([[-27, 9, -3]]))
