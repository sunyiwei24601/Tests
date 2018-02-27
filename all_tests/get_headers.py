import requests
import json


url='http://www.vpgame.com/gateway/v1/match/?callback=jQuery19109015450847762417_1519437297376&page=1&category=sports&status=close&limit=100&lang=zh_CN&_=1519437297423'
r=requests.get(url).text
r=r.split("(")[1][0:-1]
print(json.loads(r))