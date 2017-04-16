#coding=utf-8
"""日志模块 对logging的简单封装"""

import os
import logging
import logging.config

class MyLogger():
    """日志类 加载配置文件并获得logger"""

    log_instance = None
    @staticmethod
    def initLogConf():
        """从当前目录加载日志配置文件"""
        current = os.path.dirname(__file__)
        logging.config.fileConfig(current+os.path.sep+'logging.conf')

    @staticmethod
    def getLogger(name=''):
        """获得logger
            :param name  logger名称，默认获得root logger"""
        if MyLogger.log_instance == None:
            MyLogger.initLogConf()
        MyLogger.log_instance = logging.getLogger(name)
        return MyLogger.log_instance
