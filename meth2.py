import pandas as pd
from plot import plot

path = './data/meth2.csv'
df = pd.read_csv(path, sep=",")
df.iloc[:, 0] *= 1e3
df[df.columns[2]] /= df[df.columns[1]]
df.columns = ['f(Hz)', 'U1(V)', 'U2/U1']

x = df.iloc[:, 0]

sel = df.iloc[:, [0, 2]]

sel.to_csv('./data/meth2_proportion.csv', index=False)
plot(x / 1e3, [df.iloc[:, 2]], ['U2/U1'], 'kHz', 'U2/U1')