# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from scrapy import Item

class kernelItem(Item):
    title = Field()
    scriptVersionId = Field()
    languageName = Field()
    kernels_url = Field()

    lastRunTime = Field()
    enabled_time=Field()
    totalVotes = Field()
    medal = Field()
    competition_id=Field()
    scrapy_time=Field()
    ID = Field()
    username = Field()
    home_page_url = Field()
