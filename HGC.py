from time import strftime
import openpyxl
import requests
from bs4 import BeautifulSoup
import datetime
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os, sys

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('ui/HGC.ui')
icon = resource_path('assets/HGM.ico')

form_class = uic.loadUiType(form)[0]
print('프로그램이 구동됩니다.')

now = datetime.datetime.now()
today = (now.date()).strftime('%Y.%m.%d')
ty, tm ,td = (map(int,today.split('.')))

def getRange(ds,de):

    dsY,dsM,dsD = map(int,ds.split('.'))
    dateStart = datetime.datetime(dsY,dsM,dsD)

    deY,deM,deD = map(int,de.split('.'))
    dateEnd = datetime.datetime(deY,deM,deD) 
    #dateStart와 dateEnd의 차를 구하기 위해 datetime type으로 바꾸는 작업

    rawDays = dateEnd - dateStart
    rangeDays = rawDays.days
    return rangeDays

def getAttribute(articleIndex):
    if (articles[articleIndex].select_one("div.info_group > span:nth-child(2) > i.spnew.ico_paper")):
        return "신문"
    elif not(str(articles[articleIndex]).find("api_ico_svideo") == -1): #svideo는 select_one태그로 찾아지지 않음
        return "방송"
    else:
        return "인터넷"

def getContents(articleIndex) -> tuple:
    title = articles[articleIndex].select_one("a.news_tit").text
    source = articles[articleIndex].select_one("a.info.press").text.replace("언론사 선정","") #언론사 PICK태그에 #text '언론사 선정' 제거
    sum = articles[articleIndex].select_one("a.api_txt_lines.dsc_txt_wrap").text
    nlink = articles[articleIndex].select_one("a.news_tit")["href"]

    return title, source, sum, nlink

def fileCreate(searchKeyword, sort,fileNameDays,self):

    global wb, ws1, fileName

    if sort == '0':
        fileNameSort = "관련도순"
    elif sort == '1':
        fileNameSort = "최신순"
    elif sort == '2':
        fileNameSort =  "오래된순"

    fileName = searchKeyword+'_'+fileNameDays+'_'+fileNameSort+'.xlsx'

    try:
        wb = openpyxl.load_workbook(fileName)
        return 'exists'
    except FileNotFoundError:
        print('FileNotFound: 엑셀 파일을 새로 생성합니다.')
        wb = openpyxl.Workbook()            
    ws1 = wb.active

def crawl(searchKeyword, dateStart, sort, self):

    setting = {
        "searchKeyword" : searchKeyword, #검색 키워드
        "dateStart" : dateStart, #from date(ds)
        "dateEnd" : dateStart, #to date(de), 날짜 정보를 받아오지 못해 일자별로 crawl()작업을 수행함
        'sort': sort, #오래된 순: 2 #최신 순: 1 #관련도 순: 0
        'period': "3" #사용자 설정 기간검색: 3  
        #전체: 0, 1시간~6시간: 7~12, 1일: 4, 1주: 1, 1개월: 2, 3개월: 13, 6개월: 6, 1년: 5
    }
    
    page = 0
    # ws1.append(["일","언론사","기사제목","업태","미리보기","기사 주소"])
    
    while True:
        newsURL = "https://search.naver.com/search.naver?where=news&query="+setting['searchKeyword']+"&sm=tab_opt&sort="+setting['sort']+"&photo=0&field=0&pd="+setting['period']+"&ds="+setting['dateStart']+"&de="+setting['dateEnd']+"&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall&is_sug_officeid=1&start="+str(page)+"1"

        raw = requests.get(newsURL, headers={'User-Agent':'Mozilla/5.0'})
        html = BeautifulSoup(raw.text, "html.parser")

        try:
            checkNextPage = html.select_one('a.btn_next')["aria-disabled"]
        except TypeError:
            print('관련 기사가 존재하지 않습니다')
            self.label_main.setText("Not Found")
            self.label_main.setStyleSheet("Color: Red")
            break

        global articles
        articles = html.select("ul.list_news > li")
        try: 
            for articleIndex in range(10):
                attribute = getAttribute(articleIndex)
                title, source, sum, nlink = getContents(articleIndex)

                data = [setting['dateStart'], source, title, attribute, sum, nlink]
                # print(attribute, '\n', source, '\n', title, '\n\n', sum, '\n', nlink, '\n')

                ws1.append(data)

            if checkNextPage == "true":
                print('다음 페이지가 없어 크롤링을 종료합니다.') #다음 페이지가 존재하지 않을 때
                wb.save(fileName)
                break
            else:
                print(page+1,"번째 페이지입니다.")
                self.statusBar().showMessage(data[2])

            page += 1

        except IndexError:
            print("다음 기사가 없어 크롤링을 종료합니다.") #해당 페이지 마지막 기사일 때
            wb.save(fileName)
            break

