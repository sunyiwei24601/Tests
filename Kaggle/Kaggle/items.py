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
    deadline=Field()
    rank=Field()
    medal_type=Field()
    remark=Field()
    scrapy_time=Field()
    reward_display=Field()
    competitionscol = Field()

class discussItem(Item):
    ID = Field()
    username = Field()
    home_page_url = Field()

    forum_id=Field()
    forum_name=Field()
    forum_url=Field()

    forumTopic_id=Field()
    forumTopic_name= Field()
    forumTopic_url = Field()

    postDate = Field()
    message= Field()
    totalScore = Field()
    medal = Field()

    scrapy_time = Field()
    discussionscol=Field()
class kernelItem(Item):
    title =Field()
    kernel_id  =Field()
    scriptVersionId =Field()
    langaugeName =Field()
    scriptUrl =Field()

    scriptVersionDateCreated =Field()
    lastRunTime =Field()

    totalVotes =Field()
    medal =Field()

    ID =Field()
    username =Field()
    home_page_url =Field()