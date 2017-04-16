#coding=utf-8
"""链接爬取模块"""
import books.bookconfig as book_config
import books.callblack.chapterCallblack as chap_call
from books.util.downloaders import Downloader
from books.util.mongoQueue import MongoQueue



# OUTSTANAING = 0  #未处理
# PROCESSING = 1   #待处理
# COMPLETE = 2     #已处理
# ERROR = 3        #产生异常的url

conlose_logger = book_config.CONSOLE_LOGGER
error_logger = book_config.ERROR_LOGGER

def book_crawler(seen_url,delay=5,num_retries=3,encoding='utf-8',headers=None,scrape_callblack=None,cache=None):
    """小说首页爬取，获得首页中所有小说url，并存储到urls队列中
        :param  seen_url 小说主页url
        :param  delay 请求间隔时间
        :param  num_retries 下载错误时重试次数
        :param  encoding 网页编码
        :param  headers HTTP请求头信息
        :param  scrape_callblack 回调函数，用于处理具体业务逻辑
        :param  cache 数据缓存
        :raise  ValueError url解析失败则抛出
    """
    # 待爬取URL
    crawl_queue = seen_url if isinstance(seen_url,list) else [seen_url]
    # urls队列，存储小说url
    book_queue = MongoQueue(book_config.BOOK_URLS_TABLE,book_config.BOOK_URLS_FIELD)
    # 下载功能
    D = Downloader(delay=delay,num_retries=num_retries,headers=headers,encoding=encoding,cache=cache)

    while crawl_queue:
        try:
            url = crawl_queue.pop()
            try:
                html = D(url)
                # 解析功能--解析小说首页，返回首页中的所有小说urls
                if scrape_callblack:
                    links = scrape_callblack(url,html)
                    # 将小说url添加到urls队列中
                    if links:
                        [book_queue.push(link) for link in links]
                else:
                    #print '请添加回调处理函数'
                    break
            except ValueError as e:
                error_info = u'出现错误跳过当前url 信息为：%s %s ' % (e.message, url)
                conlose_logger.error(error_info)
        except KeyError as e:
            conlose_logger.info(u'小说主页爬取已完成 ')
            break

def book_detail_crwler(delay=5,num_retries=3,encoding='utf-8',headers=None,scrape_callblack=None,cache=None):
    """小说详情页爬取，并将爬取到的章节url存储到urls队列中
        :param  delay 请求间隔时间
        :param  num_retries 下载错误时重试次数
        :param  encoding 网页编码
        :param  headers HTTP请求头信息
        :param  scrape_callblack 回调函数，用于处理具体业务逻辑
        :param  cache 数据缓存
        :raise  ValueError 详情页解析失败则抛出
    """
    #小说url队列，获得小说url
    book_queue = MongoQueue(book_config.BOOK_URLS_TABLE,book_config.BOOK_URLS_FIELD)
    #章节url队列，储存爬取的章节url
    chap_queue = MongoQueue(book_config.CHA_URLS_TABLE,book_config.CHA_URLS_FIELD)

    D = Downloader(delay=delay, num_retries=num_retries, headers=headers, encoding=encoding, cache=cache)
    while True:
        try:
            url = book_queue.pop()
            try:
                html = D(url)
                # 解析功能--解析小说详情页并将小说详情储存到数据库中，返回其中的所有小说章节urls
                if scrape_callblack:
                    chap_links = scrape_callblack(url,html)
                    # 将章节url添加到urls队列中
                    [chap_queue.push(link) for link in chap_links]
                else:
                    #print '请添加回调处理函数'
                    break
            except ValueError as e:
                # 设置当前url状态为 ERROR
                book_queue.set_error(url)
                error_info = u'出现错误跳过当前url %s 信息为：%s ' % (url,e.message)
                error_logger.error(error_info)
        except KeyError as e:
            #print '处理完成',e
            conlose_logger.info(u'小说链接爬取已完成 ')
            break
        else:
            #正常处理完成，设置url状态为 已处理
            book_queue.complete(url)

def chpater_crwler(delay=5, num_retries=3, encoding='utf-8', headers=None, scrape_callblack=None, cache=None):
    """章节信息爬取，并储存到数据库
        :param  delay 请求间隔时间
        :param  num_retries 下载错误时重试次数
        :param  encoding 网页编码
        :param  headers HTTP请求头信息
        :param  scrape_callblack 回调函数，用于处理具体业务逻辑
        :param  cache 数据缓存
        :raise  ValueError 章节页解析失败则抛出
    """
    # 章节urls队列
    chap_queue = MongoQueue(book_config.CHA_URLS_TABLE, book_config.CHA_URLS_FIELD)
    D = Downloader(delay=delay, num_retries=num_retries, headers=headers, encoding=encoding, cache=cache)
    while True:
        try:
            url = chap_queue.pop()
            try:
                html = D(url)
                # 解析功能--解析小说章节页，获得章节内容，并储存到数据库中
                if scrape_callblack:
                    scrape_callblack(url,html)
                else:
                    #print '请添加回调函数'
                    break
            except ValueError as e:
                # 设置当前url状态为 ERROR
                chap_queue.set_error(url)
                error_info = u'出现错误跳过当前url %s 信息为：%s ' % (url,e.message)
                error_logger.error(error_info)
        except KeyError as e:
            conlose_logger.info(u'小说链接爬取已完成 ')
            break
        else:
            # 正常处理完成，设置url状态为 已处理
            chap_queue.complete(url)

if __name__ == "__main__":
    #link_crawler('http://www.baidu.com',headers={},scrape_callblack=scrape_callblack)
    #book_detail_crwler(headers={})
    chpater_crwler(headers={},scrape_callblack=chap_call.ChapterSpiderCallblack())