# Ajatar 一个学习大佬的练手的扫描器，努力使它兼容双python
目前只能用python2.7

### Ajatar所有功能基于插件
插件编写格式同Bugscan标准</br>

插件功能:子域名爆破，大量fuzz,cms识别，waf识别，sql注入，xss，披露漏洞的利用插件

### 使用方法:
```
[命令行]
向导模式      python Ajatar.py 运行
选择特定插件  python Ajatar.py -u www.baidu.com -p [插件]
也可以先选url python Ajatar.py -u [url]
支持文件批量  python Ajatar.py -u $url.txt
```
### 最大化使用内置库
除非是刚刚装的python 
