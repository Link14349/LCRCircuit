import pandas as pd
from pathlib import Path
from plot import plot
import numpy as np
pd.options.display.float_format = '{:.9f}'.format

def fft(df, signal_col, t_start, t_end):
    t = df.iloc[:, 0].values.astype(float)
    y = df.iloc[:, signal_col].values.astype(float)

    mask = (t >= t_start) & (t <= t_end) # 取指定时间段做矩形窗

    t_seg = t[mask]
    y_seg = y[mask]

    # plot(t_seg * 1e3, [y_seg], [str(df.columns[signal_col])], xlabel="ms", ylabel="V")

    # 采样间隔（秒）
    dt = np.mean(np.diff(t_seg))

    N = len(y_seg)

    yf = np.fft.rfft(y_seg)
    xf = np.fft.rfftfreq(N, dt)

    # 单边幅值归一化
    amplitude = (2.0 / N) * np.abs(yf)

    # cutoff
    xf = xf[xf < 50e3] # 50kHz
    amplitude = amplitude[:len(xf)]

    return xf, amplitude

data_path = Path("./data/530.csv")
if not data_path.exists():
    raise SystemExit(
        "未找到原始波形 data/530.csv（约 104 MB，超过 GitHub 单文件限制，未纳入版本控制）。\n"
        "请把示波器导出的原始文件放回 data/530.csv 后重试，详见 README「数据说明」。"
    )

df = pd.read_csv(data_path, sep=',')

# 取前三列（按位置）
x = df.iloc[:, 0]
y1 = df.iloc[:, 1]
y2 = df.iloc[:, 2]

trigger = df[y1 > 2.9].head(2)[df.columns[0]]
t1 = trigger.iloc[0]
t2 = trigger.iloc[1]
print(t1, t2)

# plot(x * 1e3, [y1, y2], [str(df.columns[1]), str(df.columns[2])], "ms", 'V')
xf, U1A = fft(df, 1, t1, t2)
xf, U2A = fft(df, 2, t1, t2)

mask = [False]
for i in range(1, len(xf), 2):
    mask.append(True)
    mask.append(False)

# print(mask)
xf = xf[mask]
U1A = U1A[mask]
U2A = U2A[mask]

df = pd.DataFrame({"f(Hz)": xf, "U2/U1": U2A / U1A})
df.to_csv('./data/fft_proportion.csv', index=False)
plot(xf / 1e3, [U2A / U1A], ["U2/U1"], xlabel="kHz", ylabel="1")

plot(xf / 1e3, [U1A], ["U1 Amplitude"], xlabel="kHz", ylabel="V")
plot(xf / 1e3, [U2A], ["U2 Amplitude"], xlabel="kHz", ylabel="V")