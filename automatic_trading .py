import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pyupbit
from apscheduler.schedulers.background import BackgroundScheduler

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

        #TODO 봇 실행 메서드 호출하기, interval 값 넘기기
        isValidStart = self.bot.firstSetting(interval)

        if not isValidStart:
            return self.popup("유효한 API키가 아닙니다.")


    def stopBot(self):
        """
        봇 종료 메서드

        1. 봇이 실행중인지 검사
        2. 봇 종료
        :return:
        """
        if not self.bot.isRunning:
            return self.popup("실행 상태가 아닙니다.")

        #TODO 봇 종료 메서드 호출
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



    class Bot():
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
            self.seheduler = BackgroundScheduler()

            if self.interval == "minute1":
                self.seheduler.add_job(self.updatePriceInfo, 'cron', minute="*", second="2", id="job")
            if self.interval == "minute3":
                self.seheduler.add_job(self.updatePriceInfo, 'cron', minute="*/3", second="2", id="job")
            if self.interval == "minute5":
                self.seheduler.add_job(self.updatePriceInfo, 'cron', minute="*/5", second="2", id="job")
            if self.interval == "minute10":
                self.seheduler.add_job(self.updatePriceInfo, 'cron', minute="*/10", second="2", id="job")
            if self.interval == "minute15":
                self.seheduler.add_job(self.updatePriceInfo, 'cron', minute="*/15", second="2", id="job")
            if self.interval == "minute30":
                self.seheduler.add_job(self.updatePriceInfo, 'cron', minute="*/30", second="2", id="job")
            if self.interval == "minute60":
                self.seheduler.add_job(self.updatePriceInfo, 'cron', hour="*", second="2", id="job")
            if self.interval == "minute240":
                self.seheduler.add_job(self.updatePriceInfo, 'cron', hour="1-23/4", second="2", id="job")
            if self.interval == "day":
                self.seheduler.add_job(self.updatePriceInfo, 'cron', day="*", hour="0", minute="0", second="2", id="job")

            self.seheduler.start()

            #2. 필요한 데이터 요청하고 게산하기 ( 상단 밴드, 중간 밴드, 매도 가격 ) -> 스케줄러 사용
            data = pyupbit.get_ohlcv(self.ticker, interval=self.interval)

            period = 20
            multiplier = 2

            data['middle'] = data['close'].rolling(period).mean() #중간밴드
            data['upper'] = data['close'].rolling(period).mean() + data['close'].rolling(period).std() * multiplier #상단 밴드

            self.middle = data.iloc[-2]['middle'] #이전봉 중간밴드 값
            self.upper = data.iloc[-2]['uppaer'] #이전 봉 상단밴드 값
            self.prevHighPrice = data.iloc[2]['high'] #이전봉 증가

            return True

    def updatePriceInfo(self):
        data = pyupbit.get_ohlcv(self.ticker, interval=self.interval)


app = QApplication(sys.argv)
window = Main()
window.show()
app.exec_()