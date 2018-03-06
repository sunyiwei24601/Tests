import requests
import json
url='https://www.kaggle.com/rankings.json?group=competitions&page={page}&pageSize=20'

r=requests.get(url).text
j=json.loads(r)
num=int(int(j['totalUsers'])/20)
com_rank_users={}
for i in range(394,num):
    print(i)
    try:
        r=requests.get(url.format(page=i)).text
        j = json.loads(r)
        for i in j['list']:
            com_rank_users[i['userUrl'][1:]] = i
    except:
        break


with open('compete_ratings3','w') as f:
    json.dump(com_rank_users,f)
