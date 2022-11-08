from kafka import KafkaConsumer 
from json import loads 
import time
import datetime
import joblib
from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import RuleBaseClassifier
# meat : 축산
# veget : 채소
# water : 생수/음료/커피
# mik_ref : 유제품/냉장/냉동
# retro : 면류/양념/오일
# ssal : 쌀/잡곡
# pastry : 제과/빵
# fish : 수산/건어물
# fruit : 과일
ruleBaseClassifier = RuleBaseClassifier.Classifier()
cvect = CountVectorizer()

client = MongoClient('mongodb://127.0.0.1:27017', authSource='admin')
homeplus = client["DATAETL"]['Street']
consumer=KafkaConsumer("11st-test", 
                        bootstrap_servers=['127.0.0.1:9092'], 
                        auto_offset_reset="earliest",
                        enable_auto_commit=True, 
                        group_id='test-group', 
                        value_deserializer=lambda x: loads(x.decode('utf-8')), 
                        consumer_timeout_ms=1000 
            )
# DTM(document-term matrix)
# 피치 가져오기



start = time.time() # 현재 시간
print("START= ", start)
while True:
    data_list = []
    cnt = 0
    for message in consumer:
        print(cnt)
        value=message.value
        print(value)
        data = value["data"]
        data['subcat']=""
        if data["cat"] =="축산":
            data['subcat']=ruleBaseClassifier.meat(data["prdName"])
        elif data["cat"] =="채소":
            data['subcat']=ruleBaseClassifier.veget(data["prdName"])
        elif data["cat"] =="생수/음료/커피":
            data['subcat']=ruleBaseClassifier.water(data["prdName"])
        elif data["cat"] =="유제품/냉장/냉동":
            data['subcat']=ruleBaseClassifier.mik_ref(data["prdName"])
        elif data["cat"] =="면류/양념/오일":
            data['subcat']=ruleBaseClassifier.retro(data["prdName"])
        elif data["cat"] =="쌀/잡곡":
            data['subcat']=ruleBaseClassifier.ssal(data["prdName"])
        elif data["cat"] =="제과/빵":
            data['subcat']=ruleBaseClassifier.pastry(data["prdName"])
        elif data["cat"] =="수산/건어물":
            data['subcat']=ruleBaseClassifier.fish(data["prdName"])
        elif data["cat"] =="과일":
            data['subcat']=ruleBaseClassifier.fruit(data["prdName"])
        data_list.append(data)
        print(data)
    try:
        homeplus.insert_many(data_list)
        print("?")
    except:
        continue