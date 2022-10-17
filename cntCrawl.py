import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from numpy import imag
import requests
from bs4 import BeautifulSoup
import pyperclip
import re
from PyQt5.QtGui import *


form_class = uic.loadUiType("main.ui")[0]
print("프로그램이 구동됩니다.")

def get_real_url_from_shortlink(url): #단축링크 원본링크로 변경
    resp = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    print(resp.url)
    return resp.url

def checkNews(url) -> tuple : #언론사별 selector

    url = get_real_url_from_shortlink(url)
    web = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    source = BeautifulSoup(web.text,'html.parser')

    if "n.news.naver" in url: #네이버뉴스
        print('n.news.naver checked')
        title = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2").text
        press = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_top > a > img.media_end_head_top_logo_img.light_type")['alt']
        content = source.select_one("#dic_area")
        date = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span").text

    if "sports.news.naver" in url: #네이버 스포츠뉴스
        print('sports.news.naver checked')
        title = source.select_one("#content > div > div.content > div > div.news_headline > h4").text
        press = source.select_one("#pressLogo > a > img")['alt']
        content = source.select_one("#newsEndContents")
        date = source.select_one("#content > div > div.content > div > div.news_headline > div > span:nth-child(1)").text

    else:
        print("호환되지 않는 언론사입니다")
    return title,press,content,date

class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #버튼에 기능을 연결하는 코드
        self.setWindowIcon(QIcon('HGM.ico'))
        self.btn_ok.clicked.connect(self.naverSort)
        self.btn_reset.clicked.connect(self.reset)
        self.input_link.returnPressed.connect(self.naverSort)
        self.btn_copy.clicked.connect(self.copy)

    def reset(self) :
        self.input_link.setText("")
        self.output.setText("")

    def naverSort(self):
        global output
        try:
            url = self.input_link.text()
            
            title, press, content, date = checkNews(url)

            contentStr = str(content).replace('<br/>','\n') #<br>태그 Enter키로 변경
            contentStr = str(contentStr).replace('</table>','\n') #이미지 부연설명 내용과 분리
            contentStr = contentStr.replace('</img>','[사진]\n') #이미지 위치 확인
            to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
            contentOut = re.sub(to_clean,'',contentStr) #html태그 모두 지우기

            print(title+"\n"+press+" "+date+"\n"+contentOut)
            output = title+"\n"+press+" "+date+"\n"+contentOut

            self.output.setText(output)
            print(self.output.toPlainText())
        except AttributeError:
            print("내용을 찾을 수 없습니다. 네이버 뉴스 기사가 맞는지 다시 확인해주세요.")
            self.output.setText("내용을 찾을 수 없습니다. 네이버 뉴스 기사가 맞는지 다시 확인해주세요.")
        except Exception :
            print("알 수 없는 이유로 실패했습니다")
            self.output.setText("알 수 없는 이유로 실패했습니다")

    def copy(self):
        content = self.output.toPlainText()
        pyperclip.copy(content)

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()
    