#coding=utf-8
"""下载相关功能模块，包括下载延迟，代理ip与浏览器user-agent，下载功能的封装"""
import time
import random
import urlparse
import datetime
import requests
import books.bookconfig as book_config

class Throttle(object):
    """Throttle类 下载限速 对两次HTTP请求之间的间隔时间进行限制，防止过频请求。
        当前时间-上次HTTP请求发起时间，得到的时间差即为两次HTTP请求之间的间隔时间"""
    def __init__(self,delay):
        """初始化Throttle类 设置两次http请求间隔时间
            :param  delay 两次HTTP请求的间隔时间"""
        self.delay = delay
        #储存url的主机域名（host)：请求发起时间
        self.domains = {}

    def wait(self,url):
        """对url 进行下载延迟设置
            :param  url 需要延迟的url"""
        #从url中解析出 主机域名（host)
        domain = urlparse.urlparse(url).netloc
        #获得当前主机域名的上次HTTP请求的发起时间
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            #datetime.datetime.now()-last_accessed
            #当前时间-上次HTTP请求发起时间，得到的时间差为 本次HTTP请求，与上次HTTP请求的时间差。
            #预设休眠时间 delay - 两次请求时间差 即为 两次请求之间的延迟时间。
            #secods 返回 timedelta类型 second 返回 datetime类型
            sleep_secs = self.delay - (datetime.datetime.now()-last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        #更新当前域名的 HTTP请求 发起时间
        self.domains[domain] = datetime.datetime.now()

class ProxyAgent(object):
    """ProxyAgent类 获得代理ip 和 浏览器标识 User-agent"""

    def __init__(self):
        """初始化User-Agent 池，proxy ip池"""

        #self.proxy_ip_list = []
        self.user_agent_list = [
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
    'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
    'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
    'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0',
    'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
    'UCWEB7.0.2.37/28/999',
    'NOKIA5700/ UCWEB7.0.2.37/28/999',
    'Openwave/ UCWEB7.0.2.37/28/999',
    'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999',
    'UCWEB7.0.2.37/28/999',
    'NOKIA5700/ UCWEB7.0.2.37/28/999',
    'Openwave/ UCWEB7.0.2.37/28/999',
    'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999'
    ]

    # def get_proxy_ip(self):
    #     """随机获取一个代理ip
    #         :return 返回一个格式为 ip ：port 的字符串形式的代理ip"""
    #     if len(self.proxy_ip_list) < 30:
    #         response = requests.get('http://localhost:8000/')
    #         self.proxy_ip_list = json.loads(response.text)
    #         #print '请求代理IP'
    #     proxy_ip = random.choice(self.proxy_ip_list)
    #     proxy_ip_str = "{}:{}"
    #     return proxy_ip_str.format(proxy_ip[0],proxy_ip[1])

    def get_user_agent(self):
        """随机获得一个浏览器标示 user-agent
            :return 一个浏览器标示 user-agent"""
        return random.choice(self.user_agent_list)

class Downloader(object):
    """下载类 对requests的简单封装
        通过 down = Downloader(headers={})
            html = down(url)
        来使用 Downloader类"""

    def __init__(self,delay=5,headers=None,num_retries=3,encoding='utf-8',timeout=10,cache=None,isBinary=False):
        """初始化Downloader相关参数
            :param  delay 下载延迟时间
            :param  timeout 下载超时时间
            :param  encoding  html编码
            :param  num_retries 下载重试次数
            :param  isBinary：是否下载二进制数据，例如图片 True表示下载二进制数据，Flase表示 下载普通html页面"""

        self.throllte = Throttle(delay)
        self.headers = headers
        self.proxy_agent = ProxyAgent()
        self.num_retries = num_retries
        self.cache = cache
        self.timeout = timeout
        self.encoding = encoding
        #是否下载二进制数据，例如图片，压缩文件 之类的。
        #True表示下载，Flase表示正常下载 HTML文件。默认Flase
        self.isBinary = isBinary
        #日志
        self.console_logger = book_config.CONSOLE_LOGGER
        self.error_logger = book_config.ERROR_LOGGER

    def __call__(self,url):
        """回调方法
            :param  url 需要进行下载的url
            :return  返回下载完成的html页面"""
        result = None
        #如此存在缓存数据，则从缓存数据中获得数据
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
        #没有数据，则重新下载url
        if not result:
            self.throllte.wait(url)
            result = self.download(url,self.headers,self.num_retries)
            if self.cache:
                self.cache[url] = result
        return result['html']

    def download(self,url,headers,num_retries,data=None):
        """根据url下载html，对requests的简单封装
            :param  url 需要下载的url
            :param  headers  HTTP header
            :param  num_retries  下载重试次数
            :param  data  post请求时需要发送的数据
            :return  下载的html，下载失败则返回None
           当下载过程中产生 超时异常或者 500-600之间的HTTP 状态码，则下载重试num_retrie次数
            """
        #print '下载---',url
        logger_info = u'下载 --- %s ' % url
        self.console_logger.info(logger_info)

        user_agent = self.proxy_agent.get_user_agent()
        headers['User-Agent'] = user_agent
        html = None
        #print '代理：',proxies
        #print 'User_Agent:',user_agent
        try:
            response = requests.get(url,headers,timeout=self.timeout,data=data)
            if self.isBinary:
                #下载二进制数据，例如 图片，压缩文件之类
                html = response.content
            else:
                response.encoding = self.encoding
                html = response.text
            code = response.status_code
            if 500 <= code < 600:
                raise response.raise_for_status()
        except requests.HTTPError as e:
            #print '服务器错误：',e
            logger_info = u'服务器错误: %s ' % url
            self.console_logger.info(logger_info)

            if num_retries > 0:
                #print '重试 ',num_retries
                logger_info = u'重试: %s ' % num_retries
                self.console_logger.info(logger_info)
                return self.download(url,headers,num_retries-1,data)
            else:
                #print '记录写入日志'
                error_info = u'服务器错误 下载 : %s 失败' % url
                self.error_logger.error(error_info)
        except (requests.Timeout,requests.ConnectionError) as e:
            #print '超时异常---',e
            logger_info = u'下载超时  ---   %s ' % url
            self.console_logger.info(logger_info)
            if num_retries > 0:
                #print '重试 ', num_retries
                logger_info = u'重试: %s ' % num_retries
                self.console_logger.info(logger_info)
                return self.download(url,headers,num_retries-1,data)
            else:
                #print '记录写入日志'
                error_info = u'超时异常  下载 : %s 失败' % url
                self.error_logger.error(error_info)

        return {'html':html}

