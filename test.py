from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017', authSource='admin')
homeplus = client["DATAETL"]['Kakao']


for i in homeplus.find({"subcat":"감/홍시"}).sort([("purchase",-1)]).limit(10):
    print(i)
# for i in homeplus.find().sort([("purchase",-1)]).limit(1): 
#     # print(i["purchase"])
#     homeplus.update_many({},[
#     {"$set":
#         {"score":
#             {"$multiply":
#                 ["$purchase", 1/i["purchase"]] 
#             }
#         }
#         }]
#     )
#     print("?")
