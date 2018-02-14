from bs4 import  BeautifulSoup as bs

import requests
url='http://www.ip181.com/'
r=requests.get(url)
r.encoding='gb2312'
html=r.text

soup=bs(html,'html.parser').find_all('tr')
re_ip_adress=[]
for i in soup:
    tds = i.find_all('td')
    for td in tds:
        if td.text == "高匿":
            ip=td.parent.find_all('td')
            re_ip_adress.append((ip[0].text,ip[1].text))



for adress,port in re_ip_adress:
    result = adress + ':' + port
    print(result)