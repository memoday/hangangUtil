import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import os

options = webdriver.ChromeOptions()
options.add_argument('User-Agent= Mozilla/5.0')
options.add_argument('headless') #크롬창 표시 금지


chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver_path = f'./{chrome_ver}/chromedriver.exe'
if os.path.exists(driver_path):
    print(f"chromedriver is installed: {driver_path}")
else:
    print('installing chromedriver')
    chromedriver_autoinstaller.install(cwd=True) #chromedriver 크롬 버전에 맞춰 설치

    
driver = webdriver.Chrome(options=options, executable_path=driver_path)
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
