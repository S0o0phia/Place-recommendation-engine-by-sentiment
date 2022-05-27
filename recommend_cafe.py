import io
import os
import time
import shutil
import joblib
import random
import getpass
import webbrowser
import collections
import folium
import numpy as np
import pandas as pd
import urllib.parse
import urllib.request
from glob import glob
from tqdm import tqdm
from folium.map import Icon
from colorthief import ColorThief
from seleniumrequestshtml import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_dominant_color(img):
  """Given an image in url format, eturn the dominant color."""
  try:
    f = io.BytesIO(img)
    color_thief = ColorThief(f)
    color = color_thief.get_color(quality=1)
    return color
  except:
    return np.NaN 

def scroll_down(webdriver):
    webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

def add_photo(webdriver) :
    temp_list = []
    one_photo = webdriver.find_elements_by_class_name("FFVAD")
    for n in one_photo:
        temp = {}
        temp['alt'] = n.get_attribute('alt')
        temp['src'] = n.get_attribute('src')
        temp_list.append(temp)
    return temp_list
#넘어오는 형식은 [{alt:내용, src:주소1},{alt:내용, src:주소}]

if os.path.isdir('./user'): shutil.rmtree('./user')
os.mkdir('user')

#검색을 원하는 insta ID
insta_id = input("인스타그램 ID : ")
insta_pw = getpass.getpass("비밀번호 : ")
url = "https://www.instagram.com/" + insta_id + '/'

chrome_options = Options()
chrome_options.add_argument('--log-level=3')

webdriver = Chrome(options=chrome_options)
webdriver.get('https://www.instagram.com/accounts/login/')
time.sleep(3)

webdriver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(insta_id)
time.sleep(3)
webdriver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(insta_pw)
time.sleep(3)
webdriver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
time.sleep(5)

WebDriverWait(webdriver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'나중에 하기')]"))).click()
WebDriverWait(webdriver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'나중에 하기')]"))).click()
time.sleep(10)

webdriver.get(url)
time.sleep(3)

session = webdriver.requests_session
response = session.get(url)

#포스트의 총 개수
len_post = int(webdriver.find_element_by_class_name('g47SY').text)
print('포스트 수집중...'.format(len_post))
photo_list = []
time.sleep(3)

try:
    while len(photo_list) != len_post:
        for n in add_photo(webdriver):
            if n in photo_list: pass
            else: photo_list.append(n)

        scroll_down(webdriver)
        if(len(photo_list) == int(len_post)):  break

except:
    pass

for i, n in enumerate(photo_list):
    if i >= 30 or i >= len(photo_list): break
    urllib.request.urlretrieve(n['src'], './user/' + str(i) + '.jpg')

webdriver.close()

emotion = None
emotions = []
photos = glob('./user/*')
for photo in tqdm(photos, desc="당신의 인스타그램 분석중.."):
    with open(photo, 'rb') as f:
        data = f.read()
        color = list(get_dominant_color(data))

        x = np.array(color)
        x = x.reshape(-1, 1)
        x = np.transpose(x)

        clf_from_joblib = joblib.load('placeEmotion.pkl') 
        tmp = clf_from_joblib.predict(x)
        try:  emotions.append(tmp[0])
        except: emotions.append('x')
    
    counts = collections.Counter(emotions)
    t = list(counts.most_common(2))
    if 'x' in t[0]: emotion = t[1][0]
    else: emotion = t[0][0]

print('당신의 인스타그램 분위기는?: ' + emotion)

matched = pd.read_csv('matched_emotions.csv')
recommends = list(matched[matched['분위기'] == emotion]['업장명'])
recommends = random.sample(recommends, 3)

rome_lat, rome_lng = 33.379894, 126.545211
m = folium.Map(location=[rome_lat, rome_lng], zoom_start=10) #, height='50%')
origin = pd.read_csv('Cafe_Data_Jeju_by_Sophia.csv')

for recommend in recommends:
    place = origin[origin['사업장명'] == recommend]

    x = list(place['x'])[0]
    y = list(place['y'])[0]
    address = list(place['도로명전체주소'])[0]
    print(recommend, '-', address)

    iframe = "<b>" + recommend+ "</b><br> "+ address
    popup = folium.Popup(iframe, min_width=200, max_width=200)

    folium.Marker(
            location=[y, x],
            popup=popup,
#            tooltip=address,
            icon=folium.Icon(color='blue', icon='star')).add_to(m)

m.save('recommended_map.html')
print("지도 표시중...")
time.sleep(2)
webbrowser.open_new('recommended_map.html')