import tensorflow as tf

# 텐서 = tf.constant([[3, 4], [5,6]])
# print(텐서)
# 텐서2 = tf.constant([6, 7, 8])
# print(텐서2)
# 텐서3 = tf.constant([[1, 2], [3, 4]])
# print(텐서3)

# print(tf.add(텐서, 텐서2))

# print(텐서 * 텐서2)

# tf.add()
# tf.subtract()
# tf.divide()
# tf.multiply()
# tf.matmul()

# print(tf.matmul(텐서3, 텐서))

# 텐서3 = tf.constant([[1, 2], [3, 4]])
# print(텐서3)
#
# 텐서4 = tf.constant([[2, 2], [3, 2]])
# print(텐서4)
#
# print(tf.add(텐서3, 텐서4))
# print(텐서4.shape)

# 키 = [170, 180, 175, 160]
# 신발 = [260, 270, 265, 255]
키 = 170
신발 = 260

a = tf.Variable(0.1)
b = tf.Variable(0.2)

def 손실함수():
    예측값 = 키 * a + b
    return tf.square(260 - 예측값)

# 경사하강법
opt = tf.keras.optimizers.Adam(learning_rate=0.1)

for i in range(100):
    opt.minimize(손실함수, var_list=[a, b])
    print(a.numpy(), b.numpy())

print(a * 키 + b)