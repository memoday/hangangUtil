from datetime import datetime
from turtle import title
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

wb = Workbook()
ws1 = wb.active

def croll():

    keyword = '한강'
    pg = 0
    ds = "2022.10.12"
    de = "2022.10.12"
    sort = "2" #오래된 순: 2
    pd = "3" #기간검색: 3
    
    maxpg = 1
    
    # ws1.append(["일","언론사","기사제목","업태","미리보기","기사 주소"])
    while pg < maxpg:
        i = 0
        raw = requests.get("https://search.naver.com/search.naver?where=news&query="+keyword+"&sm=tab_opt&sort="+sort+"&photo=0&field=0&pd="+pd+"&ds="+ds+"&de="+de+"&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall&is_sug_officeid=1&start="+str(pg)+"1",
                    headers={'User-Agent':'Mozilla/5.0'})
        html = BeautifulSoup(raw.text, "html.parser")
        articles = html.select("ul.list_news > li")
        try: 
            while i < 10:
                try:
                    checkResult = articles[i].select_one("i.spnew.ico_paper").text
                    checkResult = "신문"
                except AttributeError:
                    checkResult = "인터넷"
                try:
                    checkResult = articles[i].select_one("i.spnew.api_ico_svideo").text
                    checkResult = "방송"
                except AttributeError:
                    None
                title = articles[i].select_one("a.news_tit").text
                source = articles[i].select_one("a.info.press").text
                sum = articles[i].select_one("a.api_txt_lines.dsc_txt_wrap").text
                nlink = articles[i].select_one("a.news_tit")["href"]

                source = source.replace("언론사 선정","")
                print(checkResult)
                print(source)
                print(title)
                print(sum)
                print(nlink)
                print('\n')

                ws1.append([ds,source,title,checkResult,sum,nlink])
                i += 1

            pg = pg +1
            if html.select_one('a.btn_next')["aria-disabled"] == "true":
                print("마지막 페이지입니다.")
            else:
                maxpg = maxpg + 1
                print(maxpg,"번째 페이지입니다.\n")
        except IndexError:
            print("마지막 기사입니다.")
            break
        wb.save(filename='crawlResult.xlsx')
        
croll()