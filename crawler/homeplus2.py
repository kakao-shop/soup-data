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
import pymysql
from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers
from datetime import datetime


#--------------------------홈플러스 크롤링----------------------------
def __main__ ():
    
    st11_crawling().homeplus_crwal() # 트리거

#--------------크롤링 시작 ------------------------------   

class st11_crawling:
    def __init__(self):
        self.host = '127.0.0.1'
        self.kafka_port = '9092'
        self.producer=KafkaProducer(acks=0, 
            compression_type='gzip',
            bootstrap_servers=[self.host + ":"+ self.kafka_port],
            value_serializer=lambda x: dumps(x).encode('utf-8')
          )
        # self.client = MongoClient('mongodb://127.0.0.1:27017', authSource='admin')
        # self.homeplus = self.client["DATAETL"]['Homeplus']
        self.driver_path = "./chromedriver.exe"
        # self.con = pymysql.connect(host='localhost', user='root', password='whdgns1002@',
        #                db='product_test', charset='utf8')
        # self.cur = self.con.cursor()
        self.chrome_options = Options()
        self.elasticAPI = ElaAPI()
        self.chrome_options.add_argument('window-size=1280,640')
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=self.chrome_options)
        self.subList = ["과일", "채소", "채소", "축산","수산/건어물", "유제품/냉장/냉동", "제과/빵" , "면류/즉석식품/양념/오일", "쌀/잡곡", "생수/음료/커피"]
        self.cnt = 0
        self.categories =['과일','채소','쌀/잡곡', '축산', '수산/건어물','유제품/냉장/냉동','제과/빵','면류/즉석식품/양념/오일','생수/음료/커피']
        self.index_name = "product-"+datetime.now().strftime('%Y-%m-%d-%H-%M')

    def homeplus_crwal(self):
        data = {}
        data["index"]=self.index_name
        self.elasticAPI.createIndex(self.index_name)
        print(self.elasticAPI.allIndex())
        print(data)
        self.producer.send("home-test",value=data)
        self.producer.flush()
        
        self.driver.get("https://front.homeplus.co.kr/leaflet?gnbNo=201")
        time.sleep(1)
        cnt = 0
        idx = 0
        for i in range(2,11 ):
            print("/html/body/div[1]/div/div[3]/div[2]/div/div[1]/div/ul/li[{}]".format(str(i)))
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
        # self.normalize()


    def getData(self, soup, idx):
        cnt =0
        liList = soup.select(".itemListWrap")
        for items in liList:
            try:
               # itemList = soup.select(".itemListWrap > .itemDisplayList > div".format(i))
                for item in items:
                    for data in item:
                        cnt +=1
                        print("=====================================s")
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

                            data = {}
                            data["imgSrc" ] =img_src
                            data["prdName" ] = name
                            data["webUrl" ] = "https://front.homeplus.co.kr" +web_url
                            data["price"] = dprice
                            data["purchase"]  = int(buyer)
                            data["cat"] = categoryName
                            kafka={"data":data}
                            self.pushData(kafka)
                        except Exception as e:
                            print("",e)
                        print(cnt)
                        print("=====================================e")
            except Exception as e:
                continue 
        return cnt


    def pushData(self, data):
        self.producer.send("home-test",value=data)
        self.producer.flush()
        
        # sql = "insert into homeplus_product(imgsrc, prdname, weburl, purchase, cat, price) values (%s, %s, %s, %s, %s, %s)".format()
        # print(data)
        # self.cur.execute(sql, (data["imgSrc"],data["prdName"] , data["webUrl"],data["purchase"] , data["cat"] ,data["price"]))
        # self.con.commit()  
    
    def normalize(self):
        print("start normalize")
        for cat in self.categories:
            try:
                res = es.search(
                    index=self.index_name, 
                    
                    body={
                        "size": 0,
                        "query":{"match":{"site":"home" },
                                "match":{"cat":cat}},
                        "aggs": {
                            "test": {
                            "max": { "field": "purchase"}
                            }
                    }
                    }
                )
                print(res)
                print(res["aggregations"]["test"]["value"])
                print(cat)
                # 업데이트 쿼리
                res2= es.update_by_query(
                    index=self.index_name,  
                    body = {
                "query" :{
                    "bool": {
                            "must":[
                            {"match": {"site": "home"}},
                            { "match":{"cat":cat}}
                    ]
                    }
                }, 
                "script": {
                "source":"ctx._source.score =ctx._source.score * 1/{};".format(str(int(res["aggregations"]["test"]["value"]))),
                "lang": "painless"
                }  }
                )
                print("res2", res2)
            except Exception as e:
                print(e)
        print("end normalize")

es = Elasticsearch(hosts="127.0.0.1", port=9200)
class ElaAPI:
    
       # 객체 생성
    def deleteIndex(self, str_index):
        es.indices.delete(index=str_index, ignore=[400, 404])

    def allIndex(self):
        print (es.cat.indices())

    def dataInsert(self, docs):
        # ===============
        # 데이터 삽입
        # ===============
        helpers.bulk(es, docs)

    def searchAll(self, index):
        res = es.search(
            index = index, 
            body = {
                "query":{"match_all":{}}
            }
        )
        print (json.dumps(res, ensure_ascii=False, indent=4))


    def createIndex(self, date):
        # ===============
        # 인덱스 생성
        # ===============
        index = "product-" + date
  
        if es.indices.exists(index=index):
            pass
        else:
            es.indices.create(
            index = index,
            body = {
                "settings": {
                    "analysis": {
                        "analyzer": {
                            "content": {
                                "type": "custom",
                                "tokenizer": "nori_tokenizer",
                                "decompound_mode": "mixed"
                                }
      
                        }
                    }
                },
                "mappings": {
                
                        "properties": {
                            "imgSrc":    {"type": "text"},
                            "prdName": {"type": "text","analyzer": "content"},
                            "webUrl":    {"type": "text"},
                            "purchase":    {"type": "text"},
                            "subcat":   {"type": "text"},
                            "site":     {"type": "text"},
                            "cat":   {"type": "text"},
                            "price":     {"type": "integer"},
                            "score":   {"type": "float"}
                            }
                        
                    }
                }
            )

__main__()