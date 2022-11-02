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

    a = sys.argv[1]  
    print(a)
    kakao_crawling(a).start_crwal() # 트리거

#--------------크롤링 시작 ------------------------------   

class kakao_crawling:
    def __init__(self, keyword):
        # self.host = '127.0.0.1'
        # self.kafka_port = '9092'
        self.driver_path = "./chromedriver.exe"
        self.keyword=keyword
        #  C:/Users/kjh19/OneDrive/바탕 화면/test/chromedriver.exe // 노트북
        # ./chromedriver (2).exe  // 연구실 컴
        # /home/search/apps/dw/chromedriver 서버컴
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('--disable-dev-shm-usage') # 서버컴 전용 옵션
        self.chrome_options.add_argument('window-size=1280,1000')
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=self.chrome_options)
        self.author = {}
        self.paper = []
        self.papers = []
        self.info = {}
        self.test = []
        self.infolist = []
        self.cnt = 0
    
    def start_crwal(self):
        print(self.keyword)
        self.driver.get("https://store.kakao.com/")
        time.sleep(2)
        try:
            self.driver.find_element_by_xpath("/html/body/fu-app-root/fu-wrapper/div/fu-view-pc-gnb/div/div/div/div[3]/fu-view-gnb-menu-util/a[1]").click()
            self.driver.find_element_by_xpath("/html/body/cu-popup-container2[1]/cu-popup-wrapper2/fu-layer-search-entry/div/div/div[1]/div[1]/div/form/fieldset/div/input").send_keys(self.keyword)
            self.driver.find_element_by_xpath("/html/body/cu-popup-container2[1]/cu-popup-wrapper2/fu-layer-search-entry/div/div/div[1]/div[1]/div/form/fieldset/div/input").send_keys(Keys.RETURN)

        except Exception as e:
            print(e)
            self.driver.find_element_by_xpath("/html/body/fu-app-root/fu-wrapper/div/fu-view-pc-gnb/div/div/div/div[3]/fu-view-gnb-menu-util/a[1]").send_keys(Keys.ENTER)
            self.driver.find_element_by_xpath("/html/body/cu-popup-container2[1]/cu-popup-wrapper2/fu-layer-search-entry/div/div/div[1]/div[1]/div/form/fieldset/div/input").send_keys(self.keyword)
            self.driver.find_element_by_xpath("/html/body/cu-popup-container2[1]/cu-popup-wrapper2/fu-layer-search-entry/div/div/div[1]/div[1]/div/form/fieldset/div/input").send_keys(Keys.RETURN)
        time.sleep(2)
        self.driver.find_element_by_xpath("#mArticle > div.search_result > fu-view-search-filters > div > ul > li:nth-child(1) > a").click()
        html = self.driver.page_source
            
        soup = BeautifulSoup(html, 'html.parser')
        a_cnt = self.getData(soup)
        # cnt =0
        # for i in range(2,6):
        #     print("/html/body/div[2]/div[3]/div/div/div[2]/div[1]/div/ul[1]/li[{}]".format(str(i)))
            
            
        #     time.sleep(1)
        #     last_height = self.driver.execute_script("return document.body.scrollHeight")

        #     while True:
        #         self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #         time.sleep(2)

        #         new_height = self.driver.execute_script("return document.body.scrollHeight")
        #         if new_height == last_height:
        #             break
        #         last_height = new_height
        #     self.driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        #     html = self.driver.page_source
            
        #     soup = BeautifulSoup(html, 'html.parser')
        #     a_cnt = self.getData(soup)
        #     cnt += a_cnt
        # print(cnt)


    def getData(self, soup):
        cnt =0
        liList = soup.select("#dealPrdListing")
        for i, items in enumerate(liList):
            try:
                itemList = soup.select("#dealPrdListing > ul:nth-child({}) > li".format(i))
                for item in items:
                    for data in item:
                        # print(data)
                        cnt +=1
                        print("=====================================s")
                        try:
                            name_url = eval(data.select_one("li > div > a")["data-log-body"])
                            web_url = data.select_one("li > div > a")["href"]
                            img_src = data.select_one("li > div > a> div.prd_img > img")["src"]
                            categoryName = data.select_one("li > div > div> a").get_text()
                            purchases = data.select_one("li > div > a > div.prd_info > span").get_text()
                        
                            print("name", name_url["content_name"])
                            print("img_src", img_src)
                            print("web_url", web_url)
                            print("categoryName", categoryName)
                            print("last_discount_price", name_url["last_discount_price"])
                            if purchases == "추천상품":
                                print("0")
                            else:
                                print("purchases",purchases)

                            # url = data.select_one("li > div > a")["href"]
                            # print(url)
                        except Exception as e:
                            print(e, " ???? ")
                        #print(cnt, data)
                        print("=====================================e")
            except Exception as e:
                continue
        return cnt



            
    




    


__main__()