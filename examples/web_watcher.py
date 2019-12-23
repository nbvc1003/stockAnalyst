from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from bs4 import BeautifulSoup as bs
import urllib.request as req, sys, time
from examples.web_watcherUI import Ui_MainWindow

# QT코어 QMainWindow와 QT 디자이너 에서 생성된 Ui_MainWindow 를 상속 받는다.
class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # Ui_MainWindow 의 초기화 매소드
        self.timer = QTimer()
        # connect 함수를 사용하여 주기적으로 실행할 check 함수에 연결해줌
        self.timer.timeout.connect(self.check)
        self.timer.setInterval(5 * 60 * 1000)
        self.rb_5m.setChecked(True) # UI초기 설정
        self.show()

    def setCycle(self):
        if self.rb_10m.isChecked():
            # self.rb_10m.setChecked()
            self.timer.setInterval(10*60*1000)
        elif self.rb_5m.isChecked():
            self.timer.setInterval(5 * 60 * 1000)
        elif self.rb_1m.isChecked():
            print('clecked')
            self.timer.setInterval(1*60*1000)
        elif self.rb_30s.isChecked():
            self.timer.setInterval(0.5*60 * 1000)
        elif self.rb_5s.isChecked():
            print('clecke')
            self.timer.setInterval(5 * 1000)
        else:
            self.timer.setInterval(1000)

    def startChk(self):
        self.url.setEnabled(False)
        self.timer.start()

    def stopChk(self):
        self.url.setEnabled(True)
        self.timer.stop()

    def check(self):
        # print('인터벌 :' , self.timer.interval())
        self.rsp = req.urlopen(self.url.text())
        self.html = bs(self.rsp, 'html.parser')
        try:
            self.test = self.html.find(alt="UP").attrs['alt']
        except:
            self.test = "XX"

        self.t = time.localtime()
        self.lbl_print.setText("인터벌:{}, {}:{}:{} 채크결과: {}"
                               .format(self.timer.interval(), self.t.tm_hour, self.t.tm_min,self.t.tm_sec, self.test))


app = QApplication([]) # 실행할때 외부에서 인자를 받을때 []로 받는다.
ex = Example() # 메인 객체 생성..
# 프로그램 종료 ( 종료 조건)
sys.exit(app.exec_())
# app.exec_() 메인루프를 실행한다. 프로그램을 종료시켜서 끝날때 자동으로 밖에 있는  exit가 실행된다.
