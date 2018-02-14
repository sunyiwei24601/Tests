
import requests

get_url="http://localhost:5000/get"
r=requests.get(get_url)
print(r.text)

headers={'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0'}
proxy={'http':"http://{}".format(r.text)}
p='http://ip.t086.com/'
pro=requests.get(p,proxies=proxy,headers=headers)
pro.encoding='gbk'
print(pro.text)