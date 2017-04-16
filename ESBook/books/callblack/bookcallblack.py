#coding=utf-8
"""book回调模块，处理具体逻辑"""
import re
import urlparse
from bs4 import BeautifulSoup
import books.bookconfig as book_config

class BookSpiderCallblack(object):
    """对小说主页中的所有小说url进行爬取"""
    def __init__(self):
        """初始化 相关参数
            math 匹配 以 / 开头 且 以 / 结尾的相对url，此url即为小说url"""

        self.math = re.compile('^/.*?/$')
        self.console_logger = book_config.CONSOLE_LOGGER
        self.error_logger = book_config.ERROR_LOGGER


    def get_book_links(self, url, html):
        """解析小说主页并获得主页中所有小说url
            :param  url 小说主页url,用于跟踪url对应的页面
            :param  html 小说主页html
            :raise  html页面解析失败则抛出 ValueError
            :return  小说主页中的所有小说url set集合
        """

        soup = BeautifulSoup(html, 'lxml')
        div_main = soup.select('div#main')
        if div_main:
            a_links = div_main[0].select('a')
            book_links = []
            for link in a_links:
                patter = re.search(self.math, link['href'])
                if patter:
                    book_links.append(urlparse.urljoin(url, link['href']))
            #print '总是 ',len(book_links)
            return set(book_links)
        else:
            #print '页面不正常 ：',base_url,'写入日志'
            raise ValueError(u'页面内容不正常 ' + url)

    def __call__(self, url,html):
        """回调函数 调用get_book_links() 方法解析html
            :param  url 小说主页url,用于跟踪url对应的页面
            :param  html 小说主页html
            :raise html页面不存在，则抛出 ValueError异常
            :return  小说主页中的所有小说url set集合"""
        if html:
            links = self.get_book_links(url,html)
            if links:
                return links
        else:
            #print 'html 不存在',url
            raise ValueError(u'html 页面不存在 ' + url)
