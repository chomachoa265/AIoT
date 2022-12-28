# Part 1: localhost 呈現 highchart 圖形
XAMPP啟用Apache, Mysql，並新增使用者和資料庫(包含匯入資料表)，使得GetData得到取得資料並顯示在容器(container)內部
<div align='center'>
  <img src="https://github.com/chomachoa265/AIoT/blob/main/homework5/result_assets/part1_addUser.png"/>
  <img src="https://github.com/chomachoa265/AIoT/blob/main/homework5/result_assets/part1_noAIHighcharts.png"/>
</div>

# Part 2: AI Module 與 web 互動 (使用trainN.csv訓練SVM model)
在index.html的html，添加Trigger按鈕來跟AI Module進行互動
```html
<body>
	<div class="container">
		<div id="container" style="min-width: 310px; height: 400px; margin: 0 auto">Insert Highchart Here</div>
		<button class = "btn btn-warning " id = "GetData">GetData</button>		
		<button class = "btn btn-dangerous"id = "trigger">Trigger EA</button> 
	</div>
</body>
```
並定義此按鈕的按鈕要觸發的行為(執行GetPredidct.php)，並在執行完成後重新載入資料
```javascript
const getData = () => {
  $.ajax({									  
    url: './GetData.php',//連接的URL	  
    data: "{}",//夾帶的參數
    dataType: 'json', //資料格式 
    success: function(data)	//傳送成功的function
      {	
	lights = [];
	time = [];
	data.map((data, index) => {
		console.log(data['status']);
		data['status'] == 1 ? lights.push({y:parseInt(data['value']), color: '#00FF00' }) : lights.push({y:parseInt(data['value']), color: '#FF0000' });
		time.push(data['time']);
	})
        highcharsinit();
        } //success end
    }); //ajax end
}

window.onload = () => {
  $('#trigger').click( () => {
    $.ajax({
      url: './GetPredict.php',
      // success: getData()
      success: () => {
        getData();
      }
    })
  })
}

$(function () {
  getData()
}); //function end
```
分類模型採用SVM模型進行預測(myEA.py)
```python
model=SVC()           #支持向量機
model.fit(X,Y)
```
對於sensor採樣到的資訊進行分類
```python
c.execute("SELECT * FROM sensors")

#====== 取回所有查詢結果 ======#
results = c.fetchall()
print(type(results))
print(results[:10])
if debug:
    input("pause ....select ok..........")

test_df = df(list(results),columns=['id','time','value','temp','humi','status'])

print(test_df.head(10))
if debug:
    input("pause..  show original one above (NOT correct).......")

testX=test_df['value'].values.reshape(-1,1)
testY=model.predict(testX)
print(model.score(testX,testY))

test_df['status']=testY
```
接著更新回database
```python
c.execute('update sensors set status=0 where value>0')

## choose status ==1 have their id available
id_list=list(test_df[test_df['status']==1].id)
print(id_list)
            
for _id in id_list:
    c.execute('update sensors set status=1 where id='+str(_id))
```
執行AI Module前後的結果比較
<div align='center'>
  <img src="https://github.com/chomachoa265/AIoT/blob/main/homework5/result_assets/part2_UI.png"/>
  <img src="https://github.com/chomachoa265/AIoT/blob/main/homework5/result_assets/part2_UI_pressResult.png"/>
</div>


# Part 3:  AI module myAI.pkz 訓練出來放到 web (save & load trained model)
在檔案(myEA.py)中使用pickle, gzip來保存訓練好的模型，並且在modelPredict呼叫並進行數據的預測和更新，<br/>
這樣就不需要訓練資料集(trainN.csv)以及訓練模型，只需載入預訓練好的模型(myAI.pkz)就可以進行預測和更新。

