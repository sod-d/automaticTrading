import sys
from apscheduler.schedulers.background import BackgroundScheduler
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pyupbit

from time import sleep


ui = uic.loadUiType("automaticUI.ui")[0]
class Main(QMainWindow, ui):
    """
    GUI를 구성합니다.

    기준봉을 설정하고, 봇을 실행, 중지
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        """
        봇 객체
        """
        self.bot = self.Bot()
        """
        봇 실행
        """
        self.pushButtonStart.clicked.connect(self.startBot)

        """
        봇 중지
        """
        self.pushButtonStop.clicked.connect(self.stopBot)

    def startBot(self):
        """
        봇 실행 메서드
        1. 봇이 이미 실행 중인가
        2. 기준봉이 설정되어 있는가
        3. 봇이 꺼져있으면 실행
        :return:
        """

        # 1. 봇이 이미 실행 중인가
        if self.bot.isRunning:
            return self.popup("봇이 이미 실행 중 입니다.")

        interval = self.getInterval()
        if not interval: #false라면 기준 분봉이 설정 되어있지 않음
            return self.popup("기준봉을 설정해주세요.")

        isValidStart = self.bot.firstSetting(interval)

        if not isValidStart:
            return self.popup("유효한 API키가 아닙니다.")

        self.bot.start()

    def stopBot(self):
        """
        봇 종료 메서드

        1. 봇이 실행중인지 검사
        2. 봇 종료
        :return:
        """
        if not self.bot.isRunning:
            return self.popup("실행 상태가 아닙니다.")


        if self.bot.isRunning:
            self.bot.isRunning = False
            self.bot.scheduler.remove_job("job")
            return self.popup("봇을 종료합니다.")


    def getInterval(self):
        interval = None

        if self.radioButton1.isChecked():
            interval = "minute1"
        elif self.radioButton3.isChecked():
            interval = "minute3"
        elif self.radioButton5.isChecked():
            interval = "minute5"
        elif self.radioButton15.isChecked():
            interval = "minute15"
        elif self.radioButton30.isChecked():
            interval = "minute30"
        elif self.radioButton60.isChecked():
            interval = "minute60"
        elif self.radioButton240.isChecked():
            interval = "minute240"
        elif self.radioButtonDay.isChecked():
            interval = "minuteDay"
        # 아무것도 체크하지 않았을 경우
        if not interval:
            return False

        return interval

    def popup(self, message):
        QMessageBox.information(self, "알림",message)



    class Bot(QThread):
        """
        1.Main 클래스로부터 interval 값 가져오기 (기준봉)
        2. 필요한 데이터 요청하고 게산하기 ( 상단 밴드, 중간 밴드, 매도 가격 )
        3. 봇 실행
            - 현재 가격을 조회
            - 가격 상태 판단
            - 매매 수행
        4. 봇 중지
            -봇 중지
            -스케줄러 중지
        """

        def __init__(self):
            super().__init__()
            self.isRunning = False

            """
            private API 객체
            """
            access = "Ly89Zxb3mCRaWNCttVGDZUF0YIKYJplPmxMtAbui"
            secret = "DxgBxOxsKUYaOpalM4FTirvVv7xSiMX2kClqOyi1"
            self.upbit = pyupbit.Upbit(access, secret)

            """
            기준 코인
            """
            self.ticker = "KRW-BTC"
        def run(self):
            self.startBot()

        def firstSetting(self, interval):
            isValidAPI = self.upbit.get_balance()

            if not isValidAPI:
                return False

            # 1.Main 클래스로부터 interval 값 가져오기 (기준봉)
            self.interval = interval
            self.updatePriceInfo()

            """
            updatePriceInfo 메시드를 호출하는 스케러
            """
            self.scheduler = BackgroundScheduler()

            if self.interval == "minute1":
                self.scheduler.add_job(self.updatePriceInfo, 'cron', minute="*", second="2", id="job")
            if self.interval == "minute3":
                self.scheduler.add_job(self.updatePriceInfo, 'cron', minute="*/3", second="2", id="job")
            if self.interval == "minute5":
                self.scheduler.add_job(self.updatePriceInfo, 'cron', minute="*/5", second="2", id="job")
            if self.interval == "minute10":
                self.scheduler.add_job(self.updatePriceInfo, 'cron', minute="*/10", second="2", id="job")
            if self.interval == "minute15":
                self.scheduler.add_job(self.updatePriceInfo, 'cron', minute="*/15", second="2", id="job")
            if self.interval == "minute30":
                self.scheduler.add_job(self.updatePriceInfo, 'cron', minute="*/30", second="2", id="job")
            if self.interval == "minute60":
                self.scheduler.add_job(self.updatePriceInfo, 'cron', hour="*", second="2", id="job")
            if self.interval == "minute240":
                self.scheduler.add_job(self.updatePriceInfo, 'cron', hour="1-23/4", second="2", id="job")
            if self.interval == "day":
                self.scheduler.add_job(self.updatePriceInfo, 'cron', day="*", hour="0", minute="0", second="2", id="job")

            self.scheduler.start()

            return True

        def updatePriceInfo(self):
            # 2. 필요한 데이터 요청하고 게산하기 ( 상단 밴드, 중간 밴드, 매도 가격 ) -> 스케줄러 사용
            data = pyupbit.get_ohlcv(self.ticker, interval=self.interval)

            period = 20
            multiplier = 2

            data['middle'] = data['close'].rolling(period).mean()  # 중간밴드
            data['upper'] = data['close'].rolling(period).mean() + data['close'].rolling(period).std() * multiplier  # 상단 밴드

            self.middle = data.iloc[-2]['middle']  # 이전봉 중간밴드 값
            self.upper = data.iloc[-2]['upper']  # 이전 봉 상단밴드 값
            self.prevHighPrice = data.iloc[2]['high']  # 이전봉 증가

        def startBot(self):
            """
            3. 봇 실행
                - 현재 가격을 조회
                - 가격 상태 판단
                - 매매 수행
            4. 봇 중지
                -봇 중지
                -스케줄러 중지
            :return:
            """

            if not self.isRunning:
                self.isRunning = True

            while self.isRunning:
                self.currentPrice = pyupbit.get_current_price(self.ticker)  #현재 가격 조회
                status = self.getStatus(self.currentPrice)   # 현재 가격 상태 조회
                self.tradingLogic(status)   #매매 로직 수행하기
                sleep(1) #1초를 쉬고 반복문

        def getStatus(self, currentPrice):
            """
            현재 가격 상태 반환

            매수 : 이전봉 고가는 중간밴드 아래, 현재 가격이 중간밴드를 돌파
            매도 : 상단 밴드와 중간 밴드의 2/3 지점 돌파

            매수 타이밍 : buy
            매도 타이밍 : sell
            나머지 : None
            :param currentPrice:
            :return:
            """

            targetPrice = self.middle + (self.upper - self.middle) * 2 / 3

            buyingCondition = (currentPrice > self.middle) and (self.prevHighPrice < self.middle)
            sellingCondition = currentPrice >= targetPrice

            if buyingCondition:
                return "buy"
            elif sellingCondition:
                return "sell"

            return None

        def tradingLogic(self, status):
            if not status:
                return

            if status == "buy":
                #매수
                balance = self.upbit.get_balance()

                if balance < 5000:
                    return

                self.upbit.buy_market_order(self.ticker, balance * 0.99)


            if status == "sell":
                #매도
                volume = self.upbit.get_balance(self.ticker) #가지고있는 비트 코인
                balance = volume * self.currentPrice

                if balance < 5000:
                    return

                self.upbit.sell_market_order(self.ticker, volume)


app = QApplication(sys.argv)
window = Main()
window.show()
app.exec_()