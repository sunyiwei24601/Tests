# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class KaggleItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class competitionItem(Item):
    ID=Field()
    username=Field()
    home_page_url=Field()
    competition_name=Field()
    competition_url=Field()
    enabled_time=Field()
    dealine=Field()
    rank=Field()
    medal_type=Field()
    remark=Field()
    scrapy_time=Field()
    reward_display=Field()