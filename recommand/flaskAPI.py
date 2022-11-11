from flask import Flask, jsonify, request
import flask
import joblib
from pymongo import MongoClient
import pymysql
from time import sleep

client = MongoClient('mongodb://127.0.0.1:27017', authSource='admin')
bundledSite = client["DATAETL"]['BundledSite']
con = pymysql.connect(host='localhost', user='root', password='whdgns1002@',
                       db='test', charset='utf8')
cur = con.cursor()



app = Flask(__name__)

@app.route('/')
def main_page():
    return "this page is main page"

    
@app.route('/recommend', methods=["GET"])
def preddict():
   
    params = flask.request.args.getlist("keyword")
    keyword,count = [],[]
    for i in params:
        a,b = i.split(",")
        keyword.append(a); count.append(int(b))
    lenCount = len(count)
    tmp = sum(count)
    cnt =0
    weight = []
    while True:
        re = 0
        weight = []
        for i in range(lenCount):
            re += int((count[i]/tmp)*10)
            weight.append(int((count[i]/tmp)*10))
        if re != 10:
            count[cnt%lenCount]=count[cnt%lenCount] +1
        else: break
        cnt+=1       
    print("weight" , weight)
    print("keyword" , keyword)
    data = {}
    product = []
    for num in range(len(keyword)):
        print("num:",keyword[num])
        search = keyword[num]
        for i in bundledSite.find({"prdName":{ "$regex": search }}).sort([("score",-1)]).limit(1): 
            for j in bundledSite.find({"subcat":{ "$regex": i["subcat"] }}).sort([("score",1)]).limit(weight[num]):
                del j["_id"]
                product.append(j)

                print(j)

    data["product"] = product
    return flask.jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=80)