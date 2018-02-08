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
    'authorization': 'Bearer 2|1:0|10:1516079727|4:z_c0|92:Mi4xa0pzZ0FBQUFBQUFBVUtkZ3pXel9EQ1lBQUFCZ0FsVk5iOWhLV3dCenFuODV2U3lfOUR4RXFkUFVxMEhuY1A4UVpn|9f79d8ed5677975e6af6ff90036cce6ebced61eaa62a484698b1ee493c8dff3b',
    'x-udid': 'AIBs1jz-GA2PTpjzz1T6NK3I9R2zCtydTCI=',
    'origin': 'https://www.zhihu.com',
    'Cookie': 'q_c1=e84afa18f842439ca6ea21290194baad|1516079712000|1516079712000; capsion_ticket="2|1:0|10:1516079722|14:capsion_ticket|44:MDY3NzQ1OWUxNTEwNDNhMmI1YTg4ZmJmYWQ1M2Y2NzY=|607ea0324a5878c26b782b0142ec76f06e7d39dd33a21990c172b47747d52298"; _zap=dd4d01dc-f921-46ec-a2d0-ad9df7450d9b; z_c0="2|1:0|10:1516079727|4:z_c0|92:Mi4xa0pzZ0FBQUFBQUFBVUtkZ3pXel9EQ1lBQUFCZ0FsVk5iOWhLV3dCenFuODV2U3lfOUR4RXFkUFVxMEhuY1A4UVpn|9f79d8ed5677975e6af6ff90036cce6ebced61eaa62a484698b1ee493c8dff3b"; aliyungf_tc=AQAAALMMejeepwIAcvznZbPNo54AvQ5z; _xsrf=764ad8b6-bf62-40d6-a3c5-b46cc2ce47d0; d_c0="AIBs1jz-GA2PTpjzz1T6NK3I9R2zCtydTCI=|1517795559"',
    'Connection':' keep-alive'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhihuActs.middlewares.ZhihuactsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'zhihuActs.middlewares.MyCustomDownloaderMiddleware': 543,
#}

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
