import requests
url='http://baidu.com'
response=requests.get(url)
print(response.status_code)
print(response.text)

requests.post(url)
requests.put(url)
requests.get(url)

data={'name':'germey','age':22}

response=requests.get(url,params=data)

response.json()#如果得到的内容就是json形式可以用这个方法
response.content#获取二进制内容
with open('faction.ico') as f:
    f.write(response.content)
#通过这种方式就可以保存文件

#添加headers
headers={}
response=requests.get(url,headers=headers)
#history访问的历史记录
response.history


#文件上传
files={'file':open("cookie.txt",'rb')}
response=requests.post('http://httpbin.org/post',files=files)

#会话维持,模拟登陆,两次的请求会完全不一样，所以要用Session
s=requests.Session()
s.get(url)
response=s.get(url)

#证书验证
requests.get(url,verify=False)
requests.get(url,cert={'/path/server.crt','/path/key'})

#代理设置
proxies={
    'http':'http://user:password@ip'
}

#超时设置
requests.get(url,timeout=10)

#认证设置
from requests.auth import HTTPBasicAuth
r=requests.get(url,auth={'users','123'})
auth=HTTPBasicAuth('user','pass')