import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pyperclip
from PyQt5.QtGui import *
import hanglShorten as hgs
import os
import checkNews as cn
import webbrowser

__version__ = 'v1.3.1'

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    
icon = resource_path('assets/HGM.ico')
form = resource_path('ui/HGA.ui')

form_class = uic.loadUiType(form)[0]
print("프로그램이 구동됩니다.")

class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #프로그램 기본설정
        self.setWindowIcon(QIcon(icon))
        self.setWindowTitle('HGA '+__version__)
        self.statusBar().showMessage('프로그램 정상 구동 중')

        #버튼에 기능을 연결하는 코드
        self.btn_ok.clicked.connect(self.runCrawl)
        self.input_link.returnPressed.connect(self.runCrawl)
        self.btn_exit.clicked.connect(self.exit)
        self.autoStart.toggle()
        # self.btn_shortenUrl.clicked.connect(self.shortenUrl)

        self.btn_copyOutput2.clicked.connect(self.copyOutput2)
        self.btn_copyPress.clicked.connect(self.copyPress)
        self.btn_copyOutput.clicked.connect(self.copyOutput)
        self.btn_url.clicked.connect(self.openURL)
        self.btn_copyDate.clicked.connect(self.copyDate)
        self.btn_paste.clicked.connect(self.paste)
        
        #기타
        self.input_link.setFocus() #프로그램 실행시 input_link 자동 선택

    def closeEvent(self, event):
        hgs.exit()
        os.system("taskkill /f /im chromedriver.exe") #chomrdriver.exe 강제종료
        sys.exit(0)

    def exit(self) :
        hgs.exit()
        os.system("taskkill /f /im chromedriver.exe") #chomrdriver.exe 강제종료
        sys.exit(0)
    
    def shortenUrl(self) :
        url = self.input_link.text()
        self.output.setText('')
        self.output_2.setText(hgs.hanglShorten(url))
        self.statusBar().showMessage('링크 단축 성공')
    
    def paste(self):
        copied = pyperclip.paste()
        if 'http' in copied:
            self.input_link.setText(copied)
            if self.autoStart.isChecked() == True:
                self.runCrawl()

    def runCrawl(self):
        global output, press, date
        if self.input_link.text() != "":
            try:
                url_ = self.input_link.text().replace(" ","")
                self.input_link.setText(url_)
                url = self.input_link.text()
                
                title, press, content, date = cn.checkNews(url)
                self.statusBar().showMessage('인식된 언론사: '+press)

                print(title+"\n"+press+" "+date+"\n"+content)
                output = title+"\n"+press+" "+date+"\n"+content
                output_2 = title+"\n"+hgs.hanglShorten(url) #단축된 링크로 제공

                self.output.setText(output)
                self.output_2.setText(output_2)
                print(self.output.toPlainText())
                
            except AttributeError:
                print(AttributeError)
                self.output.setText("호환하지 않는 링크입니다.")
                self.statusBar().showMessage('호환하지 않는 링크입니다.')
            except Exception :
                output_2 = hgs.hanglShorten(url)
                self.output_2.setText(output_2)
                # self.statusBar().showMessage('Exception Error')
        else:
            self.output.setText('링크를 입력해주세요')

    def copyOutput(self):
        content = self.output.toPlainText()
        pyperclip.copy(content)

    def copyOutput2(self):
        content = self.output_2.toPlainText()
        pyperclip.copy(content)

    def copyPress(self):
        try:
            pyperclip.copy(press)
        except NameError:
            self.output.setText('복사할 내용이 없습니다.')

    def openURL(self):
        inputURL = self.input_link.text()

        if inputURL != '':
            print('inputURL')
            webbrowser.open_new_tab(inputURL)

    def copyDate(self):
        try:
            date_ = date[0:10]
            pyperclip.copy(date_)
        except NameError:
            self.output.setText('복사할 내용이 없습니다.')

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()
    