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
import pandas as pd

def __main__ ():

    # a = sys.argv[1]  
    # print(a)
    kakao_crawling().start_crwal() # 트리거

#--------------크롤링 시작 ------------------------------   




class kakao_crawling:
    def __init__(self):
        # self.host = '127.0.0.1'
        # self.kafka_port = '9092'
        self.con = pymysql.connect(host='localhost', user='root', password='whdgns1002@',
                       db='product_test', charset='utf8')
        self.cur = self.con.cursor()
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

            ["https://store.kakao.com/category/3/102104102?level=2","유제품/냉장/냉동"],
            ["https://store.kakao.com/category/3/102104100?level=2", "유제품/냉장/냉동"],
            ["https://store.kakao.com/category/3/102100100?level=2" ,"유제품/냉장/냉동"],
            ["https://store.kakao.com/category/3/102100112?level=2" ,"유제품/냉장/냉동"],
            ["https://store.kakao.com/category/3/102100118?level=2" , "유제품/냉장/냉동"],
            ["https://store.kakao.com/category/3/102100111?level=2", "유제품/냉장/냉동"],

            ["https://store.kakao.com/category/3/102109?level=1", "제과/빵"],

            [ "https://store.kakao.com/category/3/102100101?level=2", "면류/즉석식품/양념/오일"],
            [ "https://store.kakao.com/category/3/102100103?level=2", "면류/즉석식품/양념/오일"],
            [ "https://store.kakao.com/category/3/102100104?level=2", "면류/즉석식품/양념/오일"],
            [ "https://store.kakao.com/category/3/102100105?level=2", "면류/즉석식품/양념/오일"],
            [ "https://store.kakao.com/category/3/102100109?level=2", "면류/즉석식품/양념/오일"],
            [ "https://store.kakao.com/category/3/102100111?level=2", "면류/즉석식품/양념/오일"],
            [ "https://store.kakao.com/category/3/102100110?level=2", "면류/즉석식품/양념/오일"],
            [ "https://store.kakao.com/category/3/102100141?level=2", "면류/즉석식품/양념/오일"],
            [ "https://store.kakao.com/category/3/102100124103?level=3", "면류/즉석식품/양념/오일"],
            [ "https://store.kakao.com/category/3/102104116?level=2", "면류/즉석식품/양념/오일"],

            [ "https://store.kakao.com/category/3/102104107?level=2", "쌀/잡곡"],
            [ "https://store.kakao.com/category/3/102100119?level=2", "쌀/잡곡"],
            [ "https://store.kakao.com/category/3/102104115?level=2", "쌀/잡곡"],
            [ "https://store.kakao.com/category/3/102104129?level=2", "쌀/잡곡"],

            [ "https://store.kakao.com/category/3/102101?level=1", "생수/음료/커피"]
        ]

        self.cnt = 0
    
    def start_crwal(self):
        


        soup=""
        for site in self.siteList:
            self.driver.get(site[0])
            time.sleep(1)
            self.driver.find_element_by_xpath("/html/body/fu-app-root/fu-wrapper/div/div/fu-pw-category-result/div/div/cu-pagination-list/div/div[1]/div[1]/input").click()
            time.sleep(1)
            html = self.driver.page_source
            soup = BeautifulSoup(html)
            self.getData(soup, site[1])
            time.sleep(2)
            while True:
                try:
                    for i in range(4):
                        self.driver.find_element_by_xpath("/html/body/fu-app-root/fu-wrapper/div/div/fu-pw-category-result/div/div/cu-pagination-list/div/div[2]/div/button[{}]".format(str(1+i))).click()
                        time.sleep(2)
                        html = self.driver.page_source
                        soup = BeautifulSoup(html)
                        a_cnt = self.getData(soup, site[1])
                        if a_cnt == "duplicate":
                            break
                        time.sleep(2)
                except Exception as e:
                    break
                try:
                    self.driver.find_element_by_xpath("/html/body/fu-app-root/fu-wrapper/div/div/fu-pw-category-result/div/div/cu-pagination-list/div/div[3]/button[2]").click()
                    time.sleep(2)
                    html = self.driver.page_source
                    soup = BeautifulSoup(html)
                    print("????????????????????",site[1])
                    a_cnt = self.getData(soup, site[1])
                    if a_cnt == "duplicate": break
                    time.sleep(2)
                except Exception as e:
                    break

            print(site[0], "정상종료")

    def getData(self, soup, cat):
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
                price = int(re.sub(r"[^0-9]", "", price))
                # try:
                purchase = item.select("li > fu-view-product > div > span > a > div > span.other_info > em > span")
                purch=list(purchase)
                # print(type(purchase),purchase, purchase[1])
                try:
                    purch = int(re.sub(r"[^0-9]", "", str(purch[1])))
                except Exception as e:
                    purch =0
                print("imgSrc : ", imgSrc)
                print("prdName : ", prdName)
                print("webUrl : ", webUrl)
                print("price : ", type(price), price)
                print("purchase : ", purch)
                print("cat :", cat)
                print("=====================================e")
                data = {}
                data["imgSrc" ] =imgSrc
                data["prdName" ] = prdName
                data["webUrl" ] = webUrl
                data["price"] = price
                data["purchase"]  = int(purch)
                data["cat"] = cat
                self.pushData(data)
        return cnt

    def pushData(self, data):
        sql = "insert into kko_product(imgsrc, prdname, weburl, purchase, cat, price) values (%s, %s, %s, %s, %s, %s)"
        print(data)
        self.cur.execute(sql, (data["imgSrc"],data["prdName"] , data["webUrl"],data["purchase"] , data["cat"] ,data["price"]))
        self.con.commit()
            
    




    


__main__()