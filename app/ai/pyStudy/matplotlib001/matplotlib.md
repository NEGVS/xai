更稳定的解决方案（强烈推荐）

关闭 PyCharm 的 SciView。

步骤：

PyCharm
Settings
Tools
Python Scientific

取消勾选：

Show plots in tool window

然后 matplotlib 会直接弹出系统窗口，而不是 PyCharm 内嵌窗口。

1-安装
pip install matplotlib numpy
下面给你 **5 个 `matplotlib` 示例（Python）**，从 **最简单 → 逐步复杂**，每个例子都可以直接运行。

需要先安装：

```bash
pip install matplotlib numpy
```

---

# 1. 最简单：画一条折线图

适合入门理解 `plot`

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [10, 20, 25, 30]

plt.plot(x, y)

plt.title("Simple Line Chart")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")

plt.show()
```

效果：

* 一条简单折线
* 自动坐标轴

---

# 2. 多条折线图

常见于 **数据对比**

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]

y1 = [10, 20, 25, 30]
y2 = [5, 15, 20, 25]

plt.plot(x, y1, label="Series A")
plt.plot(x, y2, label="Series B")

plt.title("Multiple Line Chart")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")

plt.legend()

plt.show()
```

新增：

* `label`
* `legend()`

---

# 3. 散点图（数据分布）

常用于 **机器学习数据可视化**

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.random.rand(50)
y = np.random.rand(50)

plt.scatter(x, y)

plt.title("Scatter Plot")
plt.xlabel("X")
plt.ylabel("Y")

plt.show()
```

特点：

* 随机数据
* 50个点

---

# 4. 子图（subplot）

适合 **仪表盘 / 数据分析**

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

y1 = np.sin(x)
y2 = np.cos(x)

plt.figure(figsize=(8,4))

plt.subplot(1,2,1)
plt.plot(x, y1)
plt.title("sin(x)")

plt.subplot(1,2,2)
plt.plot(x, y2)
plt.title("cos(x)")

plt.tight_layout()

plt.show()
```

说明：

```
subplot(行,列,位置)
```

布局：

```
sin(x) | cos(x)
```

---

# 5. 综合示例（接近真实项目）

包含：

* 多图
* 样式
* 网格
* 图例
* 随机数据

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)

x = np.linspace(0, 10, 100)

y1 = np.sin(x)
y2 = np.cos(x)

noise = np.random.normal(0, 0.1, 100)

fig, ax = plt.subplots(figsize=(8,5))

ax.plot(x, y1, label="sin(x)")
ax.plot(x, y2, label="cos(x)")
ax.scatter(x, y1 + noise, alpha=0.5, label="noisy data")

ax.set_title("Matplotlib Advanced Example")
ax.set_xlabel("X")
ax.set_ylabel("Value")

ax.grid(True)
ax.legend()

plt.show()
```

新增知识点：

| 功能                         | 作用     |
| -------------------------- | ------ |
| `fig, ax = plt.subplots()` | 面向对象绘图 |
| `grid()`                   | 网格     |
| `alpha`                    | 透明度    |
| `scatter`                  | 散点     |
| `seed()`                   | 随机数固定  |

---

# matplotlib 核心结构

```
Figure (画布)
 ├── Axes (图表)
 │     ├── plot() 线
 │     ├── scatter() 点
 │     ├── bar() 柱
 │     └── hist() 直方
```

---

# 再给你一个 **常用图类型速查**

| 图类型 | 函数              |
| --- | --------------- |
| 折线图 | `plt.plot()`    |
| 散点图 | `plt.scatter()` |
| 柱状图 | `plt.bar()`     |
| 直方图 | `plt.hist()`    |
| 饼图  | `plt.pie()`     |
| 箱线图 | `plt.boxplot()` |

---

如果你愿意，我可以再给你一套 **真正实战级 matplotlib 教程（程序员必会 10 个图）**，比如：

* 股票K线图
* 机器学习训练曲线
* 热力图
* 3D图
* 实时数据刷新图

我可以整理 **一份 300 行完整 demo**，基本覆盖 **90% matplotlib使用场景**。

--Scatter
分散（动词）：指将事物分开或撒开，如 "Scatter the seeds" → "把种子分散播撒"
散落（动词/状态）：描述零散分布的状态，如 "Papers scattered on the floor" → "文件散落在地板上"
散射（物理术语）：如 "light scatter" → "光散射"
驱散（强制分散）：如 "Police scattered the crowd" → "警察驱散了人群"
