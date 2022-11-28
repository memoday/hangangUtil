import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def get_real_url_from_shortlink(url): #단축링크 원본링크로 변경
    resp = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    print('Original URL:'+resp.url)
    return resp.url

def checkNews(url) -> tuple : #언론사별 selector

    url = get_real_url_from_shortlink(url)
    web = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    if web.encoding == 'ISO-8859-1':
        web.encoding='UTF-8'
    source = BeautifulSoup(web.text,'html.parser')

    if "n.news.naver" in url: #네이버뉴스
        print('n.news.naver checked')
        title = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2").text
        press = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_top > a > img.media_end_head_top_logo_img.light_type")['alt']
        content = source.select_one("#dic_area")
        date = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span").text
        contentStr = str(content).replace('<br/>','\n') #<br>태그 Enter키로 변경
        contentStr = str(contentStr).replace('</table>','\n') #이미지 부연설명 내용과 분리
        contentStr = contentStr.replace('</img>','[사진]') #이미지 위치 확인
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
        contentStr = contentStr.replace('</img>','[사진]\n') #이미지 위치 확인
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
        contentStr = contentStr.replace('</img>','[사진]') #이미지 위치 확인
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
    
    
    # elif "hg-times.com" in url: #한강타임즈
    #     print('hg-times.com checked')
    #     title = source.select_one('#user-container > div.float-center.max-width-1100 > header > header > div').text
    #     press ='한강타임즈'
    #     content = source.select_one('div.articleBody').text

    #     try:
    #         content.find(type = 'text/javascript').decompose()
    #         content.find(class_ = 'tag-group').decompose()
    #         content.find(class_ = 'article-body-dn-txt auto-marbtm-50 no-bullet').decompose()
    #         content.find(class_ = 'view-copyright').decompose()
    #         content.find('style').decompose()
    #         content.find(class_ = 'hw-box').decompose()
    #         content.find(class_ = 'emoji-tit').decompose()
    #         content.find(id = 'emoji-for').decompose()
    #         content.find(class_ = 'editor-profile').decompose()
    #         content.find(class_ ='clearfix user-sns-send').decompose()
    #         content.find(class_ ='clearfix  ').decompose()
    #         content.find(class_ ='clearfix user-sns-send').decompose()
    #     except AttributeError:
    #         pass

    #     date = source.select_one("#user-container > div.float-center.max-width-1100 > header > section > div.info-text > ul > li:nth-child(2)").text
    #     contentStr = str(content).replace('<br/>','\n') #<br>태그 Enter키로 변경
    #     contentStr = contentStr.replace('</img>','[사진]\n') #이미지 위치 확인
    #     to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
    #     contentEdited = re.sub(to_clean,'',contentStr) #html태그 모두 지우기
        
        
    else:
        print("호환되지 않는 언론사로 meta값을 탐색합니다.")

        try:
            title = source.find('meta',property='og:title')['content']
        except:
            title = ''
            print('title meta값을 찾을 수 없습니다')

        try:
            press = source.find('meta',property='og:site_name')['content']

            if '세상을 깨우는 재미진 목소리' in press:
                press = '위키트리'
            elif '100세시대의 동반자' in press:
                press = '브릿지경제'
            
        except:
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
    
    return title,press,contentEdited,date