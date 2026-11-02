# 利用快速傅里叶变换的 LCR 电路品质因数测量

复旦大学大学物理实验 I 课程论文、实验原始数据与数据处理代码。

用示波器采集方波激励下 LCR 电路的 $U_1$、$U_2$ 波形，通过 FFT 得到 $U_2/U_1$ 的频率响应曲线，再用最小二乘法拟合出电感 $L$、电容 $C$、回路内阻 $r$ 及品质因数 $Q$，并与传统逐点变频测量方法对比。

- 论文 PDF：[article/main.pdf](article/main.pdf)
- 论文源码：[article/main.tex](article/main.tex)

## 主要结果

| 测量方式 | $f_0$ / kHz | $Q$ | $L$ / mH | $C$ / nF | $r$ / Ω |
| --- | --- | --- | --- | --- | --- |
| FFT（未截断） | 16.103 ± 0.039 | 1.803 ± 0.050 | 9.792 | 9.976 | 49.4 |
| FFT（截断至 0.53–23.85 kHz） | 16.112 ± 0.041 | 1.791 ± 0.039 | 9.733 | 10.025 | 50.2 |
| 逐点法（固定 $U_1$） | 16.071 ± 0.016 | 1.815 ± 0.011 | 9.818 | 9.989 | 46.3 |
| 逐点法（记录 $U_2/U_1$） | 16.072 ± 0.012 | 1.815 ± 0.009 | 9.813 | 9.993 | 46.0 |

完整拟合输出（含各项不确定度）见 [measure_conclusion.txt](measure_conclusion.txt)。

## 目录结构

```text
.
├── article/                  # LaTeX 论文
│   ├── main.tex
│   ├── main.pdf              # 编译好的论文
│   └── reference.bib
├── images/                   # 论文插图
│   ├── circuit.png
│   ├── meth1-fitting.png
│   ├── meth2-fitting.png
│   └── fft/                  # FFT 频谱、截断与拟合图
├── data/                     # 实验数据
│   ├── header.txt            # 示波器采集参数
│   ├── 530.csv               # 104 MB 原始波形（未纳入 Git，见下）
│   ├── meth1.csv             # 逐点法：固定 U1，记录 U2
│   ├── meth2.csv             # 逐点法：同时记录 U1、U2
│   ├── meth1_proportion.csv  # 归一化后的 U2/U1
│   ├── meth2_proportion.csv
│   ├── fft_proportion.csv    # FFT 得到的 U2/U1 频响
│   ├── fftcut_proportion.csv # 截断到 0.53–23.85 kHz 后的数据
│   └── u2_scan_raw.csv       # 谐振点附近 U2 的补充逐点记录（探索用）
├── fft.py                    # 原始波形 → FFT → 频响曲线
├── meth1.py                  # 逐点法（固定 U1）数据处理
├── meth2.py                  # 逐点法（记录 U2/U1）数据处理
├── measure.py                # 频响曲线拟合，求 f0、Q、L、C、r
├── fit.py                    # curve_fit 封装：参数、误差、R²、简约卡方
├── plot.py                   # 统一绘图样式
├── measure_conclusion.txt    # 各方法拟合结果汇总
└── requirements.txt
```

## 环境依赖

- Python 3.9+：`numpy`、`pandas`、`scipy`、`matplotlib`

```bash
pip install -r requirements.txt
```

- 编译论文另需 TeX Live（`xelatex`、`biber`，以及 `ctex`、`biblatex-gb7714-2015` 宏包）

## 复现步骤

所有脚本都在仓库根目录下运行（数据路径为相对路径 `./data/`）。

### 1. FFT 法

```bash
python fft.py
```

程序读取 `data/530.csv`，以方波相邻两次上升沿（约 1.887 ms，对应 530 Hz 基频）为窗做 FFT，取 50 kHz 以内的奇次谐波，输出 `data/fft_proportion.csv`，并弹出 $U_2/U_1$、$U_1$ 幅值、$U_2$ 幅值三张图。

> 需要原始数据文件 `data/530.csv`，它未纳入版本控制，见「数据说明」。需要用u盘到示波器中导出，选择导出为.csv文件格式来取数，应当导出原始波形。

### 2. 逐点变频法

```bash
python meth1.py   # -> data/meth1_proportion.csv
python meth2.py   # -> data/meth2_proportion.csv
```

### 3. 拟合求电路参数

```bash
python measure.py
```

按提示输入数据文件名前缀（`meth1`、`meth2`、`fft`、`fftcut` 之一），程序读取 `data/<前缀>_proportion.csv`，按

$$
\frac{U_2}{U_1} = \frac{1}{\sqrt{\left(2\pi f L/R - \frac{1}{2\pi f C R}\right)^2 + \left(1 + \frac{r}{R}\right)^2}}
$$

拟合出 $L$、$C$、$r$，并计算 $f_0$、$Q$ 及其不确定度，同时在图上叠加拟合曲线与理想曲线。

绘图函数使用 `plt.show()` 弹窗显示；如需保存图片，可在 `plot.py` 中改用 `plt.savefig(...)`。

## 数据说明

- **`data/530.csv` 未纳入版本控制。** 这是示波器（SDS1102X-E）导出的原始波形，约 104 MB，超过 GitHub 单文件 100 MB 的限制。把它放回 `data/530.csv` 即可运行 `fft.py` 复现 FFT 结果；其余脚本只依赖已提交的处理后数据，可直接运行。
- 原始波形格式：`Second, CH1, CH2` 三列，采样间隔 2 ns，约 336 万点；CH1 为信号源两端电压 $U_1$，CH2 为电阻两端电压 $U_2$。采集参数见 `data/header.txt`。
- `data/fftcut_proportion.csv` 为 `fft_proportion.csv` 截断到 0.53–23.85 kHz 后的数据，用于论文中「截断前后」的对比。
- `data/u2_scan_raw.csv` 为谐振点附近补充采集的 $U_2$–$f$ 逐点记录，仅作探索，未参与论文最终拟合。

## 编译论文

```bash
cd article
xelatex main.tex
biber main
xelatex main.tex
xelatex main.tex
```

或直接 `latexmk -xelatex main.tex`。论文中的图片通过 `../images/` 引用，需在 `article/` 目录内编译。

## 说明

本项目为大学物理实验课程作业，欢迎参考与交流；引用论文内容请遵循学术规范。
