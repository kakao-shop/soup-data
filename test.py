from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017', authSource='admin')
homeplus = client["DATAETL"]['Homeplus']

print()

for i in homeplus.find().sort([("purchase",-1)]).limit(1): 
    # print(i["purchase"])
    homeplus.update_many({},[
    {"$set":
        {"score":
            {"$multiply":
                ["$purchase", 1/i["purchase"]] 
            }
        }
        }]
    )
    print("?")
# print(homeplus.things.aggregate([{"$sort": [("purchase", -1)]}]))