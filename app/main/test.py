import sys
import urllib2
import chardet

html=urllib2.urlopen('http://money.163.com').read()
print sys.getdefaultencoding()
print type(html)
print chardet.detect(html)
print chardet.detect(html.decode('gbk').encode('utf-8'))
html=''
print chardet.detect(html)