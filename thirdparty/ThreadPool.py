#!/usr/bin/env python
#coding:utf-8
#进程池，线程池

import threading
import time
import traceback
import random
import sys
from lib.core.data import logger

#兼容python23
if sys.version > '3':
	import queue as Queue
else:
	import Queue

class Ajatar_threadpool:

	def __init__(self,threadnum,func_scan,Isjoin = False):
		self.thread_count = self.thread_nums = threadnum #线程数
		self.sacn_count_lock = threading.Lock() #扫描线程锁
		self.thread_count_lock = threading.Lock() #线程锁
		self.load_lock = threading.Lock() #加载线程锁
		self.scan_count = 0
		self.isContinue = True
		self.func_scan = func_scan
		self.queue = Queue.Queue()
		self.isjoin = Isjoin

	def push(self,payload):
		self.queue.put(payload)

	def changeScanCount(self,num):
		self.scan_count_lock.acquire() #获得锁
		self.scan_count += num
		self.scan_count_lock.release() #释放锁

	def changeThreadCount(self,num):
		self.thread_count_lock.acquire()
		self.thread_count += num
		self.thread_count_lock.release()

	def run(self):
		th = []
		for i in range(self.thread_nums):
			t = threading.Thread(target=self.scan)
			t.setDaemon(True)#设置守护线程
			t.start()
			th.append(t)

		#Ctrl-C
		if self.isjoin:
			for tt in th:
				tt.join()#阻塞没个线程
		else:
			while 1:
				if self.thread_count > 0 and self.isContinue:
					time.sleep(0.01)
				else:
					break

	def stop(self):
		self.load_lock.acquire()
		self.isContinue = False
		self.load_lock.release()

	def scan(self):
		while 1:
			self.load_lock.acquire()
			if self.queue.qsize() >0 and self.isContinue:
				payload = self.queue.get() #从队列中获取payload
				self.load_lock.release()
			else:
				self.load_lock.release()
				break
			try:
				# POC在执行时报错如果不被处理，线程框架会停止并退出
				self.func_scan(payload)
				time.sleep(0.3)
			except KeyboardInterrupt:
				self.isContinue = False
				raise KeyboardInterrupt
			except Exception:
				errmsg = traceback.format_exc()
				self.isContinue = False
				logger.error(errmsg)

		# self.changeScanCount(-1)
		self.changeThreadCount(-1)
if __name__ == '__main__':
	def calucator(num):
		i = random.randint(1,100) #随机生成100里的整数
		u = num
		a = i * u
		if (a % 6 == 0):
			for x in range(5):
				print("new thread")

	p = Ajtar_threadpool(3,calucator)
	for i in range(100000):
		p.push(i)
	p.run()