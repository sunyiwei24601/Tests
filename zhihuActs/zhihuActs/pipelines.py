# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import pymysql
import time
import json
from zhihuActs.items import actsItem
class ZhihuactsPipeline(object):
    def process_item(self, item, spider):
        return item

class save_token_pipline(object):
    def close_spider(self,spider):
        fieldnames = ['first_name', 'last_name']

        with open('token_url.csv', 'w', newline='', encoding='utf-8') as file:
            w = csv.writer(file)
            print(spider.tokens)
            for token in spider.tokens:
                w.writerow([str(token)])


class save_activities_pipline(object):

    def process_item(self,item,spider):
        act =dict(item)
        spider.activities.append(act)
        return item

    def close_spider(self,spider):
        fieldnames = actsItem.fields.keys()
        with open('activities.csv', 'w', newline='', encoding='utf-8') as file:
            w = csv.DictWriter(file, fieldnames=fieldnames)
            w.writeheader()
            for act in spider.activities:
                w.writerow(act)

class save_activities_mysql_pipeline(object):

    current_token=None
    def open_spider(self,spider):
        self.db = pymysql.connect('localhost', 'root', '192837', 'zhihu_comments',charset="utf8")
        self.cursor = self.db.cursor()

    def process_item(self,item,spider):



        sql="insert into commnet1 VALUES({article_id}," \
            "'{column_id}','{comments_author}',{pin_id},{question_id}," \
            "'{roundtable_id}',{thanks_count},'{time}','{title}'," \
            "'{topics}','{type}','{url_token}','{user_id}',{voteup_count})".format(
            article_id=str(item.get('article_id','Null')),
            column_id=str(item.get('column_id','Null')),
            comments_author=str(item.get('comments_author','Null')),
            pin_id=str(item.get('pin_id','Null')),
            question_id=str(item.get('question_id','Null')),
            roundtable_id=str(item.get('roundtable_id','Null')),
            thanks_count=str(item.get('thanks_count','Null')),
            title= str(item.get('title','Null')),
            time=str(item.get('time', 'Null')),
            topics= str(item.get('topics','Null')),
            type= str(item.get('type','Null')),
            url_token= str(item.get('url_token','Null')),
            user_id=str(item.get('user_id','Null')),
            voteup_count=str(item.get('voteup_count','Null')),)
        try:
            self.cursor.execute(sql)
        except:
            self.db.rollback()
        self.db.commit()
        return item


    def close_spider(self,spider):
        self.db.close()
        print('已经进入流程中的id如下:')
        print(spider.process_id)
        print('已经完成爬虫任务的id如下:')
        print(spider.finished_id)
        delete_id=[]
        for i in spider.process_id:
            if i not in spider.finished_id:
                delete_id.append(i)
        print('需要删除的id如下:')
        print(delete_id)

        time2=time.ctime()
        ctime2=time.time()

        '''在这里进行记录文件的调配'''
        log_text={}
        log_text["start_time"]=spider.time1
        log_text["finished_time"]=time2
        log_text['start_num']=str(spider.start_num)
        log_text['end_num']=str(spider.end_num)
        log_text["process_id"]=str(spider.process_id)
        log_text["finished_id"]=str(spider.finished_id)
        log_text["unfinisehed_id"]=str(delete_id)
        log_text["cost_time"]=cal_time(ctime2-spider.ctime1)
        log_text['finished_all']=str(spider.finished_all)
        filename="logs.txt"
        log_save(filename,log_text)

        save_name="unfinished_url.txt"
        with open(save_name,'w') as f:
           json.dump(spider.unfinished_items,f)


def log_save(filename,log_text):
    with open(filename,"a") as f:
        f.write("\n*********************************\n")
        for log in log_text:
            f.write(log)
            f.write(":\n")
            f.write(log_text[log])
            f.write("\n")

def cal_time(t):
    s=divmod(t,60)
    m=int(t/60)
    h=int(m/60)
    m=divmod(m,60)
    return("{h}hour{m}minutes{s}seconds".format(h=h,m=m[1],s=s[1]))

if(__name__=="__main__"):
    print(cal_time(3860))
