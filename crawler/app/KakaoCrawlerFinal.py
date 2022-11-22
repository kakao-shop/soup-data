from selenium import webdriver # 1004 수정
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import re
import time
from kafka import KafkaProducer
import json
from json import dumps
from datetime import datetime
from pytz import timezone
def __main__ ():
    # a = sys.argv[1]  
    # print(a)
    kakao_crawling().start_crwal() # 트리거
#   my-kafka.kafka.svc.cluster.local:9092 
#--------------크롤링 시작 ------------------------------   
class kakao_crawling:
    def __init__(self):
        self.bootstrap_server = ['localhost:9092']
        # self.host = "localhost"
        # self.kafka_port = '9092'
        self.producer=KafkaProducer(acks=0, 
            compression_type='gzip',
            # bootstrap_servers=[self.host + ":"+ self.kafka_port],
            bootstrap_servers=self.bootstrap_server,
            value_serializer=lambda x: dumps(x).encode('utf-8')
          )

        self.index_name =""
        #self.driver_path = "/usr/src/chrome/chromedriver"
        self.driver_path = "./chromedriver.exe"
        self.chrome_options = Options()
        self.chrome_options.add_argument('window-size=1280,1000')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=self.chrome_options)
        self.titleList = []
        self.subList = ["과일", "채소", "채소", "축산","수산/건어물", "냉장/냉동식품", "제과/빵" , "즉석식품/양념", "쌀/잡곡", "생수/음료"]
        self.siteList =  [                       
            ["https://store.kakao.com/category/3/102104103?level=2", "과일"],
            ["https://store.kakao.com/category/3/102104101?level=2" , "채소"],
            ["https://store.kakao.com/category/3/102104110?level=2","채소"],
            ["https://store.kakao.com/category/3/102100123?level=2","채소"],
            ["https://store.kakao.com/category/3/102104104?level=2","축산"],
            ["https://store.kakao.com/category/3/102104108?level=2","축산"],
            ["https://store.kakao.com/category/3/102104106?level=2","축산"],
            ["https://store.kakao.com/category/3/102104114?level=2","축산"],
            ["https://store.kakao.com/category/3/102104105?level=2", "수산/건어물"] , 
            ["https://store.kakao.com/category/3/102104109?level=2", "수산/건어물"],
            ["https://store.kakao.com/category/3/102104117?level=2", "수산/건어물"],
            ["https://store.kakao.com/category/3/102104102?level=2","냉장/냉동식품"],
            ["https://store.kakao.com/category/3/102104100?level=2", "냉장/냉동식품"],
            ["https://store.kakao.com/category/3/102100100?level=2" ,"냉장/냉동식품"],
            ["https://store.kakao.com/category/3/102100112?level=2" ,"냉장/냉동식품"],
            ["https://store.kakao.com/category/3/102100118?level=2" , "냉장/냉동식품"],
            ["https://store.kakao.com/category/3/102100111?level=2", "냉장/냉동식품"],
            ["https://store.kakao.com/category/3/102109?level=1", "제과/빵"],
            [ "https://store.kakao.com/category/3/102100101?level=2", "즉석식품/양념"],
            [ "https://store.kakao.com/category/3/102100103?level=2", "즉석식품/양념"],
            [ "https://store.kakao.com/category/3/102100104?level=2", "즉석식품/양념"],
            [ "https://store.kakao.com/category/3/102100105?level=2", "즉석식품/양념"],
            [ "https://store.kakao.com/category/3/102100109?level=2", "즉석식품/양념"],
            [ "https://store.kakao.com/category/3/102100111?level=2", "즉석식품/양념"],
            [ "https://store.kakao.com/category/3/102100110?level=2", "즉석식품/양념"],
            [ "https://store.kakao.com/category/3/102100141?level=2", "즉석식품/양념"],
            [ "https://store.kakao.com/category/3/102100124103?level=3", "즉석식품/양념"],
            [ "https://store.kakao.com/category/3/102104116?level=2", "즉석식품/양념"],

            [ "https://store.kakao.com/category/3/102104107?level=2", "쌀/잡곡"],
            [ "https://store.kakao.com/category/3/102100119?level=2", "쌀/잡곡"],
            [ "https://store.kakao.com/category/3/102104115?level=2", "쌀/잡곡"],
            [ "https://store.kakao.com/category/3/102104129?level=2", "쌀/잡곡"],

            [ "https://store.kakao.com/category/3/102101?level=1", "생수/음료"]
        ]
        self.cnt = 0
    def findIndexName(self):
        now = datetime.now(timezone('Asia/Seoul')).minute
        print("current minute", now)
        if now < 29:
            self.index_name = "product-"+datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d-%H-')+"00"
        else:
            self.index_name = "product-"+datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d-%H-')+"30"
    def start_crwal(self):
        print("start crawl")
        data = {}
        self.findIndexName()
        for site in self.siteList:
            print(site)
            print(self.driver)
            self.driver.get(site[0])
            
            time.sleep(1)
            try:
                self.driver.find_element_by_xpath("/html/body/fu-app-root/fu-wrapper/div/div/fu-pw-category-result/div/div/cu-pagination-list/div/div[1]/div[1]/input").click()
            
            except Exception as e:
                print( e)
                continue
            time.sleep(1)
            html = self.driver.page_source
            soup = BeautifulSoup(html)
            self.getData(soup, site[1])
            time.sleep(2)
            while True:
                try:
                    for i in range(4):
                        self.driver.find_element_by_xpath("/html/body/fu-app-root/fu-wrapper/div/div/fu-pw-category-result/div/div/cu-pagination-list/div/div[2]/div/button[{}]".format(str(1+i))).click()
                        time.sleep(1)
                        html = self.driver.page_source
                        soup = BeautifulSoup(html)
                        a_cnt = self.getData(soup, site[1])
                        if a_cnt == "duplicate":
                            break
                        time.sleep(1)
                except Exception as e:
                    print(e)
                    break
                try:
                    self.driver.find_element_by_xpath("/html/body/fu-app-root/fu-wrapper/div/div/fu-pw-category-result/div/div/cu-pagination-list/div/div[3]/button[2]").click()
                    time.sleep(2)
                    html = self.driver.page_source
                    soup = BeautifulSoup(html)
                    # print("????????????????????",site[1])
                    a_cnt = self.getData(soup, site[1])
                    if a_cnt == "duplicate": break
                    time.sleep(3)
                except Exception as e:
                    print(e)
                    break
 
            print(site[0], "정상종료")

        print("crawler finish")


        data = {}
        data["finish"]=self.index_name
        # self.elasticAPI.createIndex(data["index"])
        self.producer.send("kakao-test",value=data)
        self.producer.flush()
        #time.sleep(1)

    def getData(self, soup, cat):
        # print("파싱하나?")
        # print((soup.prettify()))
        cnt =0                                                                                                                                                                                                                                                                              
        liList = soup.select("ul.list_productcmp")
        if liList == []:
           print("    xxxx     ", liList)
        # print(liList)
        for items in liList:
            for item in items:
                if item == " ": continue
                # time.sleep(1)
                # print("=====================================s")
                imgSrc = item.select_one("li div > span")["data-tiara-image"]
                prdName = item.select_one("li div > span")["data-tiara-copy"]
                if prdName in self.titleList:
                    continue
                else:
                    self.titleList.append(prdName)
                webUrl = item.select_one("li div > span > a")["href"]
                price = item.select_one("li > fu-view-product > div > span > a > div > span.price_info > span.txt_number").get_text()
                price = int(re.sub(r"[^0-9]", "", price))
                # try:
                purchase = item.select("li > fu-view-product > div > span > a > div > span.other_info > em > span.txt_info")
                purch=list(purchase)
                for i in purch:
                    try:
                        purch = int(re.sub(r"[^0-9]", "", str(i)))
                    except Exception as e:
                        purch =0
                # print("imgSrc : ", imgSrc)
                print("prdName : ", prdName)
                # print("webUrl : ", webUrl)
                # print("price : ", type(price), price)
                # print("purchase : ", purch)
                # print("cat :", cat)
                # print("=====================================e")
                data = {}
                data["imgSrc" ] =imgSrc
                data["prdName" ] = prdName
                data["webUrl" ] = webUrl
                data["price"] = price
                data["purchase"]  = purch
                data["cat"] = cat
                data["index"] = self.index_name
                kafka={"data":data}
                self.pushData(kafka)
        return cnt

    def pushData(self, data):
        self.producer.send("kakao-test",value=data)
        self.producer.flush()

__main__()