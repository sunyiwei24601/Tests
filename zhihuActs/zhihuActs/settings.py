# -*- coding: utf-8 -*-

# Scrapy settings for zhihuActs project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhihuActs'

SPIDER_MODULES = ['zhihuActs.spiders']
NEWSPIDER_MODULE = 'zhihuActs.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhihuActs (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Host": "www.zhihu.com",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept':' application/json, text/plain, */*',
    'Accept-Language':' zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    #'Accept-Encoding': 'gzip, deflate, br',

    'x-api-version': '3.0.40',
    'authorization': 'Bearer 2|1:0|10:1518512590|4:z_c0|92:Mi4xa0pzZ0FBQUFBQUFBd0d6dWU2c2pEU1lBQUFCZ0FsVk56dmR2V3dCdVdlcy1MSHQ1MkFyM1dXSlpLaF9MaXcyalJ3|5c98ec54dd91baa05f5d265ba19e034bcb28f36959ff93b47bb3a598bdbccb18',
    'x-udid': 'AIBs1jz-GA2PTpjzz1T6NK3I9R2zCtydTCI=',
    'origin': 'https://www.zhihu.com',
    #'Cookie': 'q_c1=f50fa6a18c5f4f51a25355d8cff4e8b5|1517492814000|1517492814000; _zap=c2177108-eed3-4e9e-ab21-89578ca4fa67; __utma=155987696.230811019.1517802882.1517802882.1517802882.1; __utmz=155987696.1517802882.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aliyungf_tc=AQAAAKFLu1nt+QoAcvznZTQ4wTXmWaQ8; _xsrf=27965d9b-a682-429a-8333-b79a1d5d3333; d_c0="AMBs7nurIw2PTsIMvtr8EAld-eHpebHzNV8=|1518512063"; capsion_ticket="2|1:0|10:1518512588|14:capsion_ticket|44:Yzk0MmFhMTMwMjc1NDQzOTgwN2M2YjAxZTU3ODJjOTg=|e742864cc35fa1616bd28c3657e149b5562e2394422097b27b7d9d823ef5109c"; z_c0="2|1:0|10:1518512590|4:z_c0|92:Mi4xa0pzZ0FBQUFBQUFBd0d6dWU2c2pEU1lBQUFCZ0FsVk56dmR2V3dCdVdlcy1MSHQ1MkFyM1dXSlpLaF9MaXcyalJ3|5c98ec54dd91baa05f5d265ba19e034bcb28f36959ff93b47bb3a598bdbccb18',
    'Connection':' keep-alive'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhihuActs.middlewares.ZhihuactsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'zhihuActs.middlewares.ProxyMiddleware': 543,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
 #See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'zhihuActs.pipelines.save_token_pipline': 300,
    'zhihuActs.pipelines.save_activities_pipline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
