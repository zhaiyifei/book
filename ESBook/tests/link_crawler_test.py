#coding=utf-8
"""链接爬取模块测试"""
import books.link_crawler as link_crawler
from books.callblack.chapterCallblack import ChapterSpiderCallblack
from books.callblack.bookdetailCallblack import BookDetailCallblack
from books.callblack.bookcallblack import BookSpiderCallblack

def chpater_crwler_test():
    """章节信息测试"""
    link_crawler.chpater_crwler(headers={}, scrape_callblack=ChapterSpiderCallblack())

def book_detail_crwler_test():
    """详情页爬取测试"""
    link_crawler.book_detail_crwler(headers={},scrape_callblack=BookDetailCallblack())

def book_crawler_test():
    """小说主页爬取测试"""
    url = 'http://www.biquge.com/'
    link_crawler.book_crawler(url,headers={},scrape_callblack=BookSpiderCallblack())

if __name__ == '__main__':
    #book_crawler_test()
    book_detail_crwler_test()
    #chpater_crwler_test()