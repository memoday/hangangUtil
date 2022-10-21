import time
from selenium import webdriver
import os, sys

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('User-Agent= Mozilla/5.0')
options.add_argument('headless') #크롬창 표시 금지

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
driver_path = resource_path('chromedriver.exe')


driver = webdriver.Chrome(options=options, executable_path=driver_path)

def hanglShorten(longUrl):
    if "han.gl" in longUrl:
        return longUrl
    driver.get("https://han.gl")

    driver.find_element_by_id('url').send_keys(longUrl)
    driver.find_element_by_xpath('/html/body/section[1]/div/div/div/div/form/div/div/button[2]').click()

    shortenUrl = driver.find_element_by_xpath('/html/body/section[1]/div/div/div/div/form/div/div/button[1]')
    time.sleep(1) #슬립없으면 값을 바로 못 불러옴
    shortenUrl = shortenUrl.get_attribute('data-clipboard-text')
    print(shortenUrl)
    
    return shortenUrl
