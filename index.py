import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

app = QApplication(sys.argv)
window = Main()
window.show()
app.exec_()