#!/usr/bin/env python
#coding:utf-8
# 全局变量设置文件

import sys

VERSION = "1.0"
Site = "https://github.com/370040400/Ajatar"

#win32
IS_WIN = sys.platform 

#用于表示无效unicode编码
INVALID_UNICODE_CHAR_FORMAT = r"\x%02x"

UNICODE_ENCODING = "utf-8"

#插件列表
LIST_PLUGINS = ["subdomain", "find_service", "whatcms", "fuzz"]

GIT_REPOSITORY = "https://github.com/370040400/Ajatar.git"

ESSENTIAL_MODULE_METHODS = ["assign", "audit"]

#banner
#banners = 