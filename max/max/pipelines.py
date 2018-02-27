# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class MaxPipeline(object):
    def process_item(self, item, spider):
        return item

'''CREATE TABLE `vpgame`.`competitions` (
  `id` VARCHAR(45) NOT NULL,
`name` VARCHAR(100) NULL,
  `mode` VARCHAR(45) NULL,
  `modename` VARCHAR(45) NULL,
  `left_odd` DOUBLE NULL,
  `right_odd` DOUBLE NULL,
  `date` DATE NULL,
  `competitionscol` VARCHAR(45) NULL,
  `left_team` VARCHAR(45) NULL,
  `right_team` VARCHAR(45) NULL,
  `status` VARCHAR(45) NULL,
  `left_id` VARCHAR(45) NULL,
  `right_id` VARCHAR(45) NULL,
  `victory` VARCHAR(45) NULL,
  `whowins?` VARCHAR(45) NULL,
  `left_team_score` VARCHAR(45) NULL,
  `right_team_score` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));
'''

class save_sql(object):
    def open_spider(self,spider):
        self.db = pymysql.connect('localhost', 'root', '192837', 'vpgame', charset="utf8")
        self.cursor = self.db.cursor()

    def process_item(self,item,spider):
        key1 = ['id', 'name', 'mode', 'modename',
                'left_odd', 'right_odd', 'date', 'competitioncol', 'left_team',
                'right_team', 'status','left_id', 'right_id','victory', 'whowins', 'left_team_score', 'right_team_score']
        sql="insert into competitions values("
        print("这里应该有所记录")
        for key in key1[:-1]:
            sql+="'"+str(item.get(key,"Null"))+"',"
        sql=sql+str(item[key1[-1]])+')'



        self.cursor.execute(sql)




        self.db.commit()
        return item



    def close_spider(self,spider):
        self.db.close()



