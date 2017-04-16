#coding=utf-8
"""数据库操作模块"""
import pymongo.errors
import books.bookconfig as book_config

class BookDB(object):
    """BookDB类 对books_table和chapters_table的插入操作 """
    def __init__(self):
        """获得 books_table 和 chapters_table数据库集合 连接"""
        self.books_table = book_config.BOOKS_TABLE
        self.chapters_table = book_config.CHAPTERS_TABLE


    def insert_book(self,book_info):
        """插入小说详情内容到数据库
            :param book_info  待插入book信息文档"""
        try:
            self.books_table.insert(book_info)
        except pymongo.errors.DuplicateKeyError as e:
            #对同一主键 或者唯一索引，进行重复插入，则会抛出这个异常，
            #并且插入失败，
            #避免对同一主键或者索引进行重复的插入。
            #print e
            pass

    def insert_chapter(self,chapter_info):
        """插入章节详情内容到数据库
            :param chapter_info  待插入章节信息文档"""
        try:
            self.chapters_table.insert(chapter_info)
        except pymongo.errors.DuplicateKeyError as e:
            # 对同一主键 或者唯一索引，进行重复插入，则会抛出这个异常，
            # 并且插入失败，
            # 避免对同一主键或者索引进行重复的插入。
            pass

if __name__ == '__main__':
    chapters_table = (
        book_config.CHA_URLS_TABLE)
    result = chapters_table.find({})
    print result.count(),'总数'
    result2 = chapters_table.find({'status':0})
    print result2.count(),'未爬取'