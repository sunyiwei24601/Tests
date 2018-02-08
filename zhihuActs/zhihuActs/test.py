import requests
from PIL import Image
from bs4 import  BeautifulSoup as bs


url='https://upload.jianshu.io/users/upload_avatars/4717565/ea654134-b784-4f5a-8f25-1c230d703dd9.jpg?imageMogr2/auto-orient/strip|imageView2/1/w/96/h/96'
j=requests.get(url)
with open('w.jpg','wb') as file:
    file.write(j.content)

im=Image.open('w.jpg')
im.show()
im.close