保存(myEA.py)
```python
with gzip.GzipFile('./myAI.pkz', 'w') as f:
    pickle.dump(model, f)
```
讀取(modelPredict.py)
```python
with gzip.open('./myAI.pkz', 'r') as f:
    model = pickle.load(f)
```
並將執行路徑修改為modelPredict(GetPredict.php)
```php
$output = shell_exec('python modelPredict.py');
echo $output
```
# Part  4: 使用Flask進行實現
### 環境需求套件
1. Flask
2. pymysql
### 代碼實現
在main.py內去實現Part1 ~ Part3的功能，主要使用pymysql來與資料庫進行互動，

#### 重新實現Part. 1(noAI)
定義新的url，回傳indexNoAI的html樣板
```python
@app.route('/noAI')
def noAI():
    return render_template("indexNoAI.html")
```
getData api用來抓取資料表(sensor)內的資料，這邊僅使用time, value, status三個屬性，
其中cursors.DictCursor可讓cursor抓取到的資料為字典型式，在轉換為json上會更為直覺
```python
@app.route('/getData')
def getData():
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    # cursor will return dictionary type
    c = conn.cursor(pymysql.cursors.DictCursor) 
    c.execute("SELECT time, value, status FROM sensors")
    data = c.fetchall()
    return jsonify(data)
```
#### 重新實現Part. 2 & Part. 3(AI)
讀取trainN.csv訓練資料當作SVM的訓練集
```python
@app.route('/getPredict')
def getPredict():
    debug =0

    # part.2 section
    #=================read Data=================#
    data=pd.read_csv("./dataset/trainN.csv")        #載入traning.csv至data

    X=data['value'].values.reshape(-1,1)
    Y=data['status'].values.reshape(-1,1)

    #=================read Data End=================#
    #
```
定義模型並訓練，並將模型壓縮為pkz檔保存在models資料夾
```python
    model=SVC()           #支持向量機
    model.fit(X,Y)

    # part.3 section

    import pickle
    import gzip
    os.makedirs("./models", exist_ok=True)
    with gzip.GzipFile('./models/myAI.pkz', 'w') as f:
        pickle.dump(model, f)
    #
```
訓練完模型，將sensors資料的預測狀態利用模型重新評估，並使用update語法更新回資料庫
```python
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
```
將所有資料的status清除
```python
    if debug:
        input("pause.. now show correct one above.......")

    c.execute('update sensors set status=0 where value>0')
```
將預測狀態為1的id保存為list並更新回資料庫
```python
    ## choose status ==1 have their id available
    id_list=list(test_df[test_df['status']==1].id)
    print(id_list)
                
    for _id in id_list:
        #print('update light set status=1 where id=='+str(_id))
        c.execute('update sensors set status=1 where id='+str(_id))

    conn.commit()

    if debug:
        input("pause ....update ok..........")

    c.close()
    conn.close()

    return "OK"
```
### 結果呈現
<div align='center'>
  <img src="https://github.com/chomachoa265/AIoT/blob/main/homework5/result_assets/part2_UI.png"/>
  <img src="https://github.com/chomachoa265/AIoT/blob/main/homework5/result_assets/part2_UI_pressResult.png"/>
</div>

# Part  5: 改成 ngrok 讓他有一個domain name

下載ngrok(https://ngrok.com/download) ，並持續讓他在背景執行，ngrok會派發一個domain name讓外網也能夠存取你的App(不侷限在本地端)。<br />
命令列語法(綁定Apache的監聽埠，若使用Flask則綁定app.run定義的埠口(預設為5000))
```
ngrok http <XAMPP Apache listen port | Flask port>
```
執行後，domain name為0fda-2001-b400-e4d4-9966-4931-116-faac-5376.jp.ngrok.io，並進行App的測試。
<div align='center'>
  <img src="https://github.com/chomachoa265/AIoT/blob/main/homework5/result_assets/part4_resultNgrok.png"/>
  <img src="https://github.com/chomachoa265/AIoT/blob/main/homework5/result_assets/part4_testNgrok.png"/>
</div>


