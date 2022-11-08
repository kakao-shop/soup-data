import pymysql
from pymongo import MongoClient


def __main__ ():
    trigger = NormScore()
    siteList = ["11st_product", "kko_product", "homeplus_product"]
    for site in siteList:
        trigger.startNorm(site) # 트리거


class NormScore:
    def __init__(self):
        self.client =  MongoClient('203.255.92.141:27017', connect=False)
        self.con = pymysql.connect(host='localhost', user='root', password='whdgns1002@',
                       db='product_test', charset='utf8')
        self.cur = self.con.cursor()
        self.cnt = 0
        self.data = {}
   
    def startNorm(self,site):
        print("start : ", site)
        sql = "select cat, max(purchase) from {} group by cat".format(site)
        sql2 = "insert into integration_product values(%d,%d,%d,%d,%d,%d,%d,%d)".format(site)
        self.cur.execute(sql)
        
        data =  self.cur.fetchall()
        print(data)
        for i in data:
            if i[1]==0:continue
            sql = "update {0} set {1}.score =purchase*%s where cat=%s".format(site,site)
            self.cur.execute(sql, ( 1/i[1],i[0]))
            self.con.commit()
    
            
    




    


__main__()