# -*- coding = utf-8 -*-
from pymongo import MongoClient,errors
import datetime

class Mongo_Queue:
	#possible states of a download
	OUTSTANDING,PROCESSING,COMPLETE=range(3)

	"""possible states fo a download"""
	def __init__(self, client=None,timeout=300):
		self.client=MongoClient() if client is None else client
		self.db=self.client.cache
		self.timeout=timeout
		if 'crawl_queue' in self.db.collection_names(include_system_collections=False):
			self.db.drop_collection('crawl_queue')
			print self.db.collection_names(include_system_collections=False)


	def __nonzero__(self):
		'''Returns True if there are more jobs to preocess'''
		record=self.db.crawl_queue.find_one({'status':{'$ne':self.COMPLETE}})
		return True if record else False

	def push(self,url,depth=0):
		'define the insert function, so that a new url can insert into a collection'
		'depth is the crawl depth in the same domain'
		try:
			self.db.crawl_queue.insert_one({'_id':url,'status':self.OUTSTANDING,'depth':depth})
		except errors.DuplicateKeyError as e:
			pass #this url as a id has aready in the queue

	def get_item(self,url):
		'define the get fuction'
		return self.db.crawl_queue.find_one({'_id':url})

	def pop(self):
		'Get a outstanding url from the queue and set its status to processing. if the queu is empty a KerError exception is raised.'
		record=self.db.crawl_queue.find_one_and_update({'status':self.OUTSTANDING},{'$set':{'status':self.PROCESSING,'timestamp':datetime.datetime.now()}})
		#couldn't find one then return None? I'm not sure about it.
		if record:
			return record['_id']
		else:
			self.repair()
			raise KeyError()


	def complete(self,url):
		self.db.crawl_queue.update_one({'_id':url},{'$set':{'status':self.COMPLETE}})
	
	def repair(self):
		'''Release stalled jobs that take too much time. we consider it as error and should reset it's status to OUTSTANDING'''
		record=self.db.crawl_queue.find_one_and_update({'timestamp':{'$lt':datetime.datetime.now()-datetime.timedelta(seconds=self.timeout)},'status':{'$ne':self.COMPLETE}},{'$set':{'status':self.OUTSTANDING}})
		if record:
			print 'Released:', record['_id']
		