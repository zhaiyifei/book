#coding=utf-8
"""bookDB 测试模块"""
from books.util.bookDB import BookDB

def bookDB_test():
    """测试 books_table和chapters_table的插入操作"""
    bookdb = BookDB()
    #books_table插入测试
    bookdb.insert_book({'book_id':'测试小说id'})
    #chapters_table插入测试
    bookdb.insert_chapter({'book_id':'测试小说id','chapter_id':'测试章节id'})

if __name__ == "__main__":
    bookDB_test()
