import time
from selenium import webdriver
import os
import chromedriver_autoinstaller

options = webdriver.ChromeOptions()
options.add_argument('User-Agent= Mozilla/5.0')
options.add_argument("--disable-extensions")
options.add_argument("disable-infobars")
options.add_argument("disable-gpu")

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

    driver.find_element_by_id('url').send_keys(longUrl)
    driver.find_element_by_xpath('/html/body/section[1]/div/div/div/div/form/div/div/button[2]').click()

    time.sleep(0.7) #슬립없으면 값을 바로 못 불러옴
    shortenUrl = driver.find_element_by_xpath('/html/body/section[1]/div/div/div/div/form/div/div/button[1]')
    shortenUrl = shortenUrl.get_attribute('data-clipboard-text')
    print(shortenUrl)
    driver.refresh()
    
    return shortenUrl

def exit():
    driver.quit()

if __name__ == "__main__":
    hanglShorten('http://naver.com')
