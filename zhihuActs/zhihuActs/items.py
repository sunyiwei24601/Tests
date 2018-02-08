# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item ,Field


class actsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_id=Field()
    time=Field()
    type=Field()
    article_id=Field()
    title=Field()
    voteup_count=Field()
    comments_author=Field()
    question_id=Field()
    topics=Field()
    thanks_count=Field()
    roundtable_id=Field()
    column_id =Field()
    pin_id=Field()
    url_token=Field()


