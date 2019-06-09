#!/usr/bin/env python
#coding:utf-8
#变量类型文件 如日志，状态，类型.

class CUSTOM_LOGGING:
	SYSINFO = 9
	SUCCESS = 8
	ERROR = 7
	WARNING = 6
	DEBUG =5

class EXIT_STATUS:
	SYSETM_EXIT = 0
	ERROR_EXIT = 1
	USER_QUIT = 2

class OPTION_TYPE:
	BOOLEAN = "boolean"
	INTEGER = "integer"
	FLOAT = "float"
	STRING = "string"