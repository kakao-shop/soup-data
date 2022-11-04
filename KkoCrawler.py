from selenium import webdriver # 1004 수정
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import re
import time
import pprint
import math
from kafka import KafkaProducer
import json
from json import dumps
import sys



def __main__ ():

    # a = sys.argv[1]  
    # print(a)
    kakao_crawling().start_crwal() # 트리거

#--------------크롤링 시작 ------------------------------   

class kakao_crawling:
    def __init__(self):
        # self.host = '127.0.0.1'
        # self.kafka_port = '9092'
        self.driver_path = "./chromedriver.exe"
        # self.keyword=keyword
        #  C:/Users/kjh19/OneDrive/바탕 화면/test/chromedriver.exe // 노트북
        # ./chromedriver (2).exe  // 연구실 컴
        # /home/search/apps/dw/chromedriver 서버컴
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('--disable-dev-shm-usage') # 서버컴 전용 옵션
        self.chrome_options.add_argument('window-size=1280,1000')
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=self.chrome_options)
        self.titleList = []
        self.infolist = []
        self.siteList = [
"https://store.kakao.com/category/3/102104103?level=2",
"https://store.kakao.com/category/3/102104101?level=2" ,
"https://store.kakao.com/category/3/102104107?level=2" ,
"https://store.kakao.com/category/3/102104108?level=2",
"https://store.kakao.com/category/3/102104106?level=2" ,
"https://store.kakao.com/category/3/102100?level=1" ,
"https://store.kakao.com/category/3/102104105?level=2", 
"https://store.kakao.com/category/3/102100100?level=2" ,
"https://store.kakao.com/category/3/102101110?level=2" ,
"https://store.kakao.com/category/3/102109100?level=2" ,
"https://store.kakao.com/category/3/102109103?level=2" ,
"https://store.kakao.com/category/3/102100118?level=2" ,
"https://store.kakao.com/category/3/102100111?level=2" ,
"https://store.kakao.com/category/3/102100101?level=2" ,
"https://store.kakao.com/category/3/102101?level=1" 
        ]
        self.cat = [
"과일",
"채소",
"쌀・잡곡",
"축산",
"수산・건어물",
"유제품・냉장/냉동식품",
"제과・양산빵",
"면류・양념・오일"
        ]

        self.cnt = 0
    
    def start_crwal(self):
        


        soup=""
        for site in self.siteList:
            self.driver.get(site)
            time.sleep(1)
            self.driver.find_element_by_xpath("/html/body/fu-app-root/fu-wrapper/div/div/fu-pw-category-result/div/div/cu-pagination-list/div/div[1]/div[1]/input").click()

            time.sleep(2)
            html = self.driver.page_source
            soup = BeautifulSoup(html)
            self.getData(soup)
            time.sleep(2)
            while True:
                try:
                    for i in range(4):
                        self.driver.find_element_by_xpath("/html/body/fu-app-root/fu-wrapper/div/div/fu-pw-category-result/div/div/cu-pagination-list/div/div[2]/div/button[{}]".format(str(1+i))).click()
                        time.sleep(2)
                        html = self.driver.page_source
                        soup = BeautifulSoup(html)
                        a_cnt = self.getData(soup)
                        if a_cnt == "duplicate":
                            print(a_cnt) 
                            break
                        time.sleep(2)
                except Exception as e:
                    break
                try:
                    self.driver.find_element_by_xpath("/html/body/fu-app-root/fu-wrapper/div/div/fu-pw-category-result/div/div/cu-pagination-list/div/div[3]/button[2]").click()
                    time.sleep(2)
                    html = self.driver.page_source
                    soup = BeautifulSoup(html)
                    a_cnt = self.getData(soup)
                    if a_cnt == "duplicate": break
                    time.sleep(2)
                except Exception as e:
                    break

            print(site, "정상종료")



#mArticle > div > cu-pagination-list > div > fu-view-product-section > div > ul

    def getData(self, soup):
        # print((soup.prettify()))
        cnt =0
        liList = soup.select("ul.list_productcmp")
        if liList == []:
           print("    xxxx     ", liList)
        # print(liList)
        for items in liList:
            for item in items:
                if item == " ": continue
                
                print("=====================================s")
                imgSrc = item.select_one("li div > span")["data-tiara-image"]
                prdName = item.select_one("li div > span")["data-tiara-copy"]
                if prdName in self.titleList:
                    continue
                else:
                    self.titleList.append(prdName)
                webUrl = item.select_one("li div > span > a")["href"]
                price = item.select_one("li > fu-view-product > div > span > a > div > span.price_info > span.txt_number").get_text()
            
                try:
                    purchase = item.select_one("li) > fu-view-product > div > span > a > div > span.other_info > em > span.txt_info")
                    
                except Exception as e:
                    purchase = 0
                print("imgSrc : ", imgSrc)
                print("prdName : ", prdName)
                print("webUrl : ", webUrl)
                print("price : ", price)
                print("purchase : ", purchase)
                print("=====================================e")
        
        return cnt



            
    




    


__main__()