# -*- coding: utf-8 -*-
import requests
# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random

class ZhihuactsSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

#代理服务器获取
class ProxyMiddleware(object):
    def __init__(self):

        pass

    def process_request(self,request,spider):
        if spider.ip==None:
            p=requests.get('http://localhost:5000/get')
            spider.ip=p.text
        else:
            if(spider.scrapy_times==10):
                spider.scrapy_times=0
                p = requests.get('http://localhost:5000/get')
                spider.ip = p.text
            else:
                spider.scrapy_times+=1
        request.meta['proxy']='http://{}'.format(spider.ip)

class Proxy_Bought_Middleware(object):
    def __init__(self):
        pass
    def process_request(self,spider,request):
        if(spider.scrapy_times>1500):
            spider.refresh_proxies()
            spider.scrapy_times=0
        else:
            spider.scrapy_times+=1


        request.meta['proxy']='http://{}'.format(random.choice(spider.ips))
