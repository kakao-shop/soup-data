from pymongo import MongoClient
import pymysql

client = MongoClient('mongodb://127.0.0.1:27017', authSource='admin')
homeplus = client["DATAETL"]['Homeplus']
con = pymysql.connect(host='localhost', user='root', password='whdgns1002@',
                       db='test', charset='utf8')
cur = con.cursor()
sql = "select searchkeyword,count from keywordlog where userid = 1 order by count desc limit 3"

cur.execute(sql)
result = cur.fetchall()
print(result)
for i in ["젤리","치킨","과자"]:
    search = "/" + i[0] + "/"
    for i in homeplus.find({"prdName":{ "$regex": i[0] }}).sort([("score",1)]).limit(1): 
        for j in homeplus.find({"subcat":{ "$regex": i["subcat"] }}).sort([("score",1)]).limit(2):
            print(j)




# for i in homeplus.find({"subcat":"감/홍시"}).sort([("purchase",-1)]).limit(10):
#     print(i)


# for i in homeplus.find().sort([("purchase",-1)]).limit(1): 
#             homeplus.update_many({},[
#             {"$set":
#                 {"score":
#                     {"$multiply":
#                         ["$purchase", 1/i["purchase"]] 
#                     }
#                 }
#                 }]
#             )