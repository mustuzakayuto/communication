from pytrends.request import TrendReq
import matplotlib.pyplot as plt
from datetime import date
import datetime
import dateutil.relativedelta as relativedelta
import re
import random
def main(keyword="None",ego="JP",pn="japan",hl="jp"):
    dt_now = datetime.datetime.now()
    current_day = date.today()

    months = 1# print(current_day - relativedelta.relativedelta(day=dt_now.day-1))
    # monthsは変えると何か月前か
    one_month_ago = date.today() - relativedelta.relativedelta(days=10) if(months==0) else date.today() - relativedelta.relativedelta(months=months)
    timeframe = str(one_month_ago)+" "+str(current_day)

    # googleトレンドに接続するための設定
    # hlは host language、tzはtime zoneの設定
    pytrends = TrendReq(hl = hl+"-"+ego,tz =-540, timeout=(10, 25))
    # keyword = "None"
    is_key = True
    kw_list = [keyword]

    pytrends.build_payload(kw_list,timeframe =timeframe,geo=ego)
    Rapidly_Rising_Keywords =pytrends.trending_searches(pn=pn)


    #データの取得
    

    
    
    
    if(keyword!="None"):
        print("関連キーワード")
        data=[]
        pytrends = TrendReq(hl = hl+"-"+ego,tz =-540, timeout=(10, 25),retries=1)
        pytrends.build_payload(kw_list,timeframe =timeframe,geo=ego)
        p = pytrends.related_queries()

        # 急上昇関連キーワード
        Rapidly_Rising_Keywords = p[kw_list[0]]["rising"]
        # print(Rapidly_Rising_Keywords)
        for text in str(Rapidly_Rising_Keywords).split("\n")[1:-1]:
            
            newstring = ''.join([i for i in text if not i.isdigit()])

            
            data.append(newstring.strip())
    else:
        Rapidly_Rising_Keywords =pytrends.trending_searches(pn=pn)

        print("急上昇キーワード")
        data=[]
        for text in str(Rapidly_Rising_Keywords).split("\n")[1:-1]:

            
            newstring = ''.join([i for i in text if not i.isdigit()])
            if not newstring.strip() in data:
                data.append(newstring.strip())        
        
    # print(data)
    return data
if __name__ =="__main__":
    print(main("ウサギ"))
    