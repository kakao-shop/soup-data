import hashlib
from elasticsearch import Elasticsearch
es = Elasticsearch(["192.168.56.101:9200","192.168.56.102:9200","192.168.56.103:9200"])
dict_of_duplicate_docs = {}
# 다음 줄은 문서의 중복 여부를
# 판단하는 데 사용될 필드를 정의합니다.
keys_to_include_in_hash = ["name"]
# 현재 검색/스크롤에 의해 반환된 문서를 처리합니다.
def populate_dict_of_duplicate_docs(hits):
    for item in hits:
        combined_key = ""
        for mykey in keys_to_include_in_hash:
            combined_key += str(item['_source'][mykey])
        _id = item["_id"]
        hashval = hashlib.md5(combined_key.encode('utf-8')).digest()
        # hashval이 새로운 것이라면
        # dict_of_duplicate_docs에 새 키를 생성하며
        # 이 키에는 빈 어레이의 값이 할당됩니다.
        # 그런 다음 _id를 즉시 어레이로 푸시합니다.
        # hashval이 이미 존재한다면
        # 새로운 _id를 기존 어레이로 푸시합니다.
        dict_of_duplicate_docs.setdefault(hashval, []).append(_id)
# 인덱스의 모든 문서를 반복하고
# dict_of_duplicate_docs 데이터 구조를 채웁니다.
def scroll_over_all_docs():
    data = es.search(index="dedup2", scroll='1m',  body={"query": {"match_all": {}},
                                                        "sort":[{"cnt":{"order":"desc"}}]})
    # 스크롤 ID를 가져옵니다.
    sid = data['_scroll_id']
    scroll_size = len(data['hits']['hits'])
    # 스크롤하기 전에 적중 결과의 현재 배치를 처리합니다.
    populate_dict_of_duplicate_docs(data['hits']['hits'])
    while scroll_size > 0:
        data = es.scroll(scroll_id=sid, scroll='2m')
        # 적중 결과의 현재 배치를 처리합니다.
        populate_dict_of_duplicate_docs(data['hits']['hits'])
        # 스크롤 ID를 업데이트합니다.
        sid = data['_scroll_id']
        # 마지막 스크롤에 반환된 결과 수를 가져옵니다.
        scroll_size = len(data['hits']['hits'])
def loop_over_hashes_and_remove_duplicates():
    # 중복 해시가 있는지 확인하기 위해
    # 문서 값의 해시를 검색합니다.
    for hashval, array_of_ids in dict_of_duplicate_docs.items():
      if len(array_of_ids) > 1:
        print("********** Duplicate docs hash=%s **********" % hashval)
        # 현재 hasval에 매핑된 문서를 가져옵니다.
        matching_docs = es.mget(index="dedup2", doc_type="doc", body={"ids": array_of_ids})
        print(array_of_ids)
        print(len(matching_docs['docs']))
        for doc in matching_docs['docs'][1:]:
            
            # 이 예제에서는 중복 문서만 인쇄합니다.
            # 이 코드는 인쇄하는 대신 여기서 중복을
            # 삭제하도록 간단하게 수정할 수 있습니다.
            es.delete_by_query(index="dedup2",
            body = {
                "query" :{
                        "bool": {
                                "must":[
                                {"match": {"_id": doc["_id"]}},
                        ]
                        }
                    }
                })
            print("doc=%s\n" % doc)
def main():
    scroll_over_all_docs()
    loop_over_hashes_and_remove_duplicates()
main()
















# import hashlib
# from elasticsearch import Elasticsearch
# es = Elasticsearch(["localhost:9200"])
# dict_of_duplicate_docs = {}
# # 다음 줄은 문서의 중복 여부를
# # 판단하는 데 사용될 필드를 정의합니다.
# keys_to_include_in_hash = ["CAC", "FTSE", "SMI"]
# # 현재 검색/스크롤에 의해 반환된 문서를 처리합니다.
# def populate_dict_of_duplicate_docs(hits):
#     for item in hits:
#         combined_key = ""
#         for mykey in keys_to_include_in_hash:
#             combined_key += str(item['_source'][mykey])
#         _id = item["_id"]
#         hashval = hashlib.md5(combined_key.encode('utf-8')).digest()
#         # hashval이 새로운 것이라면
#         # dict_of_duplicate_docs에 새 키를 생성하며
#         # 이 키에는 빈 어레이의 값이 할당됩니다.
#         # 그런 다음 _id를 즉시 어레이로 푸시합니다.
#         # hashval이 이미 존재한다면
#         # 새로운 _id를 기존 어레이로 푸시합니다.
#         dict_of_duplicate_docs.setdefault(hashval, []).append(_id)
# # 인덱스의 모든 문서를 반복하고
# # dict_of_duplicate_docs 데이터 구조를 채웁니다.
# def scroll_over_all_docs():
#     data = es.search(index="stocks", scroll='1m',  body={"query": {"match_all": {}}})
#     # 스크롤 ID를 가져옵니다.
#     sid = data['_scroll_id']
#     scroll_size = len(data['hits']['hits'])
#     # 스크롤하기 전에 적중 결과의 현재 배치를 처리합니다.
#     populate_dict_of_duplicate_docs(data['hits']['hits'])
#     while scroll_size > 0:
#         data = es.scroll(scroll_id=sid, scroll='2m')
#         # 적중 결과의 현재 배치를 처리합니다.
#         populate_dict_of_duplicate_docs(data['hits']['hits'])
#         # 스크롤 ID를 업데이트합니다.
#         sid = data['_scroll_id']
#         # 마지막 스크롤에 반환된 결과 수를 가져옵니다.
#         scroll_size = len(data['hits']['hits'])
# def loop_over_hashes_and_remove_duplicates():
#     # 중복 해시가 있는지 확인하기 위해
#     # 문서 값의 해시를 검색합니다.
#     for hashval, array_of_ids in dict_of_duplicate_docs.items():
#       if len(array_of_ids) > 1:
#         print("********** Duplicate docs hash=%s **********" % hashval)
#         # 현재 hasval에 매핑된 문서를 가져옵니다.
#         matching_docs = es.mget(index="stocks", doc_type="doc", body={"ids": array_of_ids})
#         for doc in matching_docs['docs']:
#             # 이 예제에서는 중복 문서만 인쇄합니다.
#             # 이 코드는 인쇄하는 대신 여기서 중복을
#             # 삭제하도록 간단하게 수정할 수 있습니다.
#             print("doc=%s\n" % doc)
# def main():
#     scroll_over_all_docs()
#     loop_over_hashes_and_remove_duplicates()
# main()