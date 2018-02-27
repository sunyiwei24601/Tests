# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field,Item

class MaxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    key1=['id','name','mode','modename','status',
        'left_odd','right_odd','date','competitioncol','left_team','left_id','right_id',
      'right_team','victory','whowins','left_team_score','right_team_score']


    id=Field()
    name=Field()
    mode=Field()
    modename=Field()
    status=Field()
    left_odd=Field()
    right_odd=Field()
    date=Field()
    competitioncol=Field()
    left_team=Field()
    left_id=Field()
    right_id=Field()
    right_team=Field()
    victory=Field()
    whowins=Field()
    left_team_score=Field()
    right_team_score=Field()





