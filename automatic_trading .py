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

app = QApplication(sys.argv)
window = Main()
window.show()
app.exec_()