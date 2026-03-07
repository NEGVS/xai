import numpy as np
import tensorflow as tf
# from torch.backends.mkl import verbose

print('tensorflow version:')
print(tf.__version__)

# import numpy as np
print('numpy version:')

print(np.__version__)

# 定义张量
a = tf.constant([[1, 2], [3, 4]])
b = tf.constant([[5, 6], [7, 8]])

# matrix add
c = tf.add(a, b)
# matrix mul
d = tf.matmul(a, b)
print("-------------add result:\n", c)
print("---------mul result:\n", d)

# 生成模拟数据
x = np.array([[1], [2], [3], [4]], dtype=float)
# y = 2x
y = np.array([[2], [4], [6], [8]], dtype=float)

# 定义模型,单层全连接网络
model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[1])
])
# 编译模型
model.compile(optimizer='sgd', loss='mean_squared_error')
# 训练模型
model.fit(x, y, epochs=500, verbose=0)
# 预测
print("预测结果：\n", model.predict(np.array([[5]])))

print("GPU 可用：" if tf.config.list_logical_devices('GPU') else "GPU 不可用")

print('load data...')
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
print('pre doing...')
# 归一化
x_train = x_train / 255.0
# 构建模型,Sequential API（简单模型）
model_sequential = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
# 构建模型,Functional API（复杂模型）
inputs = tf.keras.Input(shape=(28, 28))
x2 = tf.keras.layers.Flatten()(inputs)
x2 = tf.keras.layers.Dense(128, activation='relu')(x2)
outputs = tf.keras.layers.Dense(10, activation='softmax')(x2)
model_functional = tf.keras.Model(inputs=inputs, outputs=outputs)
# compile
model_sequential.compile(optimizer='adam',
                         loss='sparse_categorical_crossentropy',
                         metrics=['accuracy'])
# train
model_sequential.fit(x_train, y_train, epochs=5, batch_size=32)
# evaluate
model_sequential.evaluate(x_test, y_test)
# save and load model
model_sequential.save('my_model.h5')
# load
model_sequential = tf.keras.load_model('my_model.h5')