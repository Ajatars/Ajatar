#!/usr/bin/env python
#coding:utf-8
#扫描器执行文件

import time
import sys
from lib.core.data import logger,urlconfig
from lib.core.exploit import Exploit_run
from lib.core.settings import LIST_PLUGINS
from lib.utils import crawler

def pluginScan():
	#检测是否选择插件
	if not urlconfig.usePlugin:
		return False
	urlconfig.scanport = False
	urlconfig.find_service = False
	urlconfig.diyPlugin = LIST_PLUGINS
	print(urlconfig.diyPlugin)
	startTime = time.clock()
	e = Exploit_run(urlconfig.threadNum)
	for u in urlconfig.url:
		logger.info('ScanStart Target:%s' % u)
		e.setCurrentUrl(u)
		e.load_modules(urlconfig.plugin, u)
		e.run()
		time.sleep(0.01)
	endTime = time.clock()
	urlconfig.runningTime = endTime - startTime
	#e.report()
	sys.exit()

def webScan():
	startTime = time.clock()
	e = Exploit_run(urlconfig.threadNum)

	for url in urlconfig.url:
		logger.info('ScanStart Target:%s' %url)
		e.setCurrentUrl(url)
		e.load_modules("www",url)
		e.run()
		if not urlconfig.mutiurl:
			#爬虫
			e.init_spider()
			s = crawler.SpiderMain(url)
			s.craw()
		time.sleep(0.1)
	endTime = time.clock()
	urlconfig.runningTime = endTime - startTime
	#e.report()