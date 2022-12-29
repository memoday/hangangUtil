import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('User-Agent= Mozilla/5.0')
options.add_argument('headless') #크롬창 표시 금지


driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.get("https://han.gl")


def hanglShorten(longUrl):
    if "han.gl" in longUrl:
        return longUrl

    driver.find_element(By.ID,'url').send_keys(longUrl)
    driver.find_element(By.XPATH,'/html/body/section[1]/div/div/div/div/form/div/div/button[2]').click()

    for i in range(30):
        shortenUrl = driver.find_element(By.XPATH,'/html/body/section[1]/div/div/div/div/form/div/div/button[1]')
        shortenUrl = shortenUrl.get_attribute('data-clipboard-text')
        if shortenUrl != None:
            print('None 탈출')
            break
        i += 1
        print('재시도 횟수:',i)
        time.sleep(0.1)
    
    if shortenUrl == None:
        shortenUrl = 'Timeout Error'

    print(shortenUrl)
    driver.refresh()
    
    return shortenUrl

def exit():
    driver.quit()
