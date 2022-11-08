from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# import pymysql

# def __main__ ():
#     trigger = NormScore()
#     siteList = ["11st_product", "kko_product", "homeplus_product"]
#     for site in siteList:
#         trigger.startNorm(site) # 트리거


# class NormScore:
#     def __init__(self):
#         self.con = pymysql.connect(host='localhost', user='root', password='whdgns1002@',
#                        db='product_test', charset='utf8')
#         self.cur = self.con.cursor()
#         self.tfidf_vectorizer = TfidfVectorizer()
#         self.data = {}
   
#     def startNorm(self,site):
#         print("start : ", site)
#         sql = "select cat, max(purchase) from {} group by cat".format(site)
#         self.cur.execute(sql)
        
#         data =  self.cur.fetchall()
#         print(data)
#         for i in data:
#             if i[1]==0:continue
#             sql = "update {0} set {1}.score =purchase*%s where cat=%s".format(site,site)
#             self.cur.execute(sql, ( 1/i[1],i[0]))
#             self.con.commit()
    
#     def cos(self, sentences):
#         # 문장 벡터화 하기(사전 만들기)
#         tfidf_matrix = self.tfidf_vectorizer.fit_transform(sentences)

#         ### 코사인 유사도 ###
#         # 첫 번째와 두 번째 문장 비교
#         cos_similar = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
#         print("코사인 유사도 측정")
#         print(cos_similar)
        
            
# __main__()




tfidf_vectorizer = TfidfVectorizer()

def cos(sentences):
    # 문장 벡터화 하기(사전 만들기)
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

    ### 코사인 유사도 ###
    # 첫 번째와 두 번째 문장 비교
    cos_similar = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    print("코사인 유사도 측정")
    print(cos_similar)

sentences = ("감자 농사꾼과 유기농 재배",  "농사")
# sentences = ("우유",        "유제품")





# sentences = ("가공식품", "식품")
# sentences = ("우유",        "유제품")
cos(sentences)

