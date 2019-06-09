# -*- coding:utf8 -*-

import re
import threading
import requests
import Queue

file_path = 'lenovo.txt'
threading_num = 100
quit = Queue.Queue()
file_write = r'new_ly.txt'

def heavy(file_path):
    with open(file_path,'r') as f:
        informations = map(lambda x: x.strip(), f.readlines())
    # 剔除重复数据
    result = []
    regex = re.compile(r'(.*\.douyu\.com)')
    regex1 = re.compile(r'(.*\.lenovo\.com)')
    regex2 = re.compile(r'(.*\.lenovo\.com\.cn)')
    for i in informations:
        if re.findall(regex,i):
            i = re.search(regex,i).group()
        elif re.findall(regex1,i):
            i = re.search(regex1,i).group()
        elif re.findall(regex1,i):
            i = re.search(regex2,i).group()
        if i not in result:
            result.append(i)
            quit.put(i)



#多线程检测url存活
def check_url():
    while not quit.empty():
        url = quit.get()
        url = url + '/robots.txt'
        try:
            if 'http' not in url or 'https' not in url:
                url = 'http://' + url #+ '/robots.txt'
            requests.packages.urllib3.disable_warnings() #  忽略警告：InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised.
            content = requests.get(url, verify=False, allow_redirects=True, timeout=10)
            if content.status_code == 200:
                print(url)
                with open(file_write,'a+') as f:
                    f.write(url+'\n')
        except requests.RequestException as e:
            pass

if __name__ == '__main__':
    heavy(file_path)
    for i in range(threading_num):
        t = threading.Thread(target=check_url)
        t.start()
    
    