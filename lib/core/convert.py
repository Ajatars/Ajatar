#!/usr/bin/env python
#coding:utf-8
#from POC-T
#输入输出处理文件

import sys
from lib.core.settings import IS_WIN,UNICODE_ENCODING

def singleTimeWarnMessage(mseeage):
	#控制输出
	sys.stdout.write(message)
	sys.stdout.write("\n")
	sys.stdout.flush()

def stdoutencode(data):
	retVal = None

	try:
		data = data or ""

		if IS_WIN == "win32": #WIN平台
			output = data.encode(sys.stdout.encoding,"replace") #替换其中异常的编码

			if '?' in output and '?' not in data:
				warnMsg = "cannot properly display Unicode characters "
				warnMsg += "inside Windows OS command prompt "
				singleTimeWarnMessage(warnMsg)

			retVal = output
		else:
			retVal = data.encode(sys.stdout.encoding)
	except Exception:
		retVal = data.encode(UNICODE_ENCODING) if isinstance(data, str) else data

	return retVal