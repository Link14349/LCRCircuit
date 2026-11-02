import matplotlib.pyplot as plt

colors = ['blue', 'purple', 'green', 'red', 'orange', 'black', 'gray', 'yellow', 'pink', 'brown', 'cyan', 'magenta']

def plot(xs, ys, labels, xlabel, ylabel, linestyles=None, markers=None):
    if len(xs) != len(ys):
        x = xs
        xs = [x] * len(ys)
    if linestyles is None:
        linestyles = ['-'] * len(ys)
    if markers is None:
        markers = [None] * len(ys)
    plt.figure(figsize=(8, 5))
    for i in range(len(ys)):
        plt.plot(xs[i], ys[i], color=colors[i % len(colors)], marker=markers[i], linestyle=linestyles[i], label=labels[i])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()