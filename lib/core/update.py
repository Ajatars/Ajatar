#!/usr/bin/env python

import os
import time
import subprocess
import locale
import re
from lib.core.data import paths,logger
from lib.core.common import dataToStdout,pollProcess,getSafeExString
from lib.core.settings import GIT_REPOSITORY
from lib.core.revison import getRevisionNumber

def updateProgram():
	success = False

	if not os.path.exists(os.path.join(path.Ajatar_ROOT_PATH,".git")):
		errMsg = "not a git repository. from GitHub (e.g. 'git clone --depth 1 https://github.com/370040400/Ajatar.git Ajatar')"
		logger.critical(errMsg)
	else:
		infoMsg = "updating latest development version from the GitHub repository"
		logger.info("\r[%s] [INFO] %s"%(time.strftime("%X"),infoMsg))

		debugMsg = "will try to update itself using 'git' command"
		logger.info(debugMsg)

		dataToStdout("\r[%s] [INFO] update in progress " % time.strftime("%X"))

	try:
		#创建进程stdin,stdout,stderr：分别表示程序的标准输入、标准输出、标准错误,cwd：用于设置子进程的当前目录,locale.getpreferredencoding()获取本地编码。
		process = subprocess.Popen("git checkout . && git pull %s HEAD" % GIT_REPOSITORY, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=paths.w9scan_ROOT_PATH.encode(locale.getpreferredencoding()))  # Reference: http://blog.stastnarodina.com/honza-en/spot/python-unicodeencodeerror/
		pollProcess(process,True) 
		stdout,stderr = process.communicate() #Communicate()返回一个元组
		success = not process.returncode #获取进程的返回值。如果进程还没有结束，返回None。
	except (IOError,OSError) as ex:
		success = False
		stderr = getSafeExString(ex)

	if success:
		logger.info("\r[%s] [INFO] %s the latest revision '%s'" % (time.strftime("%X"),"already at" if "Already" in stdout else "updated to", getRevisionNumber()))
	else:
		if "Not a git repository" in stderr:
			errMsg = "not a valid git repository. "
			errMsg += "from GitHub (e.g. 'git clone --depth 1 https://github.com/370040400/Ajatar.git sqlmap')"
			logger.critical(errMsg)
		else:
			logger.critical("update could not be completed ('%s')" % re.sub(r"\W+", " ", stderr).strip())

	if not success:
		if subprocess.mswindows:
			infoMsg = "for Windows platform it's recommended "
			infoMsg += "to use a GitHub for Windows client for updating "
			infoMsg += "purposes (http://windows.github.com/) or just "
			infoMsg += "download the latest snapshot from "
			infoMsg += "https://github.com/370040400/Ajatar"
		else:
			infoMsg = "for Linux platform it's required "
			infoMsg += "to install a standard 'git' package (e.g.: 'sudo apt-get install git')"

		#time.strftime("%X") 当前时间
		print("\r[%s] [INFO] %s"%(time.strftime("%X"),infoMsg))    