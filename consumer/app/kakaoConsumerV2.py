from ElasticsearchAPI import ElaAPI
import pprint as ppr
import json
from json import loads
from datetime import datetime
from kafka import KafkaConsumer 
import RuleBaseClassifier
import time
from elasticsearch import Elasticsearch, helpers

 

 
CatAndSubcat = {}
CatAndSubcat["과일"]=[    "감/홍시","사과","귤","포도","열대과일","견과/밤","키위","배","토마토",
"자몽","아보카도","바나나","기타만감류","메론","오렌지","레몬/라임","무화과",
"베리류","파인애플","수박","딸기","기타과일","견과/밤/대추"]

CatAndSubcat["채소"]=[
    "마/우엉","무/열무","토마토","버섯","배추/절임배추","샐러드","샐러드채소","감자",
"호박","나물","옥수수","고추","양파","파프리카","당근","인삼/더덕/약선재료","오이",
"반찬채소","쌈채소","쪽파","브로콜리","연근","생강","가지","피망",
"양상추","얼갈이","토란","아스파라거스","기타채소","대파"]

CatAndSubcat["축산"]=[
"가공육","돼지고기","소고기","계란/알류","수입육","닭가슴살","닭","한우",
"기타정육","기타축산","오리고기"]


CatAndSubcat["수산/건어물"]=[    "건어물","김/파래김","어패류","새우","갑각류","구색선어","오징어",
"갈치/삼치/고등어","문어","알/해삼","쭈꾸미","연어/참치","가자미","동태/명태",
"기타수산","낙지"]

CatAndSubcat["쌀/잡곡"] =[    "쌀","잡곡","현미","흑미","견과","건조식품","건조과일","깨",
"콩","조","유기농","씨앗"]

CatAndSubcat["제과/빵"]=[
"초콜릿","과자","쿠키","시리얼","커피","튀김","빵","간식류소시지","떡","아이스크림"
,"캔디","소스"]

CatAndSubcat["생수/음료"]=[
    "커피","건강식품","탄산","차","과일/야채음료","생수/탄산수"
,"기타음료","코코아/핫초코","전통음료","꿀","이온음료"
]

CatAndSubcat["냉장/냉동식품"]=[
"김치/젓갈","밀키트","면류","요거트/요구르트","국/탕/찜","만두","반찬/절임류","아이스크림"
,"오일/기름","볶음/구이","우유","돈까스/너겟/치킨","과일/야채음료","두부/유부"
,"맛집","어묵/유부/크래미","피자/핫도그","베이컨/소시지","냉동과일"
,"안주/전류","치즈/버터","볶음밥/덮밥/죽","떡볶이/떡사리","젤리/푸딩"
,"감자튀김/치즈스틱","떡갈비/함박스테이크","닭가슴살","두유"
,"계란/알류","튀김류","샌드위치/버거","기타식품","베이커리"]

CatAndSubcat["즉석식품/양념"]=[
"국/탕/찜","즉석밥","안주/전류","죽/스프","카레/짜장","소금/설탕","스팸/햄"
,"도시락","참치캔","꿀","라면","통조림","소스","오일/기름","밀키트","고춧가루/참깨"
,"다시다/미원","볶음/구이","사리얼","고추장/된장/간장","닭가슴살","만두","맛술/액젓"
,"식초/물엿","돈까스/너겟/치킨","제빵믹스","기타즉석","피자/핫도그","어묵/유부/크래미"
,"떡볶이/떡사리","시럽/잼","튀김류","케찹/마요네즈","떡갈비/함박스테이크","건어물"
,"베이컨/소시지","드레싱","새우","문어","쭈꾸미"]


es = Elasticsearch(hosts="localhost", port=9200)

client = ElaAPI()


consumer=KafkaConsumer("kakao-test", 
                        bootstrap_servers=['localhost:9092'],
                        # bootstrap_servers=['127.0.0.1:9092'], 
                        auto_offset_reset="earliest",
                        auto_commit_interval_ms=10,
                        enable_auto_commit=True, 
                        group_id='kakao-group', 
                        value_deserializer=lambda x: loads(x.decode('utf-8')), 
                        consumer_timeout_ms=1000 
            )
 
ruleBaseClassifier = RuleBaseClassifier.Classifier()
def normalize(indexName):
        print("start normalize")
        for cat in CatAndSubcat:
            for subcat in CatAndSubcat[cat]:
                time.sleep(0.2)
                try:
                    res = es.search(
                        index=indexName, 
                        
                        body={
                            "size": 1,
                            "query":{
                                    "bool": {
                                        "must":[
                                            {"match":{"site":"카카오 쇼핑" }},
                                        {"match":{"cat":cat}},
                                        {"match":{"subcat":subcat}}]
                                    }
                                },
                            "aggs": {
                                "test": {
                                "max": { "field": "purchase"}
                                }
                        }
                        }
                    )
                    print("1번 응답", res["aggregations"]["test"]["value"])
                    print(subcat)
                    time.sleep(0.2)
                    # 업데이트 쿼리
                    res2= es.update_by_query(
                        index=indexName,  
                        body = {
                    "query" :{
                        "bool": {
                                "must":[
                                {"match": {"site": "카카오 쇼핑"}},
                                {"match":{"cat":cat}},
                                { "match":{"subcat":subcat}}
                        ]
                        }
                    }, 
                    "script": {
                    "source":"ctx._source.score =ctx._source.purchase * {};".format(str(1/int(res["aggregations"]["test"]["value"]))),
                    "lang": "painless"
                    }  }
                    )
                    # print("res2", res2)
                except Exception as e:
                    print("구매 이력이 없으면 오류 ", e)
        print("end normalize")



def deleteIndex(deleteIndexName):
    es.indices.delete(index=deleteIndexName, ignore=[400, 404])


def classifier(data):
    subcat = ""
    if data["cat"] =="축산":
        subcat =ruleBaseClassifier.meat(data["prdName"])
    elif data["cat"] =="채소":
        subcat =ruleBaseClassifier.veget(data["prdName"])
    elif data["cat"] =="생수/음료":
        subcat =ruleBaseClassifier.water(data["prdName"])
    elif data["cat"] =="냉장/냉동식품":
        subcat =ruleBaseClassifier.mik_ref(data["prdName"])
    elif data["cat"] =="즉석식품/양념":
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
    if data[-1] == "0":
        data[-1]="00"
    if len(data[-2]) == 1:
        data[-2]= "0" + data[-2]
    
    # print(data)
    return "-".join(data)



def __main__():
    es_index = ""
    print("start kakao")
    res = ""
    while True:
        if res != "": break
        data_list = []
        for message in consumer:
            consumer.commit()
            docs = {}
            try:
                value=message.value
            
                if "finish" in value:
                    print("????")
                    res = "test"
                    time.sleep(1)
                    break
                data = value["data"]
                docs["_index"]= data["index"]
                data['subcat']=classifier(data)
                data["site"] ="카카오 쇼핑"
                data["score"] =float(0)
                docs["_source"] = data
                es_index=data["index"]

                data_list.append(docs)
            except Exception as e:
                print(value)
                print("consumer error : " , e)
        try:
            if data_list ==[]: 
                print("continue")
                continue
            client.dataInsert(data_list)
            print("success insert")

        except Exception as e  :
            print("insert error", e)
            continue
    print(es_index)
    normalize(es_index)
    deleteIndexName = beforeTime(es_index)
    print(deleteIndexName)
    deleteIndex(deleteIndexName)


__main__()


