from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
import time
import shutil
import requests
import pandas as pd

ACCOUNT_USERNAME = 'wantsconnny'
ACCOUNT_PASSWORD = 'test123!'

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=options)

cafeList = './Cafe_Data_Jeju_by_Sophia.csv'
cafeList = pd.read_csv(cafeList, encoding='cp949')

driver.get('https://www.instagram.com/')
time.sleep(5)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(ACCOUNT_USERNAME)
time.sleep(3)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(ACCOUNT_PASSWORD)
time.sleep(3)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
time.sleep(5)

names = cafeList['사업장명'].to_list()
baseUrl = 'https://www.instagram.com/explore/tags/'
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'나중에 하기')]"))).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'나중에 하기')]"))).click()
time.sleep(10)

for plusUrl in names:
    if os.path.isdir('./img/' + plusUrl):
        continue

    url = baseUrl + quote_plus(plusUrl)
    driver.get(url)
    time.sleep(15)

    html = driver.page_source
    soup = BeautifulSoup(html)
    imglist = []

    try:
        os.mkdir('./img/' + plusUrl)

        for i in range(0, 3):
            insta = soup.select('.v1Nh3.kIKUG._bz0w')

            for i in insta:
                print('https://www.instagram.com'+ i.a['href'])
                imgUrl = i.select_one('.KL4Bh').img['src']
                imglist.append(imgUrl)
                imglist = list(set(imglist))
                html = driver.page_source
                soup = BeautifulSoup(html)
                insta = soup.select('.v1Nh3.kIKUG._bz0w')
                
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        for i in range(0, 30):
            image_url = imglist[i]
            resp = requests.get(image_url, stream=True)
            local_file = open('./img/' + plusUrl + '/' + str(i) + '.jpg', 'wb')
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, local_file)
            del resp
    except:
        pass

    time.sleep(2)
    # print(imgUrl)
    # print(imglist)

driver.close()