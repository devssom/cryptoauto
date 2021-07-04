import pyupbit

access = "mBIyU4bW43brGanxA59SqeXTcdmlCGmBLCAh37y4"          # 본인 값으로 변경
secret = "CFudL2VGQxveT6KTXX66mZ6DkA6V2jxFqRtUv0oq"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회