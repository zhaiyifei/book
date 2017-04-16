#coding=utf-8
"""urls消息队列模块"""
import datetime
from pymongo import errors
import books.bookconfig as book_config


class MongoQueue(object):
    """MongoQueue类 基于mongodb的urls队列
        定义了urls的四种状态信息
            OUTSTANAING = 0   未处理
            PROCESSING = 1    待处理
            COMPLETE = 2      已处理
            ERROR = 3         产生异常的url
        当添加一个新url是，其状态为 OUTSTANAING,
        当从队列中取出url准备下载时，其状态为 PROCESSING
        当url下载完成时，其状态为 COMPLETE
        当url处理中（包括下载以及后续解析下载的html）产生异常是，其状态为 ERROR"""

    OUTSTANAING = book_config.OUTSTANAING  # 未处理
    PROCESSING = book_config.PROCESSING  # 待处理
    COMPLETE = book_config.COMPLETE  # 已处理
    ERROR = book_config.ERROR  # 产生异常的url

    def __init__(self, db_table,table_field,timeout=300, mgDB=None):
        """初始化队列
            :param  db_table 需要操作的mongodb数据库集合
            :param  table_field 数据库集合字段
            :param  timeout url处理时间，如果处理时间大于设定值，则url状态重新设置为OUTSTANAING
            """
        self.crawl_queue = db_table
        self.timeout = timeout
        self.table_field = table_field
        self.console_logger = book_config.CONSOLE_LOGGER

    def __nonzero__(self):
        """查询数据库中是否有状态为 OUTSTANAING 的未处理url
            __nonzero__ 用于将类转换为布尔值。通常在用类进行判断和将类转换成布尔值时调用
            例如 if 对象 相当于 if 对象.__nonzero__()
            :return 如果存在未处理url则返回True,否则返回False"""

        record = self.crawl_queue.find_one(
            {'$or': [{'status': {'$ne': self.COMPLETE}}, {'status': {'$ne': self.ERROR}}]})
        return True if record else False

    def push(self, url):
        """添加一个url到队列中，设置url状态为 未处理
            :param  url 添加到队列的url"""
        try:
            self.crawl_queue.insert(
                {self.table_field: url, 'status': self.OUTSTANAING}
            )
        except errors.DuplicateKeyError as e:
            pass

    def pop(self):
        """取得一个url，并更新url状态为待处理
            :return 一个未处理url
            :raise 没有未处理url则抛出KeyError异常"""
        record = self.crawl_queue.find_and_modify(
            query={'status': self.OUTSTANAING},
            update={'$set': {'status': self.PROCESSING, 'wait_time': datetime.datetime.now()}}
        )
        if record:
            return record[self.table_field]
        else:
            self.repair()
            raise KeyError()

    def repair(self):
        """重置url状态为 未处理"""
        record = self.crawl_queue.find_and_modify(
            query={
                'wait_time': {'%lt': datetime.datetime.now() - datetime.timedelta(seconds=self.timeout)},
                'status': {'$ne': self.COMPLETE},
            },
            update={'$set': {'status': self.OUTSTANAING}}
        )
        if record:
            #print '重置url状态', record[self.table_field]
            self.console_logger.info(u'重置 url : ' + record[self.table_field] + u' 状态')

    def complete(self, url):
        """更新url状态为 已处理"""
        self.crawl_queue.update({self.table_field: url}, {'$set': {'status': self.COMPLETE}})

    def set_error(self, url):
        """更新url状态，处理异常URL"""
        self.crawl_queue.update({self.table_field: url}, {'$set': {'status': self.ERROR}})

