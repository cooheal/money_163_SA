# -*- coding = utf-8 -*-
import re
import csv
import threading
from mongo_cache import MongoCache
from download import Download


def link_crawler(seed_url,link_regex_large,link_regex_small,max_depth=2,max_threads=5):
	'Crawl from the given seed URL following links matchedly by link_regex'
	crawl_queue=[seed_url]
	seen={seed_url:0}
	cache=MongoCache()
	D=Download(cache=cache)
	result_links=set()
	csvFile=open('D:/Work/Projects/realestate/app/static/163_money.csv','wb')
	writer=csv.writer(csvFile)

	def process_queue():
		'extract the page_download part as a function, so that every tread can call it to download page'
		while True:
			try:
				url=crawl_queue.pop()
			except IndexError:
				break
			else:
				depth=seen[url]
				if depth!=max_depth:
					html=D(url)
					links=re.findall(link_regex_large,html)

					for link in links:
						if re.match(link_regex_small,link):
							writer.writerow((link,''))
							#writer.writerow((link,''))
							print link
						else:
							#if not re.match(link_regex_exclude,link):
							if link not in seen:
								seen[link]=depth+1
								crawl_queue.append(link)
								
	threads=[]
	while crawl_queue or threads:
		while len(threads)<max_threads and crawl_queue:
			#can start some more threads
			thread=threading.Thread(target=process_queue)
			#daemon's value must be set before start(), or RuntimeError will rarise. set deamon=Ture ,so that main thread can exit when receieve ctrl-c
			thread.setDaemon(True)
			thread.start()
			threads.append(thread)

		for thread in threads:
			if not thread.is_alive():
				#remove the stopped threads
				threads.remove(thread)
	csvFile.close()
