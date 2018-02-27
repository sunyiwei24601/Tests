
import json
import re
import requests
import time
import datetime
s3='http://www.vpgame.com/gateway/v1/match/schedule?callback=jQuery1910345916363048961_1519490981892&tid=100122157&lang=zh_CN&_=1519490981937'
s2='http://www.vpgame.com/gateway/v1/match/schedule?callback=jQuery1910345916363048961_1519490981896&tid=100122145&lang=zh_CN&_=1519490981938'
s1='http://www.vpgame.com/gateway/v1/match/schedule?callback=jQuery1910345916363048961_1519490981896&tid=100122139&lang=zh_CN&_=1519490981940'
s='http://www.vpgame.com/gateway/v1/match/?callback=jQuery191014842367920773536_1519492635891&page={}&category=dota&status=close&limit=6&lang=zh_CN&_=1519492635898'
s5='http://www.vpgame.com/gateway/v1/match/schedule?callback=jQuery19109639615167288685_1519494811934&tid=100122697&lang=zh_CN&_=1519494811949'
r=requests.get('https://www.kaggle.com/kernels.json?sortBy=votes&group=everyone&pageSize=30&userId=54836&page=20').content.decode('utf-8')

timeStamp=1519490981
dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
print(otherStyleTime)
j=json.loads(r)
print (j)
