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
print(a)
print(b)
# matrix add
c = tf.add(a, b)

# matrix mul
# 1，2
# 3，4
#
# 5，6，
# 7，8
#
# 1行X1列。    5+14=19
# 1行X2列。    1*6+2*8=6+16=22
# 2行X1列。    3*5+4*7=15+28=43
# 2行X2列。    3*6+4*8=18+32=50
d = tf.matmul(a, b)

print("-------------add result:\n", c)
print("---------mul result:\n", d)
