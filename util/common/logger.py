# -*- coding: utf-8 -*-

# 日志文件操作模块

import logging
import sys

class log_base(object):
    """日志服务

    """
    def __init__(self,logger_name):
        logger = logging.getLogger(logger_name)
        formater = logging.Formatter('[PID:%(process)-5s] %(asctime)s %(message)s', '%Y/%m/%d %H:%M:%S')
        file_handler = logging.FileHandler("course.log")
        file_handler.setFormatter(formater)
        stream_handler = logging.StreamHandler(sys.stderr)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.setLevel(logging.DEBUG)
        self.logger = logger

    def err(self, log):
        self.logger.error("[ERR]\t%s"%log)

    def info(self, log):
        self.logger.info("[INF]\t%s"%log)

    def fatal(self, log):
        self.logger.fatal("[FTL]\t%s"%log)

    def warning(self, log):
        self.logger.warning("[WRN]\t%s"%log)

    def debug(self, log):
        self.logger.debug("[DBG]\t%s"%log)