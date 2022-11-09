# from datetime import datetime
# data = {}
# data["index"]="product-"+datetime.now().strftime('%Y-%m-%d-%H-%M')
# print(data)
from elasticsearch import Elasticsearch, helpers
import json


es = Elasticsearch(hosts="127.0.0.1", port=9200)

for cat in ['과일','채소','쌀/잡곡', '축산', '수산/건어물','유제품/냉장/냉동','제과/빵','면류/즉석식품/양념/오일','생수/음료/커피']:
    try:
        res = es.search(
            index="product-2022-11-10-01-41", 
            
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
        print("max",res["aggregations"]["test"]["value"])
        print("{0:.7f}".format(1/int(res["aggregations"]["test"]["value"])))
        # 업데이트 쿼리
        res2= es.update_by_query(
            index="product-2022-11-10-01-41",  
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
        "source":"ctx._source.score =ctx._source.purchase *{0:.7f};".format(1/int(res["aggregations"]["test"]["value"])),
        "lang": "painless"
        }  }
        )
        print("res2", res2)
    except Exception as e:
        print(e)




# 검색쿼리
# res = es.search(
#       index="product-2022-11-09-23-01", 
      
#        body={
#         "size": 0,
#         "query":{"match":{"site":"street" },
#                  "match":{"cat":"과일"}},
#         "aggs": {
#             "test": {
#             "max": { "field": "purchase"}
#             }
#        }
#     }
# )
# print(int(res["aggregations"]["test"]["value"]))
# # 업데이트 쿼리
# res2= es.update_by_query(
#     index='product-2022-11-10-00-30',  
#     body = {
#   "query" :{
#     "bool": {
#             "must":[
#               {"match": {"site": "street"}},
#               { "match":{"subcat": "사과"}}
#       ]
#     }
#   }, 
#   "script": {
#   "source":"ctx._source.score =ctx._source.score + {};".format(str(int(res["aggregations"]["test"]["value"]))),
#   "lang": "painless"
#   }  }
# )
# print(res2)


# es.indices.create(
#             index = "type-test-02",
#             body = {
#                 "settings": {
#                     "analysis": {
#                         "analyzer": {
#                             "content": {
#                                 "type": "custom",
#                                 "tokenizer": "nori_tokenizer",
#                                 "decompound_mode": "mixed"
#                                 }
      
#                         }
#                     }
#                 },
#                 "mappings": {
                
#                         "properties": {
#                             "imgSrc":    {"type": "text"},
#                             "prdName": {"type": "text","analyzer": "content"},
#                             "webUrl":    {"type": "text"},
#                             "purchase":    {"type": "text"},
#                             "subcat":   {"type": "text"},
#                             "site":     {"type": "text"},
#                             "cat":   {"type": "text"},
#                             "price":     {"type": "integer"},
#                             "score":   {"type": "float"}
#                             }
                        
#                     }
#                 }
#             )

# from pymongo import MongoClient
# import pymysql

# client = MongoClient('mongodb://127.0.0.1:27017', authSource='admin')
# homeplus = client["DATAETL"]['Homeplus']
# con = pymysql.connect(host='localhost', user='root', password='whdgns1002@',
#                        db='test', charset='utf8')
# cur = con.cursor()
# sql = "select searchkeyword,count from keywordlog where userid = 1 order by count desc limit 3"

# cur.execute(sql)
# result = cur.fetchall()
# print(result)
# for i in ["젤리","치킨","과자"]:
#     search = "/" + i[0] + "/"
#     for i in homeplus.find({"prdName":{ "$regex": i[0] }}).sort([("score",1)]).limit(1): 
#         for j in homeplus.find({"subcat":{ "$regex": i["subcat"] }}).sort([("score",1)]).limit(2):
#             print(j)




# # for i in homeplus.find({"subcat":"감/홍시"}).sort([("purchase",-1)]).limit(10):
# #     print(i)


# # for i in homeplus.find().sort([("purchase",-1)]).limit(1): 
# #             homeplus.update_many({},[
# #             {"$set":
# #                 {"score":
# #                     {"$multiply":
# #                         ["$purchase", 1/i["purchase"]] 
# #                     }
# #                 }
# #                 }]
# #             )