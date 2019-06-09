#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
# from sqlmap

import sys

PYVERSION = sys.version.split()[0] #获取Python version

if PYVERSION <= "3":# or PYVERSION < "2.6":
	exit("Python version detected %s . You must use version 3.x" % PYVERSION)