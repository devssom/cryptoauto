import time
import pyupbit
import datetime

access = "mBIyU4bW43brGanxA59SqeXTcdmlCGmBLCAh37y4"
secret = "CFudL2VGQxveT6KTXX66mZ6DkA6V2jxFqRtUv0oq"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=7)    # 이틀치에 해당하는 일 데이터를 조회하고
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k    # 변동성 돌파 전략 사용
    # df.iloc[0]['close'] : 다음날 시가, (df.iloc[0]['high'] - df.iloc[0]['low']) * k : 변동폭
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-DOGE")   # 오전 9시가 시작시간
        end_time = start_time + datetime.timedelta(days=1)   # 다음날 오전 9시가 마감시간
        
        # 오전 9시 < 현재 < 다음날 오전 8시 59분 50초
        if start_time < now < end_time - datetime.timedelta(seconds=10):   # 8시 59분 50초까지 돌아가
            target_price = get_target_price("KRW-DOGE", 0.6)    # 매수 목표가 설정
            current_price = get_current_price("KRW-DOGE")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:    # 최소거래금액이 5000원
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)    # 이때 수수로 0.05%를 고려해서 0.9995
        else:
            btc = get_balance("DOGE")    # 10초 전부터는 당일 종가에 비트코인을 전량 매도하는 코드
            if btc > 0.00008:    # 비트코인 가지고 있는게 5000원 이상이면
                upbit.sell_market_order("KRW-DOGE", btc*0.9995)    # 전량매도, 수수료 제외
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)