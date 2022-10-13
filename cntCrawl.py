import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import requests
from bs4 import BeautifulSoup
import pyperclip
import re

form_class = uic.loadUiType("main.ui")[0]
print("프로그램이 구동됩니다.")


class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #버튼에 기능을 연결하는 코드
        self.btn_ok.clicked.connect(self.naverSort)
        self.btn_reset.clicked.connect(self.reset)
        self.input_link.returnPressed.connect(self.naverSort)
        self.btn_copy.clicked.connect(self.copy)

    def reset(self) :
        self.input_link.setText("")

    def naverSort(self):
        global output
        
        url = self.input_link.text()
        web = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
        source = BeautifulSoup(web.text,'html.parser')
        
        title = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2").text
        press = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_top > a > img.media_end_head_top_logo_img.light_type")['alt']
        content = source.select_one("#dic_area")
        date = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span").text
        contentStr = str(content).replace('<br/>','\n') #<br>태그 Enter키로 변경
        contentStr = str(contentStr).replace('</table>','\n') #이미지 부연설명 내용과 분리
        contentStr = contentStr.replace('</img>','[사진]\n') #이미지 위치 확인
        to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
        contentOut = re.sub(to_clean,'',contentStr) #html태그 모두 지우기

        print(title+"\n"+press+" "+date+"\n"+contentOut)
        output = title+"\n"+press+" "+date+"\n"+contentOut

        self.output.setText(output)
        print(self.output.toPlainText())

    def copy(self):
        content = self.output.toPlainText()
        pyperclip.copy(content)

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()
    