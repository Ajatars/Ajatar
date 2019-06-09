#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import os
import sys

from distutils.version import LooseVersion
from lib.core.common import (weAreFrozen,getUnicode,setPaths,parser)#,Banner
from lib.core.data import logger,paths
from lib.core.settings import IS_WIN, VERSION
from thirdparty.colorama.initialise import init as winowsColorInit
from lib.utils.configfile import configFileParser
from lib.core.option import initOption
from lib.core.engine import pluginScan, webScan

sys.dont_write_bytecode = True  # 不生成pyc

try:
	__import__("lib.utils.versioncheck")  #检测 python version
except ImportError:
	exit("[!]Please install python version for 3.x")

def modulePath():

	try:
		_ = sys.executable if weAreFrozen() else __file__  #sys.executable 返回的是py2.exe的路径
	except NameError:
		_ = inspect.getsourcefile(modulePath) #返回object的python源文件名
    
    #os.path.dirname  获取py2.exe上一层文件路径
    #getUnicode()返回unicode编码过的路径
	return getUnicode(os.path.dirname(os.path.realpath(_)),encoding=sys.getfilesystemencoding())

def checkEnvironment():
	try:
		os.path.isdir(modulePath()) #os.path.isdir()用于判断对象是否为一个目录
	except UnicodeEncodeError:
		errMsg = "Unable to parse path information, please move another path"
		logger.critical(errMsg) #记录路径解析错误情况
		raise SystemExit


def main():
	#主函数

	checkEnvironment()#检测环境
	setPaths(modulePath()) #初始化一些绝对路径,参数为根目录

	#参数设置
	args = parser()
	
	if IS_WIN == 'win32':#win 初始化
		winowsColorInit()
	#Banner()

	try:
		configFileParser(os.path.join(paths.Ajatar_ROOT_PATH, "config.conf")) #配置文件参数处理
		initOption(args) #初始化参数
		#pluginScan() #插件函数
		webScan() #扫描函数
	except Exception as e:
		raise e

if __name__ == '__main__':
 	main() 