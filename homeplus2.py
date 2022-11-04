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

#--------------------------홈플러스 크롤링----------------------------
def __main__ ():
    
    st11_crawling().homeplus_crwal() # 트리거

#--------------크롤링 시작 ------------------------------   

class st11_crawling:
    def __init__(self):
        # self.host = '127.0.0.1'
        # self.kafka_port = '9092'
        self.driver_path = "./chromedriver.exe"
        self.con = pymysql.connect(host='localhost', user='root', password='whdgns1002@',
                       db='product_test', charset='utf8')
        self.cur = self.con.cursor()
        self.chrome_options = Options()
        
        self.chrome_options.add_argument('window-size=1280,640')
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=self.chrome_options)
        self.author = {}
        self.paper = []
        self.papers = []
        self.info = {}
        self.test = []
        self.infolist = []
        self.cnt = 0
    
    def homeplus_crwal(self):
        
        self.driver.get("https://front.homeplus.co.kr/leaflet?gnbNo=201")
        time.sleep(1)
        cnt = 0
        idx = 0
        for i in range(2,10):
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
        print(cnt)


    def getData(self, soup, idx):
        cnt =0
        categories = ['과일','채소','쌀/잡곡', '축산', '수산/건어물','유제품/냉동식품','제과','즉석식품/조미료','물/음료']
        liList = soup.select(".itemListWrap")
        for items in liList:
            try:
               # itemList = soup.select(".itemListWrap > .itemDisplayList > div".format(i))
                for item in items:
                    for data in item:
                        cnt +=1
                        print("=====================================s")
                        try:
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
                            categoryName = categories[idx]

                            data = {}
                            data["imgSrc" ] =img_src
                            data["prdName" ] = name
                            data["webUrl" ] = "https://front.homeplus.co.kr" +web_url
                            data["price"] = dprice
                            data["purchase"]  = int(buyer)
                            data["cat"] = categoryName
                            self.pushData(data)
                        except Exception as e:
                            print("",e)
                        print(cnt)
                        print("=====================================e")
            except Exception as e:
                continue 
        return cnt


    def pushData(self, data):
        sql = "insert into homeplus_product(imgsrc, prdname, weburl, purchase, cat, price) values (%s, %s, %s, %s, %s, %s)".format()
        print(data)
        self.cur.execute(sql, (data["imgSrc"],data["prdName"] , data["webUrl"],data["purchase"] , data["cat"] ,data["price"]))
        self.con.commit()  
        


__main__()