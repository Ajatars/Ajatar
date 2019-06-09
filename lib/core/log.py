#!/usr/bin/env python
#form POC-T
#扫描器日志记录文件

import logging
import sys
from lib.core.enums import CUSTOM_LOGGING

#设置记录类型
logging.addLevelName(CUSTOM_LOGGING.SYSINFO, "*")
logging.addLevelName(CUSTOM_LOGGING.SUCCESS, "+")
logging.addLevelName(CUSTOM_LOGGING.ERROR, "-")
logging.addLevelName(CUSTOM_LOGGING.WARNING, "!")
logging.addLevelName(CUSTOM_LOGGING.DEBUG, "DEBUG")
LOGGER = logging.getLogger("Ajatar") # 指定name

LOGGER_HANDLER = None

try:
	#输出颜色处理
	from thirdparty.ansistrm.ansistrm import ColorizingStreamHandler
	
	try:
		LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
		LOGGER_HANDLER.level_map[logging.getLevelName("*")] = (None, "cyan", False)
		LOGGER_HANDLER.level_map[logging.getLevelName("+")] = (None, "green", False)
		LOGGER_HANDLER.level_map[logging.getLevelName("-")] = (None, "red", False)
		LOGGER_HANDLER.level_map[logging.getLevelName("!")] = (None, "yellow", False)
		LOGGER_HANDLER.level_map[logging.getLevelName("DEBUG")] = (None, "white", False)
	except Exception:
		LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

except ImportError:
	LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

#设置日志格式
FORMATTER = logging.Formatter("\r[%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(CUSTOM_LOGGING.WARNING) #设置级别 可更改



class MY_LOGGER:
    @staticmethod
    def success(msg):
        return LOGGER.log(CUSTOM_LOGGING.SUCCESS, msg)

    @staticmethod
    def info(msg):
        return LOGGER.log(CUSTOM_LOGGING.SYSINFO, msg)

    @staticmethod
    def warning(msg):
        return LOGGER.log(CUSTOM_LOGGING.WARNING, msg)

    @staticmethod
    def error(msg):
        return LOGGER.log(CUSTOM_LOGGING.ERROR, msg)

    @staticmethod
    def critical(msg):
        return LOGGER.log(CUSTOM_LOGGING.ERROR, msg)
    
    @staticmethod
    def debug(msg):
        return LOGGER.log(CUSTOM_LOGGING.DEBUG, msg)

    @staticmethod
    def security_note(msg,k=''):
        MY_LOGGER.info(msg)
    
    @staticmethod
    def security_warning(msg,k=''):
        MY_LOGGER.warning(msg)
    
    @staticmethod
    def security_hole(msg,k=''):
        MY_LOGGER.success(msg)
    
    @staticmethod
    def security_info(msg,k=''):
        MY_LOGGER.info(msg)