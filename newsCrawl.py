import openpyxl
import requests
from bs4 import BeautifulSoup
from openpyxl import workbook
import datetime

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

def crawl(dateStart):
    setting = {
        "searchKeyword" : '한강', #검색 키워드
        "dateStart" : dateStart, #from date(ds)
        "dateEnd" : dateStart, #to date(de)
        'sort': "2", #오래된 순: 2
        'period': "3" #기간검색: 3  
    }
    
    page = 0
    # ws1.append(["일","언론사","기사제목","업태","미리보기","기사 주소"])
    while True:
        newsURL = "https://search.naver.com/search.naver?where=news&query="+setting['searchKeyword']+"&sm=tab_opt&sort="+setting['sort']+"&photo=0&field=0&pd="+setting['period']+"&ds="+setting['dateStart']+"&de="+setting['dateEnd']+"&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall&is_sug_officeid=1&start="+str(page)+"1"

        raw = requests.get(newsURL, headers={'User-Agent':'Mozilla/5.0'})
        html = BeautifulSoup(raw.text, "html.parser")

        checkNextPage = html.select_one('a.btn_next')["aria-disabled"]
        if checkNextPage == "false":
            print(page+1,"번째 페이지입니다.\n")
        else:
            print(page+1,"번째 마지막 페이지입니다.")

        global articles
        articles = html.select("ul.list_news > li")
        try: 
            for articleIndex in range(10):
                attribute = getAttribute(articleIndex)
                title, source, sum, nlink = getContents(articleIndex)

                data = [setting['dateStart'], source, title, attribute, sum, nlink]
                print(attribute, '\n', source, '\n', title, '\n\n', sum, '\n', nlink, '\n')

                ws1.append(data)
            page += 1

        except IndexError:
            print("마지막 기사입니다.")
            wb.save('crawlResult.xlsx')
            break

def main ():
    print('날짜 기간을 입력해주세요 dateStart')
    dsY,dsM,dsD = map(int,input("시작 년.월.일을 입력해주세요(2022.10.12)").split('.'))
    dateStart = datetime.datetime(dsY,dsM,dsD)
    deY,deM,deD = map(int,input("종료 년.월.일을 입력해주세요(2022.10.12)").split('.'))
    dateEnd = datetime.datetime(deY,deM,deD)

    rawDays = dateEnd - dateStart
    rangeDays = rawDays.days
    print(rangeDays+1)
    i = 0
    for i in range(rangeDays+1):
        urlDays = dateStart+ datetime.timedelta(days= i)
        urlDays = str(urlDays.strftime('%Y.%m.%d'))
        crawl(urlDays)
        i += 1


if __name__ == "__main__":
    try:
        wb = openpyxl.load_workbook('crawlResult.xlsx')
    except FileNotFoundError:
        wb = openpyxl.Workbook()
    ws1 = wb.active
    main()