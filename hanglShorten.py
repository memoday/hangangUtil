import requests
import json

headers = {
    'Authorization': 'Bearer 06e325d393d2807edd1bcb9aa229ce28',
    'Content-Type': 'application/json',
}

def hanglShorten(longUrl):  
    data = '{"url": "'+longUrl+'"}'
    response = requests.post('https://han.gl/api/url/add', headers=headers, data=data,timeout=5)
    if response.status_code == 200:
        if "han.gl" in longUrl: #이미 단축되어있는 링크라면 단축하지 않음
            return longUrl
        else:
            jsonObject = json.loads(response.text)
            print('\n===링크 단축 성공===')
            shortUrl = jsonObject.get("shorturl")
            print(shortUrl)
            return shortUrl
    if response.status_code == 403:
        print('Error Code: 403')