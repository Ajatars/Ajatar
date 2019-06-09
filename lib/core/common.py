#!/usr/bin/env python
#coding:utf-8
# 共同函数调用文件

import sys,random,os,re,argparse,time
from urllib.parse import urlparse
from lib.core.settings import INVALID_UNICODE_CHAR_FORMAT#,banners
from lib.core.data import paths,logger
from lib.core.convert import stdoutencode
from lib.core.log import LOGGER_HANDLER
from thirdparty.termcolor.termcolor import colored
from thirdparty.colorama.initialise import init as winowsColorInit


def weAreFrozen():
	return hasattr(sys,"frozen") #判断sys是否有frozen属性

def getUnicode(value,encoding=None,noneToNull=False):
	#返回所提供值的unicode表示形式
	if noneToNull and value is None:
		return "NULL"

	#value 是否为unicode 或者 str时
	if isinstance(value,str): 
		return value
	elif isinstance(value,basestring):
		while True:
			try:
				return str(value,encoding or "utf-8")
			except UnicodeDecodeError as ex:
				try:
					return str(value,"utf-8")
				except:
					value = value[:ex.start] + "".join(INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
	elif isListLike(value): #value 为list时
		value = list(getUnicode(_,encoding,noneToNull) for _ in value)
		return value
	else:
		try:
			return str(value)
		except Exception as e:
			return str(str(value),errors="ignore")

def setPaths(rootPath):
	paths.Ajatar_ROOT_PATH = rootPath
	paths.Ajatar_Plugin_PATH = os.path.join(paths.Ajatar_ROOT_PATH,"plugins") #根目录/plugins
	paths.Ajatar_Output_PATH = os.path.join(paths.Ajatar_ROOT_PATH, "output")

def parser():

	parser = argparse.ArgumentParser(description="Ajatar scanner")
	parser.add_argument("--update", help="update Ajatar", action="store_true")
	parser.add_argument("--guide", help="Ajatar to guide", action="store_true")
	parser.add_argument(
		"--banner", help="output the banner", action="store_true")
	parser.add_argument("-u", help="url")
	parser.add_argument("-p", "--plugin", help="plugins")
	parser.add_argument("-s", "--search", help="find infomation of plugin")
	parser.add_argument("--debug", help="output debug info",
		action="store_true", default=False)
	return parser.parse_args()

# def Banner():
# 	banner = banners
# 	if not getattr(LOGGER_HANDLER, "is_tty", False):
# 		banner = re.sub("\033.+?m", "", banner)
# 	dataToStdout(banner)

def dataToStdout(data,forceOutput=False,bold=False,content_type=None):
	#处理输出到命令行

	if isinstance(data,str):
		message = stdoutencode(data)
	else:
		message = data
	sys.stdout.write(setColor(message.decode(), bold))
	try:
		sys.stdout.flush()
	except IOError:
		pass

def setColor(message,bold=False):
	retVal = message
	if message and getattr(LOGGER_HANDLER, "is_tty", False):  # colorizing handler
		if bold: #颜色开关
			retVal = colored(message, color=None, on_color=None, attrs=("bold",))
	return retVal

def unArrayizeValue(value):
	#如果是列表或元组本身，则使用iterable创建值
	"""
	>>> unArrayizeValue([u'1'])
	u'1'
	"""
	if isListLike(value):
		if not value:
			value = None
		elif len(value) ==1 and not isListLike(value[0]):
			value = value[0]
		else:
			#根据 匿名函数lambda是否为空 过滤
			_ = filter(lambda _: _ is not None, (_ for _ in flattenValue(value)))
			value = _[0] if len(_) >0 else None
	return value

def isListLike(value):
	#聚合列表，元祖，集合
	return isinstance(value, (list, tuple, set))

def flattenValue(value):
	"""
	Returns an iterator representing flat representation of a given value

	>>> [_ for _ in flattenValue([[u'1'], [[u'2'], u'3']])]
	[u'1', u'2', u'3']
	"""
	for i in iter(value): #iter() 函数用来生成迭代器。
		if isListLike(i):
			for j in flattenValue(i):
				yield j
		else:
			yield i
def pollProcess(process,suppress_errors=False):
	#线程运行状态检测
	"""
	Checks for process status (prints . if still running)
	"""

	while True:
		dataToStdout(".")
		time.sleep(1)

		returncode = process.poll() #用于检查子进程是否已经结束。设置并返回returncode属性

		if returncode is not None:
			if not suppress_errors:
				if returncode == 0:
					dataToStdout(" done\n")
				elif returncode < 0:
					dataToStdout("process terminated by signal %d\n" % returncode)
				elif returncode > 0:
					dataToStdout("quit unexpectedly with return code %d\n" % returncode)
			break

def getSafeExString(ex,encoding=None):
	"""
	安全的方法如何获得正确的异常报告字符串
	(Note: errors to be avoided: 1) "%s" % Exception(u'\u0161') and 2) "%s" % str(Exception(u'\u0161'))

	>>> getSafeExString(Exception('foobar'))
	u'foobar'
	"""
	retVal = ex
	if getattr(ex,"message",None):
		retVal = ex.message
	elif getattr(ex,"msg",None):
		retVal = ex.msg
	return getUnicode(retVal or "",encoding=encoding).strip()

def makeurl(url):
	#url 处理

	#判断url头
	prox = "http://"
	if (url.startswith("https://")):
		prox = "https://"
	if not (url.startswith("http://") or url.startswith("https://")):
		url = prox + url
	url_info = urlparse(url)

	if url_info.path:
		#scheme='http', netloc='www.cwi.nl:80', path='/xxxx/Python.html
		url = prox + url_info.netloc + url_info.path
		if not url.endswith("/"):#url末尾加/
			url = url + "/"
	else:#无path直接加/
		url = prox + url_info.netloc + "/"
	return url

def printMessage(msg):
	dataToStdout('\r' + msg + '\n\r')

def runningTime(time):
	sTime = round(time,2)#返回浮点数x的四舍五入值。
	mTime = round(time/60,2)
	timeStr = "%s min / %s seconds"%(str(mTime),str(sTime))
	return timeStr