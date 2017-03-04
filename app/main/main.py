# -*- coding = utf-8 -*-
import datetime
import re
import csv
from download import download_page,link_crawler
start=datetime.datetime.now()
date=datetime.datetime.now().strftime('%y/%m%d')
url='http://www.163.com/'
html=download_page(url)
link_regex_large=re.compile('<a href="(http://money.163.com/.*?)"')
link_regex_small=re.compile('http://money.163.com/'+date+'.*\.html$')
#link_regex_exclude=re.compile('.*\.html.*')
#links=link_crawler(url,link_regex_large,link_regex_small)
link_crawler(url,link_regex_large,link_regex_small)
end=datetime.datetime.now()
process_time=(end-start).total_seconds()
print process_time
'''
csvFile=open('D:/Work/Projects/realestate/app/static/163_money.csv','wt')
try:
	writer=csv.writer(csvFile)
	writer.writerows(links)
finally:
	csvFile.close()
'''