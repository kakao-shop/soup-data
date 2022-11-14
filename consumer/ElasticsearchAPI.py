from elasticsearch import Elasticsearch, helpers
import json


es = Elasticsearch(hosts="127.0.0.1", port=9200)
class ElaAPI:

    def dataInsert(self, docs):
        # ===============
        # 데이터 삽입
        # ===============
        helpers.bulk(es, docs)
