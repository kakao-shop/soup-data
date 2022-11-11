from ElasticsearchAPI import ElaAPI
import pprint as ppr
import json
from json import loads
from datetime import datetime
from kafka import KafkaConsumer 
import RuleBaseClassifier
import time
from elasticsearch import Elasticsearch, helpers

 
es = Elasticsearch(hosts="127.0.0.1", port=9200)


client = ElaAPI()
index_date = datetime.now().strftime('%Y-%m-%d-%H-%M')
 
 
consumer=KafkaConsumer("street-test", 
                        bootstrap_servers=['127.0.0.1:9092'], 
                        auto_offset_reset="earliest",
                        enable_auto_commit=True, 
                        group_id='test-group', 
                        value_deserializer=lambda x: loads(x.decode('utf-8')), 
                        consumer_timeout_ms=1000 
            )
 
ruleBaseClassifier = RuleBaseClassifier.Classifier()
def normalize(indexName):
        print("start normalize")
        for subcat in ["과일", "채소", "채소", "축산","수산/건어물", "유제품/냉장/냉동", "제과/빵" , "면류/즉석식품/양념/오일", "쌀/잡곡", "생수/음료/커피"]:
            try:
                res = es.search(
                    index=indexName, 
                    
                    body={
                        "size": 0,
                        "query":{"match":{"site":"street" },
                                "match":{"cat":subcat}},
                        "aggs": {
                            "test": {
                            "max": { "field": "purchase"}
                            }
                    }
                    }
                )
                print(res)
                print(res["aggregations"]["test"]["value"])
                print(subcat)
                # 업데이트 쿼리
                res2= es.update_by_query(
                    index=indexName,  
                    body = {
                "query" :{
                    "bool": {
                            "must":[
                            {"match": {"site": "street"}},
                            { "match":{"cat":subcat}}
                    ]
                    }
                }, 
                "script": {
                "source":"ctx._source.score =ctx._source.score + {};".format(str(int(res["aggregations"]["test"]["value"]))),
                "lang": "painless"
                }  }
                )
                print("res2", res2)
            except Exception as e:
                print(e)
        print("end normalize")




def classifier(data):
    subcat = ""
    if data["cat"] =="축산":
        subcat =ruleBaseClassifier.meat(data["prdName"])
    elif data["cat"] =="채소":
        subcat =ruleBaseClassifier.veget(data["prdName"])
    elif data["cat"] =="생수/음료/커피":
        subcat =ruleBaseClassifier.water(data["prdName"])
    elif data["cat"] =="유제품/냉장/냉동":
        subcat =ruleBaseClassifier.mik_ref(data["prdName"])
    elif data["cat"] =="면류/즉석식품/양념/오일":
        subcat =ruleBaseClassifier.retro(data["prdName"])
    elif data["cat"] =="쌀/잡곡":
        subcat =ruleBaseClassifier.ssal(data["prdName"])
    elif data["cat"] =="제과/빵":
        subcat =ruleBaseClassifier.pastry(data["prdName"])
    elif data["cat"] =="수산/건어물":
        subcat =ruleBaseClassifier.fish(data["prdName"])
    elif data["cat"] =="과일":
        subcat =ruleBaseClassifier.fruit(data["prdName"])
 
    return subcat
 
es_index = ""
print("start street")
res = ""
while True:
    if res != "": break
    data_list = []
    cnt = 0
    for message in consumer:
        docs = {}

        value=message.value
        
        # print(value)
        if "index" in value:   
            es_index =value["index"]
            print("es_index", es_index) 
            time.sleep(1)
            continue
        elif "finish" in value:
            res += 1
            break
        docs["_index"]= es_index
        data = value["data"]
        data['subcat']=classifier(data)
        data["site"] ="street"
        data["score"] =float(0)
        docs["_source"] = data
        data_list.append(docs)
 
    print(data_list)
    try:
        client.dataInsert(data_list)
        print("success insert")
    except:
        continue
normalize(es_index)
import datetime
def beforeTime(time):
    data  = time.split("-")
    minute = int(data[-1])
    hour = int(data[-2]) 
    remain = minute - 30
    if remain >= 0:
        data[-2], data[-1] = str(hour), str(remain)
    else:
        if hour == 0:
            data[-2], data[-1] = str(23), str(60+remain)
        else:
            data[-2], data[-1] =  str(hour-1), str(60+remain)
    
    return "-".join(data)
deleteIndexName = beforeTime(es_index)
es.indices.delete(index=deleteIndexName, ignore=[400, 404])




