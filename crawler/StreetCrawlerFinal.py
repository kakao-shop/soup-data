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

def __main__ ():
    
    a = len(sys.argv)  
    st11_crawling().start_crwal() # 트리거

#--------------크롤링 시작 ------------------------------   

class st11_crawling:
    def __init__(self):

        # self.client = MongoClient('mongodb://127.0.0.1:27017', authSource='admin')
        # self.homeplus = self.client["DATAETL"]['Street']
        self.host = '127.0.0.1'
        self.kafka_port = '9092'
        self.producer=KafkaProducer(
            acks=0, 
            compression_type='gzip',
            bootstrap_servers=[self.host + ":"+ self.kafka_port],
            value_serializer=lambda x: dumps(x).encode('utf-8'),
            linger_ms=1000

          )
        self.driver_path = "./chromedriver.exe"
        #  C:/Users/kjh19/OneDrive/바탕 화면/test/chromedriver.exe // 노트북

        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('--disable-dev-shm-usage') # 서버컴 전용 옵션
        self.chrome_options.add_argument('window-size=1280,1000')
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=self.chrome_options)
        self.category = []
        self.index_name = "product-"+datetime.now().strftime('%Y-%m-%d-%H-%M')

        self.cnt = 0
    def findIndexName(self):
        now = datetime.now().minute
        print("current minute", now)
        if now < 29:
            self.index_name = "product-"+datetime.now().strftime('%Y-%m-%d-%H-')+"00"
        else:
            self.index_name = "product-"+datetime.now().strftime('%Y-%m-%d-%H-')+"30"

    def start_crwal(self):
        self.findIndexName()
        data = {}
        data["index"]=self.index_name
        print(data)
        self.producer.send("street-test",value=data)
        self.producer.flush()
        
        self.driver.get("https://deal.11st.co.kr/browsing/DealAction.tmall?method=getCategory&dispCtgrNo=947161")
        time.sleep(1)
        cnt =0
        for i in range(2,6):
            print("/html/body/div[2]/div[3]/div/div/div[2]/div[1]/div/ul[1]/li[{}]".format(str(i)))
            try:
                try:
                    self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div[2]/div[1]/div/ul[1]/li[{}]/a".format(str(i))).click()
                except Exception as e:
                    self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div[2]/div[1]/div/ul[1]/li[{}]/a".format(str(i))).send_keys(Keys.ENTER)
            except Exception as e:
                continue    
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
        print(set(self.category))
    
        print("crawler finish")
        data = {}
        data["finish"]=self.index_name
        # self.elasticAPI.createIndex(data["index"])st
        self.producer.send("street-test",value=data)
        self.producer.flush()



    def getData(self, soup):
        cnt =0
        liList = soup.select("#dealPrdListing")
        for i, items in enumerate(liList):
            
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
                        self.category.append(categoryName)

                        print("name", name_url["content_name"])
                        print("img_src", img_src)
                        print("web_url", web_url)
                        print("categoryName", categoryName)
                        print("last_discount_price", name_url["last_discount_price"])
                        print("purchases : ", purchases)
                        data = {}
                        data["imgSrc" ] =img_src
                        data["prdName" ] = name_url["content_name"]
                        data["webUrl" ] = web_url
                        data["price"] = int(re.sub(r"[^0-9]", "", name_url["last_discount_price"]))  
                        data["purchase"]  = int(re.sub(r"[^0-9]", "", purchases))
                        data["cat"] = categoryName
                        if categoryName == "채소류":
                            data["cat"] = "채소"
                        elif categoryName == "과일/견과":
                            data["cat"] = "과일"
                        elif categoryName == "축산물":
                            data["cat"] = "축산"
                        elif categoryName in [ "차/전통음료", "커피", "전통주", "생수/음료","홍삼/건강즙"]:
                            data["cat"] = "생수/음료/커피"
                        elif categoryName == "우유/두유":
                            data["cat"] = "유제품/냉장/냉동"
                        elif categoryName in ["라면/즉석식품","조미료/소스류","통조림/식용유/잼"]:
                            data["cat"] = "면류/즉석식품/양념/오일"
                        elif categoryName == "쌀/잡곡류":
                            data["cat"] = "쌀/잡곡"
                        elif categoryName == "수산물":
                            data["cat"] = "수산/건어물"
                        elif categoryName == "과자/간식":
                            data["cat"] = "제과/빵"
                        else: continue
                        kafka={"data":data}
                        print(kafka)
                        self.pushData(kafka)


                        # url = data.select_one("li > div > a")["href"]
                        # print(url)
                    except Exception as e:
                        print(e, " ???? ")
                    #print(cnt, data)
                    print("=====================================e")
            
        return cnt

    def pushData(self, data):
        self.producer.send("street-test",value=data)
        print("????")
        self.producer.flush()

       
        


            
    




    


__main__()