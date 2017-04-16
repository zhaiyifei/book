#coding=utf-8
"""下载功能测试模块"""
from books.util.downloaders import Downloader

def timeout_test():
    """下载超时测试"""
    url = 'http://www.biquge.com/44_44588/'
    Down = Downloader(headers={}, timeout=0.1)

    html = Down(url)
    print html

def down_500_test():
    """HTTP 500 状态码测试"""
    url = 'http://httpstat.us/500'
    Down = Downloader(headers={},timeout=20)

    html = Down(url)
    print html

def down_ok_test():
    """正常网页下载测试"""
    url = 'http://www.biquge.com/44_44588/'
    Down = Downloader(headers={})

    html = Down(url)
    print html


if __name__ == '__main__':
    #timeout_test()
    #down_500_test()
    down_ok_test()