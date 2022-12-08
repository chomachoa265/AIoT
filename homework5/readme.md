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
        humis=[];
        temps = [];
        time = [];

        for (var i =  0; i < data.length; i++)
        {
          if(parseInt(data[i][5])==0){
            lights.push({y:parseInt(data[i][2]), color: '#FF0000' });
          }else{
            lights.push({y:parseInt(data[i][2]), color: '#00FF00' });
          }
          time.push(data[i][1]);
        }
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

# Part  4: 改成 ngrok 讓他有一個domain name

下載ngrok(https://ngrok.com/download) ，並持續讓他在背景執行，ngrok會派發一個domain name讓外網也能夠存取你的App(不侷限在本地端)。<br />
命令列語法(綁定Apache的監聽埠)
```
ngrok http <XAMPP Apache listen port>
```
執行後，domain name為0fda-2001-b400-e4d4-9966-4931-116-faac-5376.jp.ngrok.io，並進行App的測試。
<div align='center'>
  <img src="https://github.com/chomachoa265/AIoT/blob/main/homework5/result_assets/part4_resultNgrok.png"/>
  <img src="https://github.com/chomachoa265/AIoT/blob/main/homework5/result_assets/part4_testNgrok.png"/>
</div>

# Part 5: 放到 GITHUB 自動部署到 Railway
