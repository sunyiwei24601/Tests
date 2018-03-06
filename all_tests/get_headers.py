c='http://eams.sufe.edu.cn/eams/allTeachTaskSearch!info.action?removeBack=1&lesson.id={id}'
import requests
import time
id1=246236
id2=249502

def getnum(id,num):
    r=requests.get(c.format(id=id)).text
    from bs4 import BeautifulSoup as bs
    b=bs(r,'html.parser')
    nums=b.find_all('td',attrs={'class':"content",'colspan':"3"})[5].text
    from all_tests.email1 import  post_message
    if(int(nums)<num):
        post_message("有空余的位置啦！！！点击链接进入\nhttp://eams.sufe.edu.cn/eams/stdElectCourse.action")
        return 2
    else:
        print("本次获取到的已参加人数为{}".format(nums)+time.ctime())
    time.sleep(30)

while(True):
    if(getnum(id1,120)==2 or getnum(id2,120)==2):
        break



