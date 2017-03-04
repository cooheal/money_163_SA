# -*- coding = utf-8 -*-
import urllib2
import re
import csv
def download_page(url):
	headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
	request=urllib2.Request(url,headers=headers)
	try:
		html=urllib2.urlopen(request).read()
	except urllib2.URLError as e:
		#print 'Download error',e.reason
		html=None
	return html

def link_crawler(seed_url,link_regex_large,link_regex_small,max_depth=3):
	'Crawl from the given seed URL following links matchedly by link_regex'
	crawl_queue=[seed_url]
	seen={seed_url:0}
	#result_link=set()
	i=1
	csvFile=open('D:/Work/Projects/realestate/app/static/163_money.csv','wb')
	try:
		writer=csv.writer(csvFile)
		while  crawl_queue:
			url=crawl_queue.pop()
			depth=seen[url]
			if depth!=max_depth:
				html=download_page(url)
				if html:
					links=re.findall(link_regex_large,html)
					for link in links:
						if re.match(link_regex_small,link):
							print link
							#result_link.add(link)
							writer.writerow((i,link))
							i+=1
						else:
							#if not re.match(link_regex_exclude,link):
							if link not in seen:
								seen[link]=depth+1
								crawl_queue.append(link)
	finally:
		csvFile.close()
	#return result_link

if __name__=="__main__":
	url='http://baidu.com'
	print download_page(url)
	print link_crawler()
