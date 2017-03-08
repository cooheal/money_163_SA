# -*- coding = utf-8 -*-
import re
import csv
import threading
import chardet
import multiprocessing
from mongo_cache import MongoCache
from download import Download
from mongo_queue import Mongo_Queue


def link_crawler(seed_url,link_regex_large,link_regex_small,max_depth=2,max_threads=5):
	'Crawl from the given seed URL following links matchedly by link_regex'
	print 'seed_ur',seed_url
	#crawl_queue=[seed_url]
	crawl_queue=Mongo_Queue()
	#seen={seed_url:0}#no need this seen for Mongo_Queue will take care of duplicate url
	#crawl_queue=Mongo_Queue.push(seed_url)
	crawl_queue.push(seed_url)
	depth=(crawl_queue.get_item(seed_url))['depth']
	print 'seedurldepth:',depth
	cache=MongoCache()
	D=Download(cache=cache)
	#result_links=set()
	csvFile=open('D:/Work/Projects/realestate/app/static/163_money.csv','wb')
	writer=csv.writer(csvFile)

	def process_queue():
		'extract the page_download part as a function, so that every tread can call it to download page'
		while True:
			try:
				url=crawl_queue.pop()
			except KeyError:
				#no url in crawl_queue
				break
			else:
				depth=(crawl_queue.get_item(url))['depth']
				'depth=128,129'
				#print depth
				if depth<=max_depth:
					html=D(url)
					links=re.findall(link_regex_large,html)

					for link in links:
						if re.match(link_regex_small,link):
							writer.writerow((link,''))
							#writer.writerow((link,''))
							print link
						else:
							crawl_queue.push(link,depth+1)
							#encoding=chardet.detect(link)
							#link=link.decode(encoding).encode('utf-8')
							#crawl_queue.push(link,depth+1)
							#seen[link]=depth+1
				crawl_queue.complete(url)
								
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

def process_link_crawler(*args,**kwargs):
	#num_cpus=multiprocessing.cpu_count()
	num_cpus=2
	print 'Starting {} processes'.format(num_cpus)
	processes=[]
	for i in range(num_cpus):
		p=multiprocessing.Process(target=link_crawler,args=args,kwargs=kwargs)
		p.start()
		processes.append(p)
	#wait for processes to complete
	for p in processes:
		#Block the calling thread until the process whose join() m3ethod is called terminates or until the optional timeout occurs.
		p.join()