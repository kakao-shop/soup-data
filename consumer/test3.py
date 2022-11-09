from ElasticsearchAPI import ElaAPI
import pprint as ppr
import json
from json import loads
from datetime import datetime
from kafka import KafkaConsumer 
import RuleBaseClassifier

import time



            
client = ElaAPI()
index_date = datetime.now().strftime('%Y-%m-%d-%H-%M')


consumer=KafkaConsumer("home-test", 
                        bootstrap_servers=['127.0.0.1:9092'], 
                        auto_offset_reset="earliest",
                        enable_auto_commit=True, 
                        group_id='test-group', 
                        value_deserializer=lambda x: loads(x.decode('utf-8')), 
                        consumer_timeout_ms=1000 
            )

ruleBaseClassifier = RuleBaseClassifier.Classifier()

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
print("start home")
while True:
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
        docs["_index"]= es_index
        data = value["data"]
        data['subcat']=classifier(data)
        data["site"] ="home"
        data["score"] =float(0)
        docs["_source"] = data
        data_list.append(docs)

    print(data_list)
    try:
        client.dataInsert(data_list)
        print("success insert")
    except:
        continue