class Thread1(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    
    def run(self):
        self.parent.btn_start.setDisabled(True)
        self.parent.statusBar().showMessage('프로그램 정상 구동 중')
        self.parent.label_main.setText("Crawling..")
        self.parent.label_main.setStyleSheet("Color: Black")

        searchKeyword = self.parent.input_keyword.text()

        if self.parent.dateStart.date() > self.parent.dateEnd.date():
            print('입력된 날짜를 다시 확인 해주세요.')
            self.parent.btn_start.setEnabled(True)
            self.parent.statusBar().showMessage('프로그램 정상 구동 중')
            self.parent.label_main.setText("Date Error")
            self.parent.label_main.setStyleSheet("Color: Red")
            return
        if searchKeyword is '':
            print('검색어를 입력해주세요')
        else:
            dateStart = self.parent.dateStart.date().toString('yyyy.MM.dd')
            dateEnd = self.parent.dateEnd.date().toString('yyyy.MM.dd')

            rangeDays = getRange(dateStart,dateEnd)

            fileNameDays = dateStart+'~'+dateEnd #파일명에 들어갈 날짜

            dsY,dsM,dsD = map(int,dateStart.split('.'))
            dateStart = datetime.datetime(dsY,dsM,dsD) 
            #dateStart를 str에서 datetime으로 type 변경, 날짜 계산하기 위한 과정

            sort = str(self.parent.combo_sort.currentIndex()) #combo box안에 있는 값 전달

            fileCreate(searchKeyword,sort,fileNameDays,self.parent)
            file = fileCreate(searchKeyword,sort,fileNameDays,self.parent)

            if file == 'exists':
                self.parent.label_main.setStyleSheet("Color: Red")
                self.parent.label_main.setText("File Exists")
                self.parent.btn_start.setEnabled(True)
                self.parent.statusBar().showMessage('프로그램 정상 구동 중')
                return

            i = 0

            for i in range(rangeDays+1):
                #기간 검색시 최근 기사의 작성날짜 정보를 불러오지 못해 rangeDays만큼 crawl()를 반복시킴
                urlDays = dateStart+ datetime.timedelta(days= i)
                urlDays = str(urlDays.strftime('%Y.%m.%d'))
                crawl(searchKeyword, urlDays, sort, self.parent)
                i += 1


        self.parent.btn_start.setEnabled(True)
        self.parent.statusBar().showMessage('프로그램 정상 구동 중')
        if self.parent.label_main.text() != "Not Found":
            self.parent.label_main.setText("Success")
            self.parent.label_main.setStyleSheet("Color: Green")

    def end(self):
        self.quit()
        self.sleep(1)


class WindowClass(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #프로그램 기본설정
        self.setWindowIcon(QIcon(icon))
        self.setWindowTitle('HGC')
        self.statusBar().showMessage('프로그램 정상 구동 중')

        #실행 후 기본값 설정
        yesterdayDate = QDate(ty,tm,td-1)
        todayDate = QDate(ty,tm,td)
        self.dateStart.setDate(yesterdayDate)
        self.dateEnd.setDate(todayDate)

        #버튼 기능
        self.btn_start.clicked.connect(self.main)
        self.input_keyword.returnPressed.connect(self.main)
        self.btn_exit.clicked.connect(self.exit)

    def main(self):
        x = Thread1(self)
        x.start()
        x.end()

    def exit(self):
        sys.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()