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
    
    a = len(sys.argv)  
    input_name = "김중한"
    input_idAgency = "가톨릭대학교"
    kotitle = "원뿔교차점 및 계간교차점이 포함된 광화학 반응 메커니즘 규명에 관한 이론적 연구"
    
    st11_crawling().start_crwal() # 트리거

#--------------크롤링 시작 ------------------------------   

class st11_crawling:
    def __init__(self):
        # self.host = '127.0.0.1'
        # self.kafka_port = '9092'
        self.driver_path = "./chromedriver.exe"
        #  C:/Users/kjh19/OneDrive/바탕 화면/test/chromedriver.exe // 노트북
        # ./chromedriver (2).exe  // 연구실 컴
        # /home/search/apps/dw/chromedriver 서버컴
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('--disable-dev-shm-usage') # 서버컴 전용 옵션
        self.chrome_options.add_argument('window-size=1280,640')
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=self.chrome_options)
        self.author = {}
        self.paper = []
        self.papers = []
        self.info = {}
        self.test = []
        self.infolist = []
        self.cnt = 0
    
    def start_crwal(self):
        
        self.driver.get("https://deal.11st.co.kr/browsing/DealAction.tmall?method=getCategory&dispCtgrNo=947161")
        time.sleep(1)
        cnt =0
        for i in range(2,6):
            print("/html/body/div[2]/div[3]/div/div/div[2]/div[1]/div/ul[1]/li[{}]".format(str(i)))
            try:
                self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div[2]/div[1]/div/ul[1]/li[{}]/a".format(str(i))).click()
            except Exception as e:
                self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div[2]/div[1]/div/ul[1]/li[{}]/a".format(str(i))).send_keys(Keys.ENTER)
            
            time.sleep(1)
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                time.sleep(2)

                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            self.driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            html = self.driver.page_source
            
            soup = BeautifulSoup(html, 'html.parser')
            a_cnt = self.getData(soup)
            cnt += a_cnt
        print(cnt)


    def getData(self, soup):
        cnt =0
        liList = soup.select("#dealPrdListing")
        for i, items in enumerate(liList):
            try:
                itemList = soup.select("#dealPrdListing > ul:nth-child({}) > li".format(i))
                for item in items:
                    for data in item:
                        cnt +=1
                        print("=====================================s")
                        print(cnt, data)
                        print("=====================================e")
            except Exception as e:
                continue
        return cnt



       # 1번 #mdPrd > div.viewtype3.list_htype3.ui_templateContent > div.virtual-wrap > div > ul
       # 2번 #mdPrd > div.viewtype3.list_htype3.ui_templateContent > div.virtual-wrap > div > ul

       # 1번 li태그  # /html/body/div[2]/div[3]/div/div/div[2]/div[2]/div[1]/div/ul
       # 2번 li태그    /html/body/div[2]/div[3]/div/div/div[2]/div[2]/div[3]/div/ul/li[1]
       # 식품 종류 태그 
       # /html/body/div[2]/div[3]/div/div/div[2]/div[1]/div/ul/li[1] ~[5]
       
        


            
    




    


__main__()