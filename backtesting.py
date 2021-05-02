# ch07/07_13.py
import pyupbit
import numpy as np

# OHLCV(open, high, low, close, volume) - 시가, 고가, 저가, 종가, 거래량
df = pyupbit.get_ohlcv("KRW-BTC", count = 30 )

# 변동성 돌파 전략 - 매수량 계산
# 변동폭 * k 계산, (고가 - 저가) * k
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1) 

# ror(수익률), np.where(조건문,참, 거짓)
fee = 0.0005
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee, 1)

# 누적 곱 계산(cumprod) => 누적 수익률
df['hpr'] = df['ror'].cumprod()

# Draw Down 계산(누적 최대 값과 현재 hpr차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

print("MDD(%): ", df['dd'].max())
df.to_excel("Larry.R.Williams.xlsx")