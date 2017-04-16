#coding=utf-8
"""小说详情解析 模块"""

import re
import os
import urlparse
from bs4 import BeautifulSoup
import books.bookconfig as book_config
from books.util.bookDB import BookDB
from books.util import downloaders


class BookDetailCallblack(object):
    """小说详情解析类
        解析小说详情页中：
            小说标签（玄幻，言情之类），小说标题，作者，最后更新时间，小说简介，小说章节url
        保存到数据库 格式：
            小说url，标题，作者，简介，更新时间，封面url，章节url
        封面图片
            封面图片保存到磁盘文档
    """

    def __init__(self):
        """初始化相关参数
            正则表达式 '>(.*?)>' 匹配小说标签"""
        #匹配小说标签
        self.math = re.compile('>(.*?)>')
        self.base_url = 'http://www.biquge.com/'
        #isBinary = True 下载二进制类型文件
        self.down = downloaders.Downloader(headers={},isBinary=True)
        self.console_logger = book_config.CONSOLE_LOGGER
        self.error_logger = book_config.ERROR_LOGGER
        self.book_db = BookDB()

    def __call__(self,url,html):
        """回调方法 回调函数 方法解析html，并将解析内容保存到数据库
            :param  url 小说详情页url,用于跟踪url对应的页面
            :param  html 小说详情页html
            :raise html页面不存在，则抛出 ValueError异常
            :return  小说详情页中的小说章节url list类型 """

        if html:
            soup = BeautifulSoup(html,'lxml')
            book_id = self.get_book_id(url)
            book_tag = self.get_book_tag(soup)
            book_title = self.get_book_title(soup)
            book_author,update_time = self.get_book_author_update_time(soup)
            book_summary = self.get_book_summary(soup)
            book_chapters = self.get_chapter_links(soup)
            book_img_path = self.get_book_img(soup,book_id)
            book_info = {
                'book_id':book_id,
                'book_tag':book_tag,
                'book_title':book_title,
                'book_author':book_author,
                'update_time':update_time,
                'book_summary':book_summary,
                'book_img_path':book_img_path
            }

            self.save_book_details(book_info)
            return book_chapters
        else:
            raise ValueError(u'html 页面不存在 ')

    def get_book_id(self, url):
        """从url中解析出小说id
                :param  url 小说详情页url
                :return  小说id 字符串类型
        """
        book_id = urlparse.urlsplit(url).path.strip('/').strip()
        return book_id

    def save_img(self,img_url, file_name, file_path=r'ESBook\data\img'):
        """保存图片到磁盘文件夹
            :param  img_url 图片url地址
            :param  file_name 图片名称
            :raise  产生IOError异常 则抛出  ValueError异常
            :return  返回保存到磁盘文件的图片的绝对路径
        """
        try:
            base_path = os.getcwd().split('ESBook')[0]
            file_path = ''.join([base_path, r'ESBook\data\img'])
            if not os.path.exists(file_path):
                #print '文件夹', file_path, '不存在，重新建立'
                self.console_logger.info(u'文件夹 ' + file_path + u' 不存在，重新建立')
                # os.mkdir(file_path)
                # 使用makedirs而不是使用mkdir 是因为 mkdir只能建立单级文件目录
                # makedirs可以建立多级文件目录,也可以建立单级文件目录
                # 单级文件目录：img
                # 多级文件目录：my/img
                os.makedirs(file_path)

            file_suffix = os.path.splitext(img_url)[1]
            filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
            context = self.down(img_url)
            #这个地方一定要用a+的文件打开方式，不然多进程的情况下回导致图片写入文件不完整。
            #因为图片是二进制数据，所以要选择ab模式
            #以a+方式open一个文件的时候，write文件是个原子操作，多进程之间不会出现交叉写的情况，
            #  并且write大小没有限制的，不受4k大小限制。
            #  write一个文件内核是加锁的，会保证原子执行。

            with open(filename,'ab+') as f:
                f.write(context)
            return filename
        except IOError as e:
            #print '文件操作失败', e
            raise ValueError(u'文件操作失败 ')

    def get_book_img(self,soup,book_id):
        """下载小说封面，保存到本地文件夹，小说封面名称为小说id名称,并返回当前小说封面文件路径
            :param  soup  BeautifulSoup对象
            :param  book_id 小说id
            :raise  ValueError 小说封面不存在则抛出ValueError异常
            :return  小说封面磁盘文件路径
        """
        img_div = soup.select('div#fmimg > img')
        if img_div:
            img_src = urlparse.urljoin(self.base_url,img_div[0]['src'])
            img_path = self.save_img(img_src,book_id)
            return img_path
        else:
            #print '小说封面不存在'
            raise ValueError(u'小说封面不存在 ')


    def get_book_tag(self,soup):
        """获得小说标签，玄幻，武侠之类的
            :param  soup  BeautifulSoup对象
            :raise  ValueError 小说标签不存在或者解析异常，则抛出ValueError异常
            :return  小说标签，失败则返回None
        """
        book_tag_div = soup.select('div.con_top')
        book_tag = None
        if book_tag_div:
            tag_string = list(book_tag_div[0].stripped_strings)[1]
            info = re.search(self.math, tag_string)
            if info:
                book_tag = info.group(1).strip()
            else:
                #print '小说标签解析失败---:'
                raise ValueError(u'小说标签解析失败 ')
        else:
            #print '小说标签获取失败----'
            raise ValueError(u'小说标签不存在 ')
        return book_tag

    def get_book_title(self,soup):
        """获得小说标题
            :param  soup  BeautifulSoup对象
            :raise   ValueError 小说标题不存在或者解析异常，则抛出ValueError异常
            :return  小说标题 失败则返回None"""

        book_title_div = soup.select('div#info > h1')
        book_title = None
        if book_title_div:
            # 使用get_text 返回 unicode 对象
            # .string 返回的是 NavigableString对象，保存到数据库时候 需要再次转换为python字符串才行。
            book_title = book_title_div[0].get_text()
        else:
            raise ValueError(u'小说标题不存在 ')
        return book_title

    def get_book_author_update_time(self,soup):
        """获得小说作者和更新时间
            :param  soup  BeautifulSoup对象
            :raise  ValueError 小说作者和更新时间不存在或者解析异常，则抛出ValueError异常
            :return 小说作者，更新时间，元组类型。失败则返回（None,None)
            """
        info_div = soup.select('div#info > p')
        author = None
        update_time = None
        if info_div:
            author = info_div[0].string.encode('utf-8').split('：')[1]
            update_time = info_div[2].string.encode('utf-8').split('：')[1]
        else:
            #print '作者，更新时间 不存在'
            # 如果获取的内容不存在，则说明网页获取不正确，pass掉，不在对当前页进行解析，记录url，异常信息，进行下一个页面的获取
            raise ValueError(u'小说 作者，更新时间 不存在 ')
        return (author, update_time)

    def get_book_summary(self,soup):
        """获得小说简介
            :param  soup  BeautifulSoup对象
            :raise  ValueError 小说简介不存在或者解析异常，则抛出ValueError异常
            :return  小说简介，失败则返回None
        """
        summary_div = soup.select('div#intro')
        summary = None
        if summary_div:
            summary = summary_div[0].get_text().strip()
        else:
            #print '小说简介不存在'
            raise ValueError(u'小说简介不存在 ')
        return summary

    def get_chapter_links(self,soup):
        """获得小说章节url
            :param  soup  BeautifulSoup对象
            :raise  ValueError 小说章节url不存在或者解析异常，则抛出ValueError异常
            :return  返回小说章节url list类型，失败则返回None"""

        book_chapter_div = soup.select('div#list dd > a')
        book_chapters = None
        if book_chapter_div:
            # 必须将set对象转换为list对象，MongoDB无法储存set对象。
            book_chapter_list = [urlparse.urljoin(self.base_url, a['href'])
                                 for a in book_chapter_div]
            book_chapters = list(set(book_chapter_list))
        else:
            raise ValueError(u'小说 章节url不存在 ')
        return book_chapters

    def save_book_details(self,book_info):
        """保存小说信息到数据库
            :param  小说详情信息"""

        self.book_db.insert_book(book_info)



