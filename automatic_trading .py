import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

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
        elif self.radioButton3.isCheck():
            interval = "minute3"
        elif self.radioButton5.isCheck():
            interval = "minute5"
        elif self.radioButton15.isCheck():
            interval = "minute15"
        elif self.radioButton30.isCheck():
            interval = "minute30"
        elif self.radioButton60.isCheck():
            interval = "minute60"
        elif self.radioButton240.isCheck():
            interval = "minute240"
        elif self.radioButtonDay.isCheck():
            interval = "minuteDay"
        # 아무것도 체크하지 않았을 경우
        if not interval:
            return False

        return interval

    def popup(self, message):
        QMessageBox.information(self, "알림",message)



    class Bot():
        def __init__(self):
            self.isRunning = False


app = QApplication(sys.argv)
window = Main()
window.show()
app.exec_()