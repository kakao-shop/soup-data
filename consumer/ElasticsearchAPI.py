from elasticsearch import Elasticsearch, helpers
import json


es = Elasticsearch(hosts="127.0.0.1", port=9200)
class ElaAPI:
    
       # 객체 생성
    def srvHealthCheck(self):
        health = es.cluster.health()
        print (health)

    def allIndex(self):
        print (es.cat.indices())

    def dataInsert(self, docs):
        # ===============
        # 데이터 삽입
        # ===============
        helpers.bulk(es, docs)

    def searchAll(self, index):
        res = es.search(
            index = index, 
            body = {
                "query":{"match_all":{}}
            }
        )
        print (json.dumps(res, ensure_ascii=False, indent=4))


    def createIndex(self, date):
        # ===============
        # 인덱스 생성
        # ===============
        index = "product-" + date
  
        if es.indices.exists(index=index):
            pass
        else:
            es.indices.create(
            index = index,
            body = {
                "settings": {
                    "analysis": {
                        "analyzer": {
                            "default": {
                                "type": "nori"
                            }
                        }
                    }
                },
                "mappings": {
                
                        "properties": {
                            "imgSrc":    {"type": "text"},
                            "prdName": {"type": "text"},
                            "webUrl":    {"type": "text"},
                            "purchase":    {"type": "text"},
                            "subcat":   {"type": "text"},
                            "site":     {"type": "text"},
                            "cat":   {"type": "text"},
                            "price":     {"type": "integer"},
                            "score":   {"type": "double"}
                            }
                        
                    }
                }
            )