!pip install pymannkendall
!pip install mplfinance
import pymannkendall as mk
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
df = yf.download("VCB.VN", start="2026-01-01", end="2026-06-27", progress=False)
df.columns = df.columns.droplevel('Ticker')
full_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
df = df.reindex(full_date_range)
df = df.ffill()
df['simple_ret'] = df['Close'].pct_change()
df['log_ret'] = np.log(df['Close'] / df['Close'].shift(1))
fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
# Biểu đồ 1: Giá đóng cửa
ax[0].plot(df.index, df['Close'], color='red', label='GIÁ ĐÓNG CỬA')
ax[0].set_title('GIÁ ĐÓNG CỬA CỦA CỔ PHIẾU VCB')
ax[0].set_ylabel('VND')
ax[0].legend()
ax[0].grid(True)
# Biểu đồ 2: Log return
ax[1].plot(df.index, df['log_ret'], color='green', label='Log Return')
ax[1].set_title('VCB Log Return')
ax[1].set_ylabel('Log Return')
ax[1].set_xlabel('Date')
ax[1].legend()
ax[1].grid(True)
plt.tight_layout()
plt.show()
# Vẽ biểu đồ nến
mpf.plot(df, type="candle",
mav=[10, 20],
volume=True,
style="yahoo",
title="GIÁ CỔ PHIẾU VCB TỪ 1/1/2024 - 27/6/2026",
figsize=[10, 5])
#Lấy giá đóng cửa
close_prices = df["Close"].dropna().reset_index(drop=True)
#Thực hiện kiểm định Mann-Kendall
result = mk.original_test(close_prices)
# In kết quả
print("Trend:", result.trend)
print("p-value:", result.p)
print("Tau:", result.Tau)
print("Variance of S:", result.var_s)
# Diễn giải
if result.p < 0.05:
    print("==> Có xu hướng đáng kể về mặt thống kê.")
else:
    print("==> Không có xu hướng rõ ràng.")
