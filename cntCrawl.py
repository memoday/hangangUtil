import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import requests
from bs4 import BeautifulSoup
import pyperclip
import re
from PyQt5.QtGui import *
import hanglShorten as hgs
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    
icon = resource_path('HGM.ico')
form = resource_path('main.ui')

form_class = uic.loadUiType(form)[0]
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

    if "newspim.com" in url: #뉴스핌
        print('newspim checked')
        title = source.select_one("#main-title").text
        press = "뉴스핌"
        content = source.select_one("#wrap > div.container.subwrap > div > div:nth-child(2) > div.left > div > div.contents")
        date = source.select_one("#send-time").text
        date = date.replace("년",".").replace("월",".").replace("일","")

    else:
        print("호환되지 않는 언론사입니다")
    return title,press,content,date

class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.statusBar().showMessage('프로그램 정상 구동 중')

        #버튼에 기능을 연결하는 코드
        self.setWindowIcon(QIcon(icon))
        self.setWindowTitle('HGA')
        self.btn_ok.clicked.connect(self.runCrawl)
        self.input_link.returnPressed.connect(self.runCrawl)
        self.btn_exit.clicked.connect(self.exit)
        self.input_link.setFocus() #프로그램 실행시 input_link 자동 선택
        self.btn_shortenUrl.clicked.connect(self.shortenUrl)

    def exit(self) :
        sys.exit(0)
    
    def shortenUrl(self) :
        url = self.input_link.text()
        self.output_2.setText(hgs.hanglShorten(url))

    def runCrawl(self):
        global output
        try:
            url = self.input_link.text()
            
            title, press, content, date = checkNews(url)

            contentStr = str(content).replace('<br/>','\n') #<br>태그 Enter키로 변경
            contentStr = str(contentStr).replace('</table>','\n') #이미지 부연설명 내용과 분리
            contentStr = contentStr.replace('</img>','[사진]\n') #이미지 위치 확인
            to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
            contentOut = re.sub(to_clean,'',contentStr) #html태그 모두 지우기

            self.statusBar().showMessage('로딩 중') #작동 안함
            print(title+"\n"+press+" "+date+"\n"+contentOut)
            output = title+"\n"+press+" "+date+"\n"+contentOut
            output_2 = title+"\n"+hgs.hanglShorten(url) #단축된 링크로 제공

            self.output.setText(output)
            self.output_2.setText(output_2)
            self.output_3.setText(press)
            self.statusBar().showMessage('인식된 언론사: '+press)
            print(self.output.toPlainText())
            
        except AttributeError:
            self.output.setText("호환되지 않는 링크입니다.")
            self.statusBar().showMessage('호환되지 않는 링크입니다.')
        except Exception :
            self.output.setText("알 수 없는 이유로 실패했습니다")
            self.statusBar().showMessage('Exception Error')

    def copy(self):
        content = self.output.toPlainText()
        pyperclip.copy(content)

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()
    