# -*- coding = utf-8 -*-
from pymongo import MongoClient,errors
import datetime

class Mongo_Queue:
	#possible states of a download
	OUTSTANDING,PROCESSING,COMPLETE=range(3)

	"""possible states fo a download"""
	def __init__(self, client=None,timout=300):
		self.client=MongoClient() if client is None else client
		self.db=self.client.cache
		self.timout=timout

	def __nonzero__(self):
		'''Returns True if there are more jobs to preocess'''
		record=self.db.crawl_queue.find_one({'status':{'$ne':self.COMPLETE}})
		return True if record else False

	def push(self,url):
		'define the insert function, so that a new url can insert into a collection'
		try:
			self.db.crawl_queue.insert_one({'_id':url,'status':self.OUTSTANDING})
		except errors.DumplicatedKeyError as e:
			pass #this url as a id has aready in the queue

	def pop(self):
		'Get a outstanding url from the queue and set its status to processing. if the queu is empty a KerError exception is raised.'
		record=self.db.crawl_queue.find_one_and_update({'_id':url},{'$set':{'status':self.PROCESSING,'timestamp':datetime.datetime.now()}})
		#couldn't find one then return None? I'm not sure about it.
		if record:
			return record['_id']
		else:
			raise KeyError()

	def complete(self,url):
		self.db.crawl_queue.update_one({'_id':url},{'$set':{'status':self.COMPLETE}})
	
	def repair(self):
		'''Release stalled jobs that take too much time. we consider it as error and should reset it's status to OUTSTANDING'''
		record=self.db.crawl_queue.find_one_and_update({'timestamp':{'$it':datetime.datetime.now()-timedate.timedelta(seconds=self.timeout)},'status':{'$ne':self.COMPLETE}},{'$set':{'status':self.OUTSTANDING}})
		if record:
			print 'Released:' record['_id']




		