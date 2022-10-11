from xml.dom.minidom import Document
import requests
from bs4 import BeautifulSoup
import pyperclip
import re

print("네이버 뉴스 주소를 입력해주세요:")
url = "https://n.news.naver.com/mnews/article/031/0000701931?sid=101"
web = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
source = BeautifulSoup(web.text,'html.parser')

def sort():
    global output
    title = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2").text
    press = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_top > a > img.media_end_head_top_logo_img.light_type")['alt']
    content = source.select_one("#dic_area")
    date = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span").text
    contentStr = str(content).replace('<br/>','\n') #<br>태그 Enter키로 변경
    to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
    contentOut = re.sub(to_clean,'',contentStr) #html태그 모두 지우기

    print(title+"\n"+press+" "+date+"\n"+contentOut)
    output = title+"\n"+press+" "+date+"\n"+contentOut


if __name__ == "__main__":
    sort()
    pyperclip.copy(output)
    