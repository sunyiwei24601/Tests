import csv
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud, ImageColorGenerator




comments=[]
with open(r'nutriline_comments.csv',newline='',encoding='utf-8') as file:
    reader = csv.DictReader(file)
    comments=[]
    for row in reader:
        comments.append(row['content'])

import jieba
import re
commentlist=[]
n=0
for comment in comments:
    n+=1
    for i in jieba.cut(comment,cut_all=True):
        if i!='':
            commentlist.append(i)
result={}
for word in commentlist:
    #if(len(word)>1):
        if result.get(word):
            result[word]+=1
        else:
            result[word]=1
pops=[]
'''
for word in result:
    if result[word]in(4,5,6):
        pops.append(word)

for key in pops:
    result.pop(key)
'''
stopwords = {}
isCN = 1 #默认启用中文分词
back_coloring_path = "nutilite.jpg" # 设置背景图片路径
font_path = 'D:\Fonts\simkai.ttf' # 为matplotlib设置中文字体路径没
imgname1 = "叶子图形纽崔莱单词2.png" # 保存的图片名字1(只按照背景图片形状)
imgname2 = "叶子图形纽崔莱单词.png"# 保存的图片名字2(颜色按照背景图片颜色布局生成)
d = path.dirname(__file__)

back_coloring = imread(back_coloring_path)# 设置背景图片
wc = WordCloud(font_path=font_path,
               background_color="white",  # 背景颜色
               max_words=2000,  # 词云显示的最大词数
               mask=back_coloring,  # 设置背景图片
               max_font_size=100,  # 字体最大值
               random_state=42,
               width=1000, height=860, margin=2,# 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
               )

wc.generate_from_frequencies(result)
image_colors = ImageColorGenerator(back_coloring)

plt.figure()
# 以下代码显示图片
plt.imshow(wc)
plt.axis("off")
plt.show()
# 绘制词云

# 保存图片
wc.to_file(path.join(d, imgname1))

image_colors = ImageColorGenerator(back_coloring)

plt.imshow(wc.recolor(color_func=image_colors))
plt.axis("off")
# 绘制背景图片为颜色的图片
plt.figure()
plt.imshow(back_coloring, cmap=plt.cm.gray)
plt.axis("off")
plt.show()
# 保存图片
wc.to_file(path.join(d, imgname2))




