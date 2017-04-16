#coding=utf-8
"""
    项目配置模块
        数据库配置
            mongodb数据库连接的创建

            urls_table集合的创建以及索引 book_url 的创建
                urls_table 小说url表单，储存爬取的小说url
            cha_urls_table集合的创建以及索引 chapter_url的创建
                章节url表单，储存爬取的小说章节url
            books_table集合的创建以及索引 book_id 的创建
                小说表单，储存爬取的小说详情内容
            chapters_table集合的创建以及联合索引 book_id -- chapter_id 的创建
                chapters_table 章节表单，储存爬取的小说章节内容

        日志配置
            consloe_logger 输出日志到控制台 info级别
            error_logger 输出日志到日志文件 和 控制台 error级别

        url状态 ：数据库集合中url的状态
            OUTSTANAING = 0  #未处理
            PROCESSING = 1   #待处理
            COMPLETE = 2     #已处理
            ERROR = 3        #产生异常的url
"""
import pymongo
from books.util.logger import MyLogger

OUTSTANAING = 0  # 未处理
PROCESSING = 1   # 待处理
COMPLETE = 2     # 已处理
ERROR = 3        # 产生异常的url

# 数据库连接创建
client = pymongo.MongoClient('localhost',27017)
book_db = client['book']

# 小说url表单，储存爬取的小说url
BOOK_URLS_TABLE = book_db['urls_table']
BOOK_URLS_FIELD = 'book_url'
BOOK_URLS_TABLE.create_index([(BOOK_URLS_FIELD,pymongo.DESCENDING)],unique=True)

# 章节url表单，储存爬取的小说章节url
CHA_URLS_TABLE = book_db['cha_urls_table']
CHA_URLS_FIELD = 'chapter_url'
CHA_URLS_TABLE.create_index([(CHA_URLS_FIELD,pymongo.DESCENDING)],unique=True)

# 小说表单，储存爬取的小说详情内容
BOOKS_TABLE = book_db['books_table']
BOOKS_FIELD = 'book_id'
BOOKS_TABLE.create_index([(BOOKS_FIELD,pymongo.DESCENDING)],unique=True)

# 章节表单，储存爬取的小说章节信息
# 小说id，章节id 联合索引
CHAPTERS_TABLE = book_db['chapters_table']
CHAPTERS_FIELD = 'chapter_id'
# 复合唯一索引，由book_id -- chapter_id 确认一条记录的唯一性
CHAPTERS_TABLE.create_index([(BOOKS_FIELD, pymongo.DESCENDING), (CHAPTERS_FIELD, pymongo.DESCENDING)], unique=True)

# 日志
# consloe_logger 输出日志到控制台 info级别
# error_logger 输出日志到日志文件 和 控制台 error级别
CONSOLE_LOGGER = MyLogger.getLogger('consolelogger')
ERROR_LOGGER = MyLogger.getLogger('errorlogger')
