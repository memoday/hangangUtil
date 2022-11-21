import time
from selenium import webdriver
import os, sys
import chromedriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


start = time.time()

options = webdriver.ChromeOptions()
options.add_argument('User-Agent= Mozilla/5.0')
options.add_argument("--disable-extensions")
options.add_argument("disable-infobars")
options.add_argument("disable-gpu")
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"

options.add_argument('headless') #크롬창 표시 금지

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver_path = f'./{chrome_ver}/chromedriver.exe'
if os.path.exists(driver_path):
    print(f"chromedriver is installed: {driver_path}")
else:
    print('installing chromedriver')
    chromedriver_autoinstaller.install(cwd=True) #chromedriver 크롬 버전에 맞춰 설치

def hanglShorten(longUrl):
    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    if "han.gl" in longUrl:
        return longUrl
    driver.get("https://han.gl")

    driver.find_element_by_id('url').send_keys(longUrl)
    driver.find_element_by_xpath('/html/body/section[1]/div/div/div/div/form/div/div/button[2]').click()

    shortenUrl = driver.find_element_by_xpath('/html/body/section[1]/div/div/div/div/form/div/div/button[1]')
    time.sleep(1) #슬립없으면 값을 바로 못 불러옴
    shortenUrl = shortenUrl.get_attribute('data-clipboard-text')
    print(shortenUrl)

    print('time:',time.time()- start)

    driver.close()
    driver.quit()
    
    return shortenUrl

if __name__ == "__main__":
    hanglShorten('http://naver.com')
