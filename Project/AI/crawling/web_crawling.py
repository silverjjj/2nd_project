from urllib.request import urlopen,Request
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver # webdriver 가져오기
import time
import os

k_categories = list(input("한글명:").split())
e_categories = list(input("영어명:").split())
####################################################################################
# bing.com에서 이미지 크롤링
####################################################################################
for i in range(len(k_categories)):
    ko_name = k_categories[i]
    en_name = e_categories[i]
    # url_name = url_categories[i]
    start = time.time()  # 시작 시간 저장
    print(ko_name + "의 데이터 수집 시작")

    # bing
    baseUrl = "https://www.bing.com/images/search?q="
    baseUrl2 = "&form=HDRSC2&first=1&scenario=ImageBasicHover"

    # 웹페이지를 안보이게해줌 
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')

    url = baseUrl + quote_plus(ko_name) + baseUrl2
    driver = webdriver.Chrome(
            executable_path = "C:/Users/multicampus/chromedriver_win32/chromedriver.exe",
            chrome_options=options)
    
    driver.get(url)
    time.sleep(1)

    SCROLL_PAUSE_TIME = 1.0
    url_path = []
    cnt = 0 
    ####################################################################################
    # 1. 이미지 url 수집
    ####################################################################################
    while cnt < 11: # cnt 1당 => 약 50개 사이의 이미지 데이터 추출
        print(cnt)
        cnt += 1
        pageString = driver.page_source
        bsObj = BeautifulSoup(pageString, 'html.parser')
        try:
            for line in bsObj.find_all(name='div', attrs={"class":"img_cont hoff"}):
                page = line.find(name="img")["src"]
                if page.find("data:image/jpeg") == -1:
                    url_path.append(page)
        
        except IndexError as ider:
            print("IndexError")
        
        last_height = driver.execute_script('return document.body.scrollHeight')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            else:
                last_height = new_height
                continue
        time.sleep(0.3)
        url_path = list(set(url_path))
    driver.close()
    url_path = list(set(url_path))
    print("추출된 url 개수는 : ",len(url_path))

    ####################################################################################
    # 2. 저장
    ####################################################################################
    # images에 폴더 만들기 (폴더는 영어이름으로만 지정)
    try:
        if not os.path.exists("./images/"+en_name):
            os.makedirs("./images/"+en_name)
    except OSError:
        print('Error:Creating Directory' + en_name)

    print(ko_name , "의 걸린 시간 : " , time.time() - start)

    # 크롤링한 url 이미지를 jpg로 저장함
    n = 1
    print("이미지 저장중입니다.")
    for url in url_path:
        with urlopen(url) as f:
            with open('./images/'+en_name+"/"+en_name+str(n)+'.jpg','wb') as h:
                img = f.read()
                h.write(img)
            n += 1
    print("이미지 저장이 끝났습니다.")

print("총 걸린 시간 :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    