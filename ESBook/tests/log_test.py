#coding=utf-8
"""日志测试模块，测试日志相关功能"""
from books.bookconfig import CONSOLE_LOGGER,ERROR_LOGGER
import time

def error_logger_test():
    """error logger 测试 输出error级别日志信息到日志文件并且输出到控制台。
        删除多于指定保留个数的日志文件
        日志信息写入当前目录下logs文件夹内"""
    ERROR_LOGGER.error('error logger 测试')
    time.sleep(65)
    ERROR_LOGGER.error('error logger 测试2')
    time.sleep(65)
    ERROR_LOGGER.error('error logger 测试3')

def console_logger_test():
    """console logger 测试 输出info级别日志信息到控制台"""

    CONSOLE_LOGGER.info('console_logger 测试')
    time.sleep(65)
    CONSOLE_LOGGER.info('console_logger 测试2')
    time.sleep(65)
    CONSOLE_LOGGER.info('console_logger 测试3')


if __name__ == '__main__':
    # #console logger 测试
    # console_logger_test()
    # #error_logger 测试
    # error_logger_test()
    import requests
    from bs4 import BeautifulSoup

    response = requests.get('http://www.biquge.com/')
    response.encoding = 'utf-8'
    html = response.text

    soup = BeautifulSoup(html,'lxml')
    a_tag = soup.find('div')
    print a_tag
    xxx = a_tag.find_all('li')
    print xxx


