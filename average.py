import pandas as pd #as는 별칭을 의미
import pyupbit
import matplotlib.pyplot as plt

#업비트에서 데이터 가져오기
data = pyupbit.get_ohlcv("KRW-BTC", interval="minute240") #240분 마다 가져오기


data['middle'] = data['close'].rolling(20).mean() #이전 20개 데이터에 대해 이동평균 구해서 data['movingAverage20']에 담기
data['upper'] = data['close'].rolling(20).mean() + data['close'].rolling(20).std() * 2
data['lower'] = data['close'].rolling(20).mean() - data['close'].rolling(20).std() * 2
data['selling'] = data['middle'] + (data['upper'] - data['middle']) * (2/3)
#csv 파일로 저장
# data.to_csv("bollinger-band.csv") #csv 파일로 저장

#시각화
ax = plt.gca()
data.plot(kind="line", y="middle", ax=ax)
data.plot(kind="line", y="upper", ax=ax)
data.plot(kind="line", y="lower", ax=ax)
data.plot(kind="line", y="selling", ax=ax)

plt.show()