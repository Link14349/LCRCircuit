import pandas as pd
from plot import plot

path = './data/meth1.csv'
df = pd.read_csv(path, sep=",")
df.iloc[:, 1] /= 1.4  # U1 保持 1.4 V 不变，直接归一化
df.iloc[:, 0] *= 1e3
df.columns = ['f(Hz)', 'U2/U1']

x = df.iloc[:, 0]
y1 = df.iloc[:, 1]

df.to_csv('./data/meth1_proportion.csv', index=False)
plot(x / 1e3, [y1], ['U2/U1'], 'kHz', 'U2/U1')