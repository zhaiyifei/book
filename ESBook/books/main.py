#coding=utf-8
"""多进程版爬虫 """

import time
import link_crawler
import multiprocessing
import books.bookconfig as book_config
from books.util.tools import replace_img
from books.callblack.bookcallblack import BookSpiderCallblack
from books.callblack.bookdetailCallblack import BookDetailCallblack
from books.callblack.chapterCallblack import ChapterSpiderCallblack

def book_detail_crawler():
    """小说详情页爬取"""
    link_crawler.book_detail_crwler(headers={}, scrape_callblack=BookDetailCallblack())


def chpater_crwler():
    """章节页爬取"""
    link_crawler.chpater_crwler(headers={}, scrape_callblack=ChapterSpiderCallblack())

def process_crawler(func):
    """启动进程"""
    pool = multiprocessing.Pool(processes=8)
    for i in range(8):
        pool.apply_async(func)
    pool.close()
    pool.join()

def start():
    """启动爬虫"""
    #爬取小说url
    book_config.CONSOLE_LOGGER.info(u'开始 -- 爬取主页小说')
    url = 'http://www.biquge.com/'

    link_crawler.book_crawler(url,headers={},scrape_callblack=BookSpiderCallblack())
    time.sleep(10)
    start_time = time.time()
    #小说详情爬取
    #book_crawler = link_crawler.book_crawler
    book_config.CONSOLE_LOGGER.info(u'开始 -- 小说详情爬取')
    process_crawler(book_detail_crawler)
    print '耗时=== ',time.time()-start_time
    #替换不正常图片为默认封面图片
    replace_img()
    time.sleep(10)
    #章节信息爬取
    book_config.CONSOLE_LOGGER.info(u'开始 -- 章节详情爬取')
    process_crawler(chpater_crwler)

if __name__ == '__main__':

    start()