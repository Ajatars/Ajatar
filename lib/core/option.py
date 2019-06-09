#!/usr/bin/env python
#coding:utf-8

import sys
import os
import logging
import time
from lib.core.data import paths, logger, urlconfig, Ajconfig
from lib.core.update import updateProgram
from lib.core.log import LOGGER
from lib.core.enums import CUSTOM_LOGGING
from lib.core.common import makeurl, printMessage
from lib.core.settings import LIST_PLUGINS
from lib.core.exception import ToolkitUserQuitException,ToolkitMissingPrivileges,ToolkitSystemException


def initOption(args):
	urlconfig.mutiurl = False
	urlconfig.url = []
	urlconfig.search = False
	urlconfig.usePlugin = False

	#初始化配置文件
	urlconfig.threadNum = int(Ajconfig.thread) #线程
	if urlconfig.threadNum is None:
		urlconfig.threadNum = 5
	urlconfig.deepMax = int(Ajconfig.crawlerDeep) #爬虫深度
	if urlconfig.deepMax is None:
		urlconfig.deepMax = 100

	setLoggingLevel(args)
	if args.banner:
		bannerOutput()
	elif args.update:
		checkUpdate()
	elif args.search:
		searchPlguin(args)
	elif args.u and args.plugin:
		urlRegister(args)
	guideRegister(args)

def bannerOutput():
	#只是查看扫描器banner
	sys.exit(0)

def setLoggingLevel(args):
	#日志文件处理函数
	filename = os.path.join(paths.Ajatar_Output_PATH,"log" + "_" + str(int(time.time()))+ ".txt")

	logger.info("Log file saved on %s" %filename)
	FILE_HANDLER = logging.FileHandler(filename) #日志设置文件为对象
	FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S") #输出格式
	FILE_HANDLER.setFormatter(FORMATTER)
	LOGGER.addHandler(FILE_HANDLER)

	if args.debug:
		LOGGER.setLevel(CUSTOM_LOGGING.DEBUG)#日志级别为DEBUG

def checkUpdate():
	#更新扫描器
	updateProgram()
	sys.exit(0)

def searchPlguin(args):
	#搜索插件
	urlconfig.search = True
	name = args.search
	path = paths.Ajatar_Plugin_PATH
	plugins = os.listdir(path) #遍历路径下的所有插件文件
	foder = []
	for p in plugins:
		if name in p:
			foder.append(p)
	if not foder:
		logger.info("Not found the exp of '%s'" % (name))
	for f in foder:
		files = os.listdir(os.path.join(path, f))#返回指定的文件夹包含的文件或文件夹的名字的列表
		logger.info("Found:%-8s Total:%-4d Files:%-10s" % (f, len(files), str(files)))

	sys.exit(0)
def urlRegister(args):
	#url处理
	url = args.u
	urlconfig.usePlugin = True
	urlconfig.plugin = args.plugin
	urlconfig.diyPlugin = [urlconfig.plugin]

	if url.startswith("@"):#判断是否是文件
		urlconfig.mutiurl = True
		filename = url[1:] #取文件名
		try:
			o = open(filename, "r").readlines()
			for u in o:
				u = makeurl(u.strip())#处理url
				urlconfig.url.append(u)
				printMessage(u)#获取url的信息
		except IOError:
			raise ToolkitMissingPrivileges("Filename:'%s' open faild" % fileName)
		if len(o) == 0:
			raise ToolkitMissingPrivileges("The target address is empty")
	else:#单个url处理
		urlconfig.url.append(makeurl(url))

def guideRegister(args):
	#向导模式 
	#有url 没选插件参数时
	if args.u and not args.plugin:
		inputUrl = args.u
		print('xsss')
		urlconfig.url.append(makeurl(inputUrl))
		printMessage('[Prompt] URL has been loaded:%d' % len(urlconfig.url))
		urlconfig.diyPlugin = ["find_service", "whatcms"] #插件选择
		printMessage("[Prompt] You select the plugins:%s" %(' '.join(urlconfig.diyPlugin)))

		urlconfig.scanport = False #端口扫描默认关闭
		urlconfig.find_service = True #服务信息扫描默认开启
		return True

	#有url 有选插件参数时
	if args.u and args.plugin:
		return False

	#无url 和插件参数时
	inputUrl = raw_input('[1] Input url > ') 
	if inputUrl == '':
		raise ToolkitSystemException("You have to enter the url")

	#输入为文件时:
	if inputUrl.startswith("@"):
		urlconfig.mutiurl = True
		filename = inputUrl[1:]
		try:
			o = open(filename, "r").readlines() #一行行读取
			for url in o:
				urlconfig.url.append(makeurl(url.strip()))
		except IOError:
			raise ToolkitSystemException("Filename:'%s' open faild" % fileName)
		if len(o) == 0:
			raise ToolkitSystemException("The target address is empty")
	else:
		urlconfig.url.append(makeurl(inputUrl))

	printMessage('[Prompt] URL has been loaded:%d' % len(urlconfig.url))
	printMessage("[Prompt] You can select these plugins (%s) or select all" % (' '.join(LIST_PLUGINS)))

	diyPlugin = raw_input("[2] Please select the required plugins > ")

	if diyPlugin.lower() == 'all':
		urlconfig.diyPlugin = LIST_PLUGINS #sessting里的设置插件
	else:
		urlconfig.diyPlugin = diyPlugin.strip().split(' ')
	urlconfig.scanport = False
	urlconfig.find_service = False
	#是否开启端口和服务器信息扫描
	if 'find_service' in urlconfig.diyPlugin:
		urlconfig.find_service = True
		input_scanport = raw_input('[2.1] Need you scan all ports ?(Y/N) (default N)> ')
		if input_scanport.lower() in ("y", "yes"):
			urlconfig.scanport = True