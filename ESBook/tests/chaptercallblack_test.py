#coding=utf-8
"""章节爬取解析 测试模块"""
import requests
from books.callblack.chapterCallblack import ChapterSpiderCallblack

def chapter_test():
    url = 'http://www.biquge.com/23_23176/1983983.html'
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text

    chapter_call = ChapterSpiderCallblack()
    chapter_call(url, html)

if __name__ == "__main__":
    chapter_test()