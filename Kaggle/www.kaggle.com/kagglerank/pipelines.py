# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import json
class KagglerankPipeline(object):
    def process_item(self, item, spider):
        return item
    def close_spider(self,spider):
        with open('compete_ranking.json','w')as f:
           json.dump(spider.com_rank_users,f)

class kernels_mysql_save(object):
    def open_spider(self,spider):

        self.db = pymysql.connect('localhost', 'root', '192837', 'kaggle', charset="utf8")
        self.cursor = self.db.cursor()


    def process_item(self, item, spider):

        sql="insert into kernels VALUES("
        keys=[]
        for i in item:
            keys.append(i)
        for i in keys[:-1]:
            sql+="'"+str(item.get(i,"NUll")).replace("'",r"\'")+"',"
        sql = sql + str(item[keys[-1]]).replace("'",r"\'") + ')'

        self.cursor.execute(sql)
        self.db.commit()

        return item

    def close_spider(self,spider):
        print(spider.valid_num)
        print(spider.invalid_num)
        self.db.close()

