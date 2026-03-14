import matplotlib.pyplot as plt
import numpy as np

x = np.random.rand(50)
y = np.random.rand(50)
print(x)

plt.scatter(x, y)
plt.title('Scatter Plot')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
