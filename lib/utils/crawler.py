#!/usr/bin/env python
#coding:utf-8
#爬虫模块
# 爬到的文件丢给任务'spider_file' 爬虫完丢给任务`spider_end`

import re,urlparse
from thirdparty import hackhttp
from lib.core.data import Ajatar_hash_pycode,logger
from lib.utils import until
from lib.core.data import urlconfig

req = hackhttp.hackhttp()

class UrlManager(object):
	def __init__(self):
		#设置url两个集合
		self.new_urls = set()
		self.old_urls = set()

	def add_new_url(self,url):
		#判断url是否爬取过
		if url not in self.new_urls and url not in self.old_urls:
			self.new_urls.add(url)

	#对一些url的处理
	def add_new_urls(self,urls):
		if urls is None or len(urls) == 0:
			return
		for url in urls:
			self.add_new_url(url)

	def has_new_url(self):
		#判断是否还有url爬取
		return len(self.new_urls) != 0

	def get_new_url(self):
		#从未爬取过的url集合中取出一个url
		new_url = self.new_urls.pop()
		self.old_urls.add(new_url)
		return new_url

class SpiderMain(object):

	def __init__(self,root):
		self.urls = UrlManager()
		self.root = root
		self.deep = 0
		self.maxdeep = urlconfig.deepMax #爬虫最大深度
		self.SIMILAR_SET = set()
		self.domain = urlparse.urlparse(root).netloc
		self.IGNORE_EXT = ['jpg','png','gif','rar','pdf','doc'] #不爬取的文件

	def craw(self):
		#放入主站url到爬取集合
		self.urls.add_new_url(self.root)
		while self.urls.has_new_url() and self.maxdeep>self.deep and self.maxdeep > 0:
			new_url = self.urls.get_new_url()
			logger.debug("craw:" + new_url)
			try:
				#获取内容
				html = until.Ajatar_get(new_url)
				check(new_url,html)
			except:
				html = ''
			new_urls = self._parse(new_url,html)
			self.urls.add_new_urls(new_urls)
			self.deep = self.deep + 1

	def _parse(self,page_url,content):
		if content is None:
			return
		#匹配url正则
		webreg = re.compile('''<a[^>]+href=["\'](.*?)["\']''', re.IGNORECASE)
		urls = webreg.findall(content)
		_news = self._get_new_urls(page_url,urls)
		return _news

	def _judge(self,url):
		netloc = urlparse.urlparse(url).netloc
		#判断是否是主站url
		if (self.domain != netloc):
			return False
		# 判断url相似度
		if (self.url_similar_check(url) is False):
			return False

		#指定后缀判断
		ext = urlparse.urlparse(url)[2].split('.')[-1]
		if ext in self.IGNORE_EXT:
			return False
		return True

	def url_similar_check(self,url):
		#URL相似度分析当url路径和参数键值类似时，则判为重复
		
		url_struct = urlparse.urlparse(url)
		#参数排序
		query_key = '|'.join(sorted([i.split('=')[0] for i in url_struct.query.split('&')]))
		#根据hash比较相似度
		url_hash = hash(url_struct.path + query_key)
		if url_hash not in self.SIMILAR_SET:
			self.SIMILAR_SET.add(url_hash)
			return True
		return False

	def check_url(self,url):
		#替换回被转义的url参数
		url = url.replace("&amp;", "&")
		url = url.replace("#", "")
		url = url.replace(" ", "+")
		return url

	def _get_new_urls(self, page_url, links):
		#添加爬取到的新url
		new_urls = set()
		for link in links:
			new_url = link
			new_full_url = urlparse.urljoin(page_url, new_url)
			new_full_url = self.check_url(new_full_url)
			if (self._judge(new_full_url)):
				new_urls.add(new_full_url)
		return new_urls

def check(url,html = ''):
	#从字典中获取插件,进行爬虫
	for k, v in Ajatar_hash_pycode.iteritems():
		try:
			pluginObj = v["pluginObj"]
			service = v["service"]
			if(service == "spider_file"):
				pluginObj.audit(url,html)
		except Exception as errinfo:
			logger.error("spider plugin:%s errinfo:%s url:%s"%(k,errinfo,url))

def check_end():
	for k, v in Ajatar_hash_pycode.iteritems():
		try:
			pluginObj = v["pluginObj"]
			service = v["service"]
			if(service == "spider_end"):
				pluginObj.audit()
		except:
			pass

if __name__ == '__main__':
	u = "http://www.baidu.com/"
	s = SpiderMain(u)
	s.craw()