# -*- coding = utf-8 -*-
import datetime
import re
import download
import link_crawler
import csv
import multiprocessing

if __name__=='__main__':
	#multiprocessing.freeze_support()
	start=datetime.datetime.now()
	date=start.strftime('%y/%m%d')
	url='http://money.163.com/'
	link_regex_large=re.compile('<a href="(http://money.163.com/.*?)"')
	link_regex_small=re.compile('http://money.163.com/'+date+'.*\.html$')

	link_crawler.process_link_crawler(url,link_regex_large,link_regex_small,max_depth=2,max_threads=5)
	end=datetime.datetime.now()
	process_time=(end-start).total_seconds()
	print process_time
'''
csvFile=open('D:/Work/Projects/realestate/app/static/163_money.csv','wb')
try:
	writer=csv.writer(csvFile)
	for each in list(result_links):
		writer.writerows((i,each))
finally:
	csvFile.close()
'''