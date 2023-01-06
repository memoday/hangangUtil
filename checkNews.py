import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urlparse
import html

def get_real_url_from_shortlink(url): #단축링크 원본링크로 변경
    resp = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    print('Original URL:'+resp.url)
    return resp.url

def checkNews(url) -> tuple : #언론사별 selector

    domain = urlparse(url).netloc #도메인 이름 가져옴 ex) https://www.example.com/ex/123 -> www.example.com

    url = get_real_url_from_shortlink(url)
    web = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    if web.encoding != 'UTF-8':
        web.encoding=None
    source = BeautifulSoup(web.text,'html.parser')

    if "n.news.naver" in url: #네이버뉴스
        print('n.news.naver checked')
        title = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2").text
        press = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_top > a > img.media_end_head_top_logo_img.light_type")['alt']
        content = source.select_one("#dic_area")
        date = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span").text
        contentStr = str(content).replace('<br/>','\n') #<br>태그 Enter키로 변경
        contentStr = str(contentStr).replace('</table>','\n') #이미지 부연설명 내용과 분리
        contentStr = contentStr.replace('</img>','') #이미지 위치 확인
        to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
        contentEdited = re.sub(to_clean,'',contentStr) #html태그 모두 지우기

    elif "sports.news.naver" in url: #네이버 스포츠뉴스
        print('sports.news.naver checked')
        title = source.select_one("#content > div > div.content > div > div.news_headline > h4").text
        press = source.select_one("#pressLogo > a > img")['alt']
        content = source.select_one("#newsEndContents")

        content.find(class_ = 'source').decompose()
        content.find(class_ = 'byline').decompose()
        content.find(class_ = 'reporter_area').decompose()
        content.find(class_ = 'copyright').decompose()
        content.find(class_ = 'categorize').decompose()
        content.find(class_ = 'promotion').decompose()

        date = source.select_one("#content > div > div.content > div > div.news_headline > div > span:nth-child(1)").text
        date = date.replace('기사입력 ','')
        
        contentStr = str(content).replace('<br/>','\n') #<br>태그 Enter키로 변경
        contentStr = str(contentStr).replace('</table>','\n') #이미지 부연설명 내용과 분리
        contentStr = contentStr.replace('</img>','') #이미지 위치 확인
        to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
        contentEdited = re.sub(to_clean,'',contentStr) #html태그 모두 지우기
    
    elif "entertain.naver.com" in url:
        print('entertain.naver checked')
        title = source.find('meta',property='og:title')['content']
        press = source.select_one("#content > div.end_ct > div > div.press_logo > a > img")['alt']
        content = source.select_one("#articeBody")
        date = source.select_one('#content > div.end_ct > div > div.article_info > span > em').text

        contentStr = str(content).replace('<br/>','\n') #<br>태그 Enter키로 변경
        contentStr = str(contentStr).replace('</table>','\n') #이미지 부연설명 내용과 분리
        contentStr = contentStr.replace('</img>','') #이미지 위치 확인
        to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
        contentEdited = re.sub(to_clean,'',contentStr) #html태그 모두 지우기

    # elif "newspim.com" in url: #뉴스핌
    #     print('newspim.com checked')
    #     title = source.select_one("#main-title").text
    #     press = "뉴스핌"
    #     content = source.select_one("#wrap > div.container.subwrap > div > div:nth-child(2) > div.left > div > div.contents")
    #     date = source.select_one("#send-time").text
    #     date = date.replace("년",".").replace("월",".").replace("일","")
    #     contentStr = str(content).replace('<br/>','\n') #<br>태그 Enter키로 변경
    #     contentStr = str(contentStr).replace('</table>','\n') #이미지 부연설명 내용과 분리
    #     contentStr = contentStr.replace('</img>','[사진]\n') #이미지 위치 확인
    #     to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
    #     contentEdited = re.sub(to_clean,'',contentStr) #html태그 모두 지우기
        
        
    else:
        print("호환되지 않는 링크로 meta값을 탐색합니다.")

        try:
            title = source.find('meta',property='og:title')['content']
        except:
            title = ''
            print('title meta값을 찾을 수 없습니다')

        pressSetting = { #press meta값이 없을 때 수동으로 언론사 이름을 제공해줌
            'www.sisa-news.com' : '시사뉴스',
            'www.ilyosisa.co.kr' : '일요시사',
            'www.skyedaily.com' : '스카이데일리',
            'skyedaily.com' : '스카이데일리',
            'idsn.co.kr' : '매일안전신문',
            'www.siminilbo.co.kr' : '시민일보',
        } 

        try:
            press = source.find('meta',property='og:site_name')['content']

            if '세상을 깨우는 재미진 목소리' in press: #언론사 이름에 이름 외 정보도 같이 포함되는 경우
                press = '위키트리'
            elif '100세시대의 동반자' in press:
                press = '브릿지경제'
            elif '(DISCOVERYNEWS)' in press:
                press = '디스커버리뉴스'
            elif '인천의 든든한 친구' in press:
                press = '중부일보'
            elif 'NSP뉴스통신사' in press:
                press = 'NSP통신'
            elif 'NSP뉴스통신사' in press:
                press = 'NSP통신'
            elif '종합일간지 : 신문/웹/모바일 등 멀티 채널로 국내외 실시간 뉴스와 수준 높은 정보를 제공' in press:
                press = '아시아투데이'
            elif '아침을 여는 신문' in press:
                press = '기호일보'
            elif '글로벌 뉴스 미디어 채널 데일리포스트' in press:
                press = '데일리포스트'
            elif 'www.donga.com' in press:
                press = '동아일보'
            elif 'tborad' in press:
                press = 'SK브로드밴드'
            elif ' OBS경인TV' in press:
                press = 'OBS'
            elif 'HARPERSBAZAAR' in press:
                press = '하퍼스바자'
            elif 'mbnmoney.mbn.co.kr' in press:
                press = '매일경제TV'
            elif '전국매일신문' in press:
                press = '전국매일신문'
            elif 'Queen' in press:
                press = 'Queen'
            elif '푸드경제신문'  in press:
                press = '푸드경제신문'
            elif 'ktv.go.kr' in press:
                press = 'KTV국민방송'


        except: #meta값을 찾지 못했을 때 pressSetting 딕셔너리를 통해 언론사 이름을 불러옴
            if domain in pressSetting:
                print('도메인 주소: '+domain)
                press = pressSetting[domain]
            else:
                print(domain)
                press = ''
                print('site_name meta값을 찾을 수 없습니다')

        contentEdited = ''

        try:
            metaDate = source.find('meta',property='article:published_time')['content']
            rawDate = metaDate[0:10]
            rawDate = datetime.strptime(rawDate,'%Y-%m-%d')
            finalDate = str(datetime.strftime(rawDate,'%Y.%m.%d.'))

            time = metaDate[11:16]
            time = datetime.strptime(time,'%H:%M')
            time = str(time.strftime("%p %I:%M"))
            print(time)
            finalTime = time.replace('AM','오전').replace('PM','오후')   

            date = (finalDate+' '+finalTime)

        except:
            date = ''
            print('published_time meta값을 찾을 수 없습니다')

    contentEdited = html.unescape(contentEdited) #&lt;(<) &gt;(>) 정상적으로 다시 변환시킴

    return title,press,contentEdited,date