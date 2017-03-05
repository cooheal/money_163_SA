# -*- coding = utf-8 -*-
import re
import csv
from mongo_cache import MongoCache
from download import Download

def link_crawler(seed_url,link_regex_large,link_regex_small,max_depth=1):
	'Crawl from the given seed URL following links matchedly by link_regex'
	crawl_queue=[seed_url]
	seen={seed_url:0}

	cache=MongoCache()
	D=Download(cache=cache)
	i=1
	csvFile=open('D:/Work/Projects/realestate/app/static/163_money.csv','wb')
	try:
		writer=csv.writer(csvFile)
		while  crawl_queue:
			url=crawl_queue.pop()
			depth=seen[url]
			if depth!=max_depth:
				html=D(url)
				if html != '':
					links=re.findall(link_regex_large,html)
					#links=link_regex_large.findall(html)
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
