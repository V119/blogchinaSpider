# -*- coding: utf-8 -*-

# Scrapy settings for blogchinaSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'blogchinaSpider'

SPIDER_MODULES = ['blogchinaSpider.spiders']
NEWSPIDER_MODULE = 'blogchinaSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'blogchinaSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

CONCURRENT_ITEMS = 1000

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 256

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.25
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 128
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
                    'Accept':'text/javascript, application/javascript,application/ecmascript, application/x-ecmascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip,deflate',
                    'Accept-Language': 'zh-CN, zh; q=0.8, en-US; q=0.5, en; q=0.3',
                    'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'blogchinaSpider.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'blogchinaSpider.middlewares.rotate_useragent.RotateUserAgentMiddleware': 543,
}

USER_AGENT = ''

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     'blogchinaSpider.pipelines.ImageSavePipeline': 300,
#     'blogchinaSpider.pipelines.SaveHBasePipeline': 400
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 3
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 日志文件存储路径
# LOG_FILE = "blogchinaSpider/logs/scrapy.log"

# 图片存储路径
IMAGES_STORE = 'images/'

# 连接Hbase配置
HBASE_URI = '192.168.100.103'
HBASE_PORT = '9090'

# HBase 表名称
TB_INFO = 'spider_info'
TB_AUTHOR = 'blogchina_author'
TB_BLOG = 'blogchina_blog'
TB_COMMENT = 'blogchina_comment'
