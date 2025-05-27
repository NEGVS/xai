import numpy as np

import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mp
from ipywidgets import interact
mp.use('TkAgg')  # 或其他后端，如 'Qt5Agg'


def plot_pred(w, b):
    data = pd.read_csv("/Users/andy_mac/PycharmProjects/xai/static/csv/ml.csv")
    # print(data)
    # y = w* x+ b
    x = data["YeaysExperience"]
    y = data["Salary"]
    y_pred = x * w + b
    # 1-
    # plt.scatter(x, y, marker="x", color="purple", label="real")
    # plt.title("Year Experience`s Salary")
    # plt.xlabel("Experience[Year]")
    # plt.ylabel("Salary[th]")
    #
    # plt.plot(x, y_pred, color="blue", label="pred")
    # plt.xlim([0, 4])
    # plt.ylim([-10, 80])
    # plt.legend()
    compute_cost(x, y, 10, 0)
    costs = []
    for w in range(-100, 101):
        cost = compute_cost(x, y, w, 0)
        costs.append(cost)
    #     2-
    plt.plot(range(-100, 101), costs)
    plt.title("cost function b =0,w=-100~100")
    plt.xlabel("w")
    plt.ylabel("cost")

    ws = np.arange(-100, 101)
    bs = np.arange(-100, 101)
    costs = np.zeros((201, 201))
    i = 0
    for w in ws:
        j = 0
        for b in bs:
            cost = compute_cost(x, y, w, b)
            costs[i, j] = cost
            j = j + 1
        i = i + 1
    print(costs)
    # 3-
    # plt.show()
    plt.figure(figsize=(15, 15))
    ax = plt.axes(projection="3d")
    ax.xaxis.set_pane_color((0, 1, 0))
    ax.yaxis.set_pane_color((0, 0, 1))
    ax.zaxis.set_pane_color((1, 0, 0))
    b_grid, w_grid = np.meshgrid(bs, ws)
    ax.plot_surface(w_grid, b_grid, costs, cmap="Spectral_r", alpha=0.7)
    ax.plot_wireframe(w_grid, b_grid, costs, color="white", alpha=0.7)
    ax.set_title("w b -->cost")
    ax.set_xlabel("w")
    ax.set_xlabel("b")
    ax.set_xlabel("cost")
    ax.view_init(45, -120)
    w_index, b_index = np.where(costs == np.min(costs))
    ax.scatter(ws[w_index], bs[b_index], costs[w_index, b_index], color="black", s=40)
    plt.show()
    print(np.min(costs))
    print(w_index, b_index)
    print(ws[w_index], bs[b_index])

def compute_cost(x,y,w,b):
    y_pred= w* x+b
    cost= (y-y_pred)**2
    cost=cost.sum()/len(x)
    return cost
plot_pred(0, 0)
interact(plot_pred,w=(-100,100,1),b=(-100,100,1))

# print(x)
# print(y)
