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

def __main__ ():
    
    a = len(sys.argv)  
    st11_crawling().start_crwal() # 트리거

#--------------크롤링 시작 ------------------------------   

class st11_crawling:
    def __init__(self):
        # self.host = '127.0.0.1'
        # self.kafka_port = '9092'
        self.driver_path = "./chromedriver.exe"
        #  C:/Users/kjh19/OneDrive/바탕 화면/test/chromedriver.exe // 노트북
        self.con = pymysql.connect(host='localhost', user='root', password='whdgns1002@',
                       db='product_test', charset='utf8')
        self.cur = self.con.cursor()
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('--disable-dev-shm-usage') # 서버컴 전용 옵션
        self.chrome_options.add_argument('window-size=1280,1000')
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=self.chrome_options)
        self.category = []
        self.titleList = []
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
        print(len(list(set(self.category))))
        print(set(self.category))


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
                        if purchases == "추천상품":
                            purchases = "0"
                        else:
                            print("purchases",purchases)

                        data = {}
                        data["imgSrc" ] =img_src
                        data["prdName" ] = name_url["content_name"]
                        data["webUrl" ] = "https://front.homeplus.co.kr" +web_url
                        data["price"] = int(re.sub(r"[^0-9]", "", name_url["last_discount_price"]))  
                        data["purchase"]  = int(re.sub(r"[^0-9]", "", purchases))
                        data["cat"] = categoryName
                        if categoryName == "채소류":
                            data["cat"] = "채소"
                        elif categoryName == "과일/견과":
                            data["cat"] = "과일"
                        elif categoryName == "축산물":
                            data["cat"] = "축산"
                        elif categoryName in [ "차/전통음료", "커피", "전통주", "생수/음료"]:
                            data["cat"] = "물/음료"
                        elif categoryName == "우유/두유":
                            data["cat"] = "유제품"
                        elif categoryName == "라면/즉석식품":
                            data["cat"] = "면"
                        elif categoryName == "쌀/잡곡류":
                            data["cat"] = "쌀/잡곡"
                        elif categoryName == "수산물":
                            data["cat"] = "수산/건어물"
                        elif categoryName == "과자/간식":
                            data["cat"] = "제과"
                        else: continue
                        self.pushData(data)


                        # url = data.select_one("li > div > a")["href"]
                        # print(url)
                    except Exception as e:
                        print(e, " ???? ")
                    #print(cnt, data)
                    print("=====================================e")
            
        return cnt

    def pushData(self, data):
        sql = "insert into 11st_product(imgsrc, prdname, weburl, purchase, cat, price) values (%s, %s, %s, %s, %s, %s)"
        print(data)
        self.cur.execute(sql, (data["imgSrc"],data["prdName"] , data["webUrl"],data["purchase"] , data["cat"] ,data["price"]))
        self.con.commit()

       # 1번 #mdPrd > div.viewtype3.list_htype3.ui_templateContent > div.virtual-wrap > div > ul
       # 2번 #mdPrd > div.viewtype3.list_htype3.ui_templateContent > div.virtual-wrap > div > ul

       # 1번 li태그  # /html/body/div[2]/div[3]/div/div/div[2]/div[2]/div[1]/div/ul
       # 2번 li태그    /html/body/div[2]/div[3]/div/div/div[2]/div[2]/div[3]/div/ul/li[1]
       # 식품 종류 태그 
       # /html/body/div[2]/div[3]/div/div/div[2]/div[1]/div/ul/li[1] ~[5]
       
        


            
    




    


__main__()