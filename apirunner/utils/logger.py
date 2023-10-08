import logging
import os
import time
from apirunner.config.setting import FILE_PATH
from logging.handlers import RotatingFileHandler  # 按文件大小滚动备份

log_dir = FILE_PATH['logs']
if not os.path.exists(log_dir):
    os.mkdir()
log_file = log_dir + r'\text_{}.log'.format(time.strftime("%Y%m%d"))

class Log():
    def get_logger(self):
        """获取logger对象"""
        logger = logging.getLogger(__name__)
        # 防止重复打印日志
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            log_format = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d -[%(module)s:%(funcName)s] - %(message)s')
            # 日志输出到指定文件，滚动备份日志
            # 日志输出到文件中的handler
            fh = RotatingFileHandler(filename=log_file, mode='a', maxBytes=5242880,
                                     backupCount=7,
                                     encoding='utf-8')  # maxBytes:控制单个日志文件的大小，单位是字节,backupCount:用于控制日志文件的数量

            fh.setLevel(logging.DEBUG)
            fh.setFormatter(log_format)
            # 将相应的handler添加在logger对象中
            logger.addHandler(fh)

            # 日志输出到控制台的handler
            sh = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)
            sh.setFormatter(log_format)
            logger.addHandler(sh)
        return logger

log = Log()
logger = log.get_logger()

