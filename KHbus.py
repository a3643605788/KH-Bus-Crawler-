import urllib.request as req
import bs4
import json

# --------------- 將 url 解析成 list 後回傳 ---------------
def getdata(url):
    re = req.Request(url , headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    })

    with req.urlopen(re) as response:
        jsondata = response.read().decode("utf-8")

    jsondata = json.loads(jsondata)

    return jsondata





# --------------- 讓程式模仿普通人的訪問動作 ---------------
url = "https://ibus.tbkc.gov.tw/cms/driving-map"

re = req.Request(url , headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
})

with req.urlopen(re) as response:
    data = response.read().decode("utf-8")



# --------------- 抓 html 原始碼，篩選出 type = text/javascript script 標籤內容，再將篩選內容轉成 str 型態 ---------------
root = bs4.BeautifulSoup(data , "html.parser")
title = root.find_all("script" , {"type":"text/javascript"})
title1 = (str(title))



# --------------- 擷取篩選過的字串中部分的資料(provider ~ bus_type 之前的資料) ---------------
title2 = 'provider:'
title3 = 'bus_type'
data = title1[title1.index(title2):title1.index(title3)]



# --------------- 將部分擷取的資料再擷取， 用 eval() 函式 把 str 處理成其他型態的資料 ---------------
title2 = '{"ProviderId"'
title3 = '"}],'
data = data[data.index(title2):data.index(title3)+2]
b = eval(data)



#--------------- 抓處理過的資料所含的 routeMapImageUrl 對應值(url)---------------
urlstr = []
namezh = []
for i in b:
    if(i["routeMapImageUrl"] != ""):
        carname = i["NameZh"]
        str1 = i["routeMapImageUrl"]
        str2 = ':\/\/ibus.tbkc.gov.tw\/cms\/api\/route\/' 
        str3 = 'map'

        jsonurl = "https" + str1[str1.index(str2):str1.index(str3)] + "estimate"
        jsonurl = jsonurl.replace('\/','/')
        urlstr.append(jsonurl)
        namezh.append(carname)



# --------------- main ---------------
index=0
for url in urlstr:
    jsondata=getdata(url)
    
    count = 0
    while count<2:                                                                                      # count<2 代表抓2班公車的資訊
        print("[車名] : " , namezh[index])
        
        for i in jsondata:
            print("[站名] : " , i["StopName"])
            print("[到站時間] : ",i["ComeTime"])
            print()
        print("===============================================================================")
        index+=1
        count+=1
    break