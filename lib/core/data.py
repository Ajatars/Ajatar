#!/usr/bin/env python
#coding:utf-8
# from sqlmap
#数据类型处理文件

from lib.core.datatype import AttribDict
from lib.core.log import MY_LOGGER

logger = MY_LOGGER

#paths
paths = AttribDict()

#cmder
cmdLineOptions = AttribDict()

#urlconfig
urlconfig = AttribDict()
Ajconfig = AttribDict()

#plugins pycode hash
Ajatar_hash_pycode = dict()
