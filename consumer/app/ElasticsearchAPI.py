from elasticsearch import Elasticsearch, helpers
import json
import os

es_host = os.environ["ELASTICSEARCH_HOST"]
es_port = os.environ["ELASTICSEARCH_PORT"]
es = Elasticsearch(hosts=es_host, port=es_port)
class ElaAPI:

    def dataInsert(self, docs):
        # ===============
        # 데이터 삽입
        # ===============
        helpers.bulk(es, docs)
    def dataInsert(self, docs):
        # ===============
        # 데이터 삽입
        # ===============
        helpers.bulk(es, docs)
