import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
# import pyubit

ui = uic.loadUiType("custom_test.ui")[0]

class Main(QMainWindow, ui):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)

        self.ticker = "KRW-BTC"

        # self.pushButtonPrice.clicked.connect(self.getPrice) #비트코인 가격을 가져와서, textEditPrice에 넣어주기
        # self.pushButtonBuy.clicked.connect() #textEditBuy에 있는 숫자를 가져와서 시장가 매수 API 호출
        # self.pushButtonSell.clicked.connect() #textEditSell에 있는 숫자를 가져와서 시장가 매도 API 호출

        """
        private API        
        """
        access = "Ly89Zxb3mCRaWNCttVGDZUF0YIKYJplPmxMtAbui"
        secret = "DxgBxOxsKUYaOpalM4FTirvVv7xSiMX2kClqOyi1"
        # self.upbit = pyubit.Upbit(access, secret)

    # def getPrice(self):
        """
        비트코인 가격을 가져와서 textEdit에 넣어주기
        :return:
        """
    # def BuyMarketPrice(self):

    # def sellMarketPrice(self):


app = QApplication(sys.argv)
window = Main()