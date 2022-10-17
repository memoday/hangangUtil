from turtle import title
import requests
from bs4 import BeautifulSoup

keyword = '한강'
raw = requests.get("https://search.naver.com/search.naver?where=news&query="+keyword+"&sm=tab_opt&sort=1&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall&is_sug_officeid=0",
                   headers={'User-Agent':'Mozilla/5.0'})
html = BeautifulSoup(raw.text, "html.parser")
articles = html.select("ul.list_news > li")

def croll():
    i = 0
    r = 1
    while i < 10:
        title = articles[i].select_one("a.news_tit").text
        source = articles[i].select_one("a.info.press").text
        sum = articles[i].select_one("a.api_txt_lines.dsc_txt_wrap").text
        nlink = articles[i].select_one("a.info")["href"]
        if r < 10:
            while r < 10:
                if (title == (articles[r].select_one("a.news_tit").text)) :
                    print('')
                    print('중복된 뉴스입니다.')
                    print('')
                    r = r + 1
                    i = i + 1
                    break
                else:
                    print(source+': '+title)
                    print(sum)
                    print(nlink)
                    print('')
                    r = r + 1
                    i = i + 1
                    break
        else:
            print(source+': '+title)
            print(sum)
            print(nlink)
            break

croll()