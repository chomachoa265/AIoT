from flask import Flask, render_template, jsonify;
import os
import json
import pymysql
from  pandas import DataFrame as df
import pandas as pd 
import numpy as np
from sklearn.svm import SVC

myserver ="localhost"
myuser="test123"
mypassword="test123"
mydb="aiotdb"

app = Flask(__name__)

@app.route('/noAI')
def noAI():
    return render_template("indexNoAI.html")

@app.route('/AI')
def AI():
    return render_template("indexAI.html")

@app.route('/getData')
def getData():
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    # cursor will return dictionary type
    c = conn.cursor(pymysql.cursors.DictCursor) 
    c.execute("SELECT time, value, status FROM sensors")
    data = c.fetchall()
    return jsonify(data)

@app.route('/getPredict')
def getPredict():
    import pickle
    import gzip
    debug =0

    # part.2 section
    #=================read Data=================#
    # data=pd.read_csv("./dataset/trainN.csv")        #載入traning.csv至data

    # X=data['value'].values.reshape(-1,1)
    # Y=data['status'].values.reshape(-1,1)

    #=================read Data End=================#
    #

    ############## Part 3. 才使用 ###############
    with gzip.open('./models/myAI.pkz', 'r') as f:
        model = pickle.load(f)
    #############################################
    # model=SVC()           #支持向量機
    # model.fit(X,Y)

    # os.makedirs("./models", exist_ok=True)
    # with gzip.GzipFile('./models/myAI.pkz', 'w') as f:
    #     pickle.dump(model, f)

        
    import pymysql.cursors
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    c = conn.cursor()
    if debug:
        input("pause.. conn.cursor() ok.......")

    #====== 執行 MySQL 查詢指令 ======#
    c.execute("SELECT * FROM sensors")

    #====== 取回所有查詢結果 ======#
    results = c.fetchall()
    if debug:
        input("pause ....select ok..........")

    test_df = df(list(results),columns=['id','time','value','temp','humi','status'])
    if debug:
        input("pause..  show original one above (NOT correct).......")

    testX=test_df['value'].values.reshape(-1,1)
    testY=model.predict(testX)
    print(model.score(testX,testY))
    test_df['status']=testY

    if debug:
        input("pause.. now show correct one above.......")



    ##Example 2 ## write back mysql ###############
    ## make all status =0
    c.execute('update sensors set status=0 where value>0')

    ## choose status ==1 have their id available
    id_list=list(test_df[test_df['status']==1].id)
    print(id_list)
                
    for _id in id_list:
        #print('update light set status=1 where id=='+str(_id))
        c.execute('update sensors set status=1 where id='+str(_id))

    conn.commit()

    if debug:
        input("pause ....update ok..........")

    ######### cursor close, conn close
    c.close()
    conn.close()

    return "OK"


    



# @app.route('/media/<path:repoID>/<path:type>/<path:filename>')
# def media(repoID, type, filename):



if __name__ == '__main__':
    app.run(debug=True)


    