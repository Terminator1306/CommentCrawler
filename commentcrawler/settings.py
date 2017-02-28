# -*- coding: utf-8 -*-

# Scrapy settings for commentcrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'commentcrawler'

SPIDER_MODULES = ['commentcrawler.spiders']
NEWSPIDER_MODULE = 'commentcrawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'commentcrawler (+http://www.yourdomain.com)'
USER_AGENTS = [
  "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
  "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
  "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
  "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
  "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
  "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
  "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
  "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
  "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",

  # 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)',
  # 'Googlebot/2.1 (+http://www.google.com/bot.html)',
  # 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
  # 'Sogou web spider/3.0(+http://www.sogou.com/docs/help/webmasters.htm#07)',
  # 'Sogou Push Spider/3.0(+http://www.sogou.com/docs/help/webmasters.htm#07)',
  # 'Mozilla/5.0 (compatible; Yahoo! Slurp China; http://misc.yahoo.com.cn/help.html)',
  # 'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',

]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 10
# CONCURRENT_REQUESTS_PER_IP = 1

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'application/javascript, */*;q=0.8',
  'Accept-Language': 'zh-CN,zh;q=0.8',
  'Connection': 'keep-alive',
  # 'Cookie': 'pnm_cku822=075UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5OcktwRX5FeEF5THNNciQ%3D%7CU2xMHDJ7G2AHYg8hAS8WIgwsAl4%2FWTVSLFZ4Lng%3D%7CVGhXd1llXGdSaVJvVm5bZFplUm9NdEl3SXdPc0l9RXhEcUR9R2k%2F%7CVWldfS0TMwY4BycSMhwkFHMIWDVfe1UDVQ%3D%3D%7CVmhIGCUFOQc8BycbIh0jAzgFPAIiHiceIwM3CjcXKxIrFjYDOAVTBQ%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D  cookie2=1abd1988561b207bbffbc860ebcbeb2f  res=scroll%3A1423*6043-client%3A1423*799-offset%3A1423*6043-screen%3A1440*900  l=AoCAedPj4WQcxKerV6ErAiSI0ARSCWTT  _tb_token_=oIA8dqMGpOuU  t=265651046d436fb6c5a7a398e4d65a4c  cna=MgGQDlZ+nHsCAWonKbYoFjaM  cq=ccp%3D1  isg=AikpBI00WtENd2aQhdgdXB8vONXKrB0oyAa8HMsepZBPkkmkE0Yt-BeAIoFe  _med=dw:1440&dh:900&pw:1440&ph:900&ist:0'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    # 'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
#    'commentcrawler.middlewares.MyCustomSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'commentcrawler.middlewares.RandomUserAgent': 543,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
    # 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
    # 'commentcrawler.middlewares.ProxyMiddleware': 544,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'commentcrawler.pipelines.Pipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'


PROXIES = [
  {'ip_port': '171.36.255.111:8123', 'user_pass': ''},
  {'ip_port': '183.136.217.75:8080', 'user_pass': ''},
  {'ip_port': '116.213.105.10:80', 'user_pass': ''},
  {'ip_port': '59.37.162.133:80', 'user_pass': ''},
  {'ip_port': '59.151.3.197:80', 'user_pass': ''},
  {'ip_port': '59.151.77.26:80', 'user_pass': ''},
]

# SPLASH_URL = 'http://192.168.59.103:8050/'
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'