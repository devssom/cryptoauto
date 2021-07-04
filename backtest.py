import pyupbit
import numpy as np

# OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
df = pyupbit.get_ohlcv("KRW-BTC", count=7)  # 7일동안의 원화-BTC

# 변동성 돌파전략에서 매수가를 구하기 위한 코드 : 변동폭 * k 계산, (고가 - 저가) * k값. 처음엔 k값을 0.5로 잡아줌
df['range'] = (df['high'] - df['low']) * 0.5

# target(매수가), range 컬럼을 한칸씩 밑으로 내림(.shift(1))
# range는 전날, open은 당일 시가. 더해줘서 타겟 매수가를 만들어줘
df['target'] = df['open'] + df['range'].shift(1)
print(df)

# ror(수익률), np.where(조건문, 참일때 값, 거짓일때 값)
df['ror'] = np.where(df['high'] > df['target'],  # high 고가가 목표가 보다 높게되면 (매수) -> 이게 참이라면
                     df['close'] / df['target'], # 종가에 매도를 하게 되니까 (종가/목표가) = 수익률. 
                     1)    # 그리고 거짓일때는, 매수를 하지 않게 되니까 수익률은 그냥 그대로 1

# 수익률을 누적해서 곱해서 계산(cumprod) -> 누적수익률 
df['hpr'] = df['ror'].cumprod()

# Draw Down (하락폭) 계산을 해주기 위해서 -> (누적 최대값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# MDD (Draw Down의 최대값)
 print("MDD(%): ", df['dd'].max())

# 이렇게 계산한 값들을 엑셀로 출력
df.to_excel("dd.xlsx")