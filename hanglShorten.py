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
        jsonObject = json.loads(response.text)
        print('링크 단축 성공')
        print(jsonObject.get("shorturl"))
    if response.status_code == 403:
        print('Error Code: 403')
    else:
        print('Unknown Error')