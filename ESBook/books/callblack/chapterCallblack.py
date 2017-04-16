#coding=utf-8
"""章节信息解析模块"""
import urlparse
from bs4 import BeautifulSoup
from books.util.bookDB import BookDB

class ChapterSpiderCallblack(object):
    """章节信息抓取回调"""
    def __init__(self):
        self.book_db = BookDB()

    def get_book_and_chapter_id(self, url):
        """获得小说id 和 章节id
            :param url  小说章节url
            :return （小说id，章节id） 元组类型"""
        info = urlparse.urlsplit(url).path.split('/')
        book_id = info[1]
        chapter_id = info[2].strip('.html')
        return (book_id, int(chapter_id))

    def get_chapter_name(self,soup):
        """获得章节名称
            :param  soup  BeautifulSoup对象
            :raise  章节标题不存在 则抛出ValueError异常
            :return 章节标题"""
        name_div = soup.select('div.bookname > h1')
        if name_div:
            chapter_name =name_div[0].get_text().strip()
            return chapter_name
        else:
            #print 'NO'
            raise ValueError(u'章节标题不存在 ')

    def get_charpter_txt(self,soup):
        """获得章节小说内容
            :param  soup  BeautifulSoup对象
            :raise  章节内容不存在则抛出 ValueError异常
            :return 章节内容
        """
        content = soup.select('div#content')
        if content:
            charpter_txt = unicode(content[0])
            return charpter_txt
        else:
            #print 'No'
            raise ValueError(u'章节小说内容不存在 ')

    def save_chapter(self,chapter_info):
        """保存章节信息到数据库
            :param  chapter_info 章节信息"""
        self.book_db.insert_chapter(chapter_info)

    def __call__(self, url,html):
        """回调函数
                :param  url 章节url
                :param  html 章节HTML
                :raise  章节HTML不存在 则抛出ValueError异常
        """
        if html:
            soup = BeautifulSoup(html,'lxml')
            chapter_name = self.get_chapter_name(soup)
            chapter_txt = self.get_charpter_txt(soup)

            book_id, chapter_id = (
                self.get_book_and_chapter_id(url))
            #保存到数据库
            #数据库格式如下：小说id，章节id（int)，章节名称，章节内容。
            chapter_info = {
                'book_id': book_id,
                'chapter_id': chapter_id,
                'chapter_name': chapter_name,
                'chapter_txt': chapter_txt
            }
            self.save_chapter(chapter_info)
            #return chapter_info
        else:
            raise ValueError(u'html 页面不存在 ')

