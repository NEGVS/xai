import numpy as np
import tensorflow as tf

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