if __name__ == '__main__':
    import  requests

    math = re.compile('>(.*?)>')

    url = 'http://www.biquge.com/18_18716/'
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html,'lxml')

    book_tag_div = soup.select('div.con_top')
    book_tag = None
    if book_tag_div:
        tag_string = list(book_tag_div[0].stripped_strings)[1]
        info = re.search(math, tag_string)
        if info:
            book_tag = info.group(1).strip()
            print book_tag
        else:
            # print '小说标签解析失败---:'
            raise ValueError(u'小说标签解析失败 ')
    else:
        # print '小说标签获取失败----'
        raise ValueError(u'小说标签不存在 ')



# def kaishi():
#     file_path = 'I:' + os.sep + 'myimg'
#     img_url = 'http://upload.jianshu.io/admin_banners/web_images/2474/259a36ccbca577c3064c68ab3c0f1834d77456d7.png'
#     save_img(img_url, 'jianshu', file_path=file_path)
# if __name__ == '__main__':
#     # import downloaders
#     #
#     # book_url = 'http://www.biquge.com/43_43821/'
#     # D = downloaders.Downloader(headers={})
#     # bookdetail = BookDetailCallblack()
#     # html = D(book_url)
#     # bookdetail(book_url,html)
#     img_url = 'http://upload.jianshu.io/admin_banners/web_images/2474/259a36ccbca577c3064c68ab3c0f1834d77456d7.png'
#     base_path = os.getcwd().split('ESBook')[0]
#     file_path = ''.join([base_path, r'ESBook\data\img'])
#     print 'file_path ',file_path
#     if not os.path.exists(file_path):
#         # print '文件夹', file_path, '不存在，重新建立'
#         # os.mkdir(file_path)
#         # 使用makedirs而不是使用mkdir 是因为 mkdir只能建立单级文件目录
#         # makedirs可以建立多级文件目录,也可以建立单级文件目录
#         # 单级文件目录：img
#         # 多级文件目录：my/img
#         print '创建文件夹 ',file_path
#         os.makedirs(file_path)
#     # 当前文件夹的绝对路径
#     abs_path = os.path.realpath(file_path)
#     print '绝对路径',abs_path
#     file_name = '我的图片'
#     file_suffix = os.path.splitext(img_url)[1]
#     filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
#     print filename

