# ...existing code...
import numpy as np
from scipy.optimize import curve_fit
from plot import plot

def fit(func, x, y, p0=None, sigma=None, absolute_sigma=False):
    """
    对给定函数 func(x, *params) 和数据 x,y 做最小二乘拟合。
    返回 (popt, perr, pcov, r, r_squared, reduced_chi2)
      - popt: 最佳参数数组
      - perr: 参数 1σ 不确定度（从协方差矩阵开根号）
      - pcov: 协方差矩阵（可能为 inf 或 nan，需检查）
      - r: 拟合值与原始 y 的皮尔逊相关系数
      - r_squared: 决定系数 R^2
      - reduced_chi2: 简约卡方：ss_res / (N - n_params)
    参数:
      func: 可调用对象 f(x, *params)
      x, y: 一维数组
      p0: 初始猜测参数（可 None）
      sigma: 数据点的标准差（可 None）
      absolute_sigma: 传递给 scipy.curve_fit，若 True 则 sigma 作为绝对误差
    依赖: scipy.optimize.curve_fit
    """
    x = np.asarray(x)
    y = np.asarray(y)
    popt, pcov = curve_fit(func, x, y, p0=p0, sigma=sigma, absolute_sigma=absolute_sigma)
    # 参数不确定度
    if pcov is None:
        perr = np.full_like(popt, np.nan, dtype=float)
    else:
        perr = np.sqrt(np.diag(pcov))
        # 若协方差包含 inf/nan，保为 nan
        perr = np.where(np.isfinite(perr), perr, np.nan)

    # 拟合值与残差
    y_fit = func(x, *popt)
    residuals = y - y_fit
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y - np.mean(y))**2)

    # 决定系数 R^2（若 ss_tot==0 则为 nan）
    r_squared = 1.0 - ss_res / ss_tot if ss_tot != 0 else np.nan

    # 皮尔逊相关系数 r（拟合值与原始 y）
    try:
        r = np.corrcoef(y, y_fit)[0,1]
    except Exception:
        r = np.nan

    # 简约卡方
    dof = max(1, len(y) - len(popt))
    reduced_chi2 = ss_res / dof

    return popt, perr, pcov, r, r_squared, reduced_chi2

# 简单示例
if __name__ == "__main__":
    # 合成测试数据：二次函数带噪声
    def model(x, a, b, c):
        return a * x**2 + b * x + c

    rng = np.random.default_rng(0)
    x = np.linspace(-1, 1, 100)
    y_true = model(x, 2.0, -1.0, 0.5)
    y = y_true + rng.normal(scale=0.05, size=x.size)

    popt, perr, pcov, r, r2, redchi2 = fit(model, x, y, p0=[1,0,0])
    print("popt:", popt)
    print("perr:", perr)
    print("r:", r)
    print("R^2:", r2)
    print("reduced_chi2:", redchi2)
    plot(x, [y, model(x, *popt)], ['data', 'fit'], 'x', 'y', linestyles=['', '-'], markers=['x', None])
# ...existing code...