# 用于拟合曲线, 测量结果
import pandas as pd
from plot import plot
from fit import fit
import numpy as np

path = f'./data/{input("Filename: ")}_proportion.csv'
def model(f, l, c, r):
    return 1 / np.sqrt((2 * np.pi * f * l - 1 / (2 * np.pi * f * c)) ** 2 + r**2)

df = pd.read_csv(path, sep=",")

R = 500

f = df.iloc[:,0].values.astype(float)
y = df.iloc[:,1].values.astype(float)

popt, perr, pcov, r, r2, redchi2 = fit(model, f, y, p0=[10e-3 / R, 10e-9 * R, 1])

L = popt[0] * R
C = popt[1] / R
r_ = (popt[2] - 1) * R

Lerr = perr[0] * R
Cerr = perr[1] / R
rerr = perr[2] * R

f0 = 1 / (2 * np.pi * np.sqrt(L * C))
Q=np.sqrt(L / C) / (R+r_)

f0err = f0 / 2 * np.sqrt((Lerr / L) ** 2 + (Cerr / C) ** 2)
Qerr = Q * np.sqrt((Lerr / L / 2) ** 2 + (Cerr / C / 2) ** 2 + (rerr / r_) ** 2)

print(f"f0={f0*1e-3}kHz, Q={Q}")
print(f"f0err={f0err*1e-3}kHz, Qerr={Qerr}")
print(f"L={L*1e3}mH, C={C*1e9}nF, r_={r_}Ω")
print(f"Lerr={Lerr*1e3}mH, Cerr={Cerr*1e9}nF, r_err={rerr}Ω")
print("r:", r)

x = np.linspace(f[0], f[-1], 1000)

# print(model(x, *popt))

plot([f / 1e3, x / 1e3, x / 1e3], [y, model(x, *popt), model(x, popt[0], popt[1], 1)], ['data', 'fit', "idealized"], 'kHz', 'U2/U1', linestyles=['', '-', '--'], markers=['x', None, None])