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
from datetime import datetime
from pytz import timezone

#--------------------------홈플러스 크롤링----------------------------
def __main__ ():
    
    st11_crawling().homeplus_crwal() # 트리거

#--------------크롤링 시작 ------------------------------   

class st11_crawling:
    def __init__(self):
        # self.host = 'my-cluster-kafka-2.my-cluster-kafka-brokers.default.svc'
        self.host = "127.0.0.1"
        self.kafka_port = '9092'
        self.producer=KafkaProducer(acks=0, 
            compression_type='gzip',
            bootstrap_servers=[self.host + ":"+ self.kafka_port],
            value_serializer=lambda x: dumps(x).encode('utf-8')
          )
        self.driver_path = "./chromedriver.exe"
        # self.driver_path = "/usr/src/chrome/chromedriver"
        self.chrome_options = Options()
        self.chrome_options.add_argument('window-size=1280,1000')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=self.chrome_options)
        self.subList = ["과일", "채소", "채소", "축산","수산/건어물", "유제품/냉장/냉동", "제과/빵" , "면류/즉석식품/양념/오일", "쌀/잡곡", "생수/음료/커피"]
        self.cnt = 0
        self.categories =['과일','채소','쌀/잡곡', '축산', '수산/건어물','유제품/냉장/냉동','제과/빵','면류/즉석식품/양념/오일','생수/음료/커피']
        self.index_name = "product-"+datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d-%H-%M')

    def findIndexName(self):
        now = datetime.now().minute
        print("current minute", now)
        if now < 29:
            self.index_name ="product-"+datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d-%H-')+"00"
        else:
            self.index_name = "product-"+datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d-%H-')+"30"
    def homeplus_crwal(self):
        print("start")
        self.findIndexName()
        data = {}
        data["index"]=self.index_name
        # print(data)
        self.producer.send("home-test",value=data)
        self.producer.flush()
        print(self.index_name)
        self.driver.get("https://front.homeplus.co.kr/leaflet?gnbNo=201")
        time.sleep(1)
        cnt = 0
        idx = 0
        for i in range(2,11 ):
            # print("/html/body/div[1]/div/div[3]/div[2]/div/div[1]/div/ul/li[{}]".format(str(i)))
            try:
                self.driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div[1]/div/ul/li[{}]/button".format(str(i))).click()
            except Exception as e:
                self.driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div[1]/div/ul/li[{}]/button".format(str(i))).send_keys(Keys.ENTER)
            
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
            a_cnt = self.getData(soup, idx)
            cnt += a_cnt
            idx += 1
        print("crawler finish")
        data = {}
        data["finish"]=self.index_name
        self.producer.send("home-test",value=data)
        self.producer.flush()

    def getData(self, soup, idx):
        cnt =0
        liList = soup.select(".itemListWrap")
        for items in liList:
            try:
               # itemList = soup.select(".itemListWrap > .itemDisplayList > div".format(i))
                for item in items:
                    for data in item:
                        cnt +=1
                        # print("=====================================s")
                        try:
                            name = data.select("div > div.detailInfo > a > p")
                            if len(name) >= 2:
                                name = data.select_one("div > div.detailInfo > a > p:nth-child(2)").get_text()
                            else:
                                name = data.select_one("div > div.detailInfo > a > p").get_text()
                            web_url = data.select_one("div > div.detailInfo > a")["href"]
                            try:
                                img_src = data.select_one("div > div.thumbWrap > button > span > img")["src"]
                            except Exception  as e:
                                img_src = None
                            dprice = data.select_one("div > div.detailInfo > div.priceWrap > div.price > strong").get_text()
                            dprice =  re.sub(r"[^0-9]", "", dprice)
                            buyer = data.select_one("div > div.detailInfo > div.prodScoreWrap > span:nth-child(3)").get_text()
                            buyer = re.sub(r"[^0-9]", "", buyer)
                            categoryName = self.categories[idx]
                            print(name)
                            data = {}
                            data["imgSrc" ] =img_src
                            data["prdName" ] = name
                            data["webUrl" ] = "https://front.homeplus.co.kr" +web_url
                            data["price"] = dprice
                            data["purchase"]  = int(buyer)
                            data["cat"] = categoryName
                            data["index"] = self.index_name
                            kafka={"data":data}
                            self.pushData(kafka)
                        except Exception as e:
                            print("",e)
                        # print(cnt)
                        # print("=====================================e")
            except Exception as e:
                continue 
        return cnt


    def pushData(self, data):
        self.producer.send("home-test",value=data)
        self.producer.flush()
     

__main__()