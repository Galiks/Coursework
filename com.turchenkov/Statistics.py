import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def test_func(time_pool, time_not_pool):
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 10})
    ax = plt.axes()
    ax.yaxis.grid(True, zorder=1)

    days = [1, 2, 3, 4, 5, 6, 7]
    x_axis = np.arange(len(days))

    plt.bar(
        [x + 0.3 for x in x_axis],
        [d for d in time_pool],
        width=0.2,
        color='blue',
        label='pool',
        alpha=0.7,
        zorder=2
    )

    plt.bar(
        [x + 0.05 for x in x_axis],
        [d for d in time_not_pool],
        width=0.2,
        color='red',
        label='not pool',
        alpha=0.7,
        zorder=2
    )

    plt.xticks(x_axis, days)
    plt.legend(loc='upper left')
    fig.savefig('Graph.png')
    plt.show()


if __name__ == '__main__':
    time_not_pool = []
    time_pool = []

    for line in open("Program's time NotPool.txt"):
        time = str(datetime.timedelta(seconds=int(line[5:9])))
        time_not_pool.append(time)

    for line in open("Program's time Pool.txt"):
        time = str(datetime.timedelta(seconds=int(line[5:8])))
        time_pool.append(time)

    time_pool.sort()
    time_not_pool.sort()

    test_func(time_pool, time_not_pool)
