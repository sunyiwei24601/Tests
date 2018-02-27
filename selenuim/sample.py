import requests
from bs4 import BeautifulSoup as bs

home_url='http://wlan.ct10000.com/?UserIPAddress=101.94.8.29&MSCGIP=124.74.56.71&UserLocation=ethtrunk/20:402.0'
r=requests.get(home_url)
t=r.text
print(t)
b=bs(t,'html.parser')
paramstr=b.find_all('frame',attrs={'name':'mainFrame'})[0].attrs['src'].split('?')[1].split('=')[1]
input_url='http://wlan.ct10000.com/style/cjdx/index.jsp?paramStr={paramstr}'


input=requests.get(input_url.format(paramstr=paramstr)).text
print(input)
b2=bs(input,'html.parser')
paramstr=b2.find_all('input',attrs={'name':'paramStr'})[0].attrs['value']
print(paramstr  )
formdata={'defaultProv':'sh',
          'isChCardUser':'false',
          'isRegisterRealm':'false',
          'isWCardUser':'false',
          'paramStr':paramstr,
          #'paramStrEnc':'%2FQAcMcmUlGW68MioOv9jcasVMMu21cFgORAqnf8CSTSW9PFlihv28rA6aY8erEYPwkVo2cCnkCIcEgOw4wYf2yI5ydeHT%2F9pMtcALV584ok42sCx7rv9mn%2BFaBIx9Z2RVi%2BFN0zFJQgxZh%2B1RhV3yQogv74zN95YKRcIGYqyqLwRV7y8nxFZkWZeEZR1UD43l1ZXj6G8u%2BCZd7ZJm2F7iyKwOBCqxDYkiTTfShwjG8eD8tirRhh8xyCO9hbihBwSh1zjS4bBsb5a3ngl7ampfAthwBKe8IZQpLa9obDIAD8UPKgGZX4k1ZAuzwy9VLaeP0tSPcfs3ieJ%2FlwzbBCSboOFLPND2FcSR0yQHVCns6XuFxj7qe5PJA%3D%3D',
          'Password':294239,
          'province':'wlan.sh.chntel.com',
          'UserName':1027220030544,
}

url='http://wlan.ct10000.com/authServlet'
ss=requests.post(url=url,data=formdata)
print(ss.text)