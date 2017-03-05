# -*- coding = utf-8 -*-
import datetime
from pymongo import MongoClient

class MongoCache:
	"""
	Wrapper around MongoDB to cache downloads
	"""
	def __init__(self, client=None,expires=datetime.timedelta(days=1)):
		"""
		client: mongo database client
		expires: timedelta of amount of time before a cache entry is considered expired
		"""
		# if a client object is not passed 
		# then try connecting to mongodb at the default localhost port 
		self.client = MongoClient('localhost', 27017) if client is None else client
		#create collection to store cached webpages,
		# which is the equivalent of a table in a relational database
		self.db = self.client.cache
		#expireAfterSeconds: <int> Used to create an expiring (TTL) collection.
		#MongoDB will automatically delete documents from this collection after <int> seconds.
		#The indexed field must be a UTC datetime or the data will not expire.
		self.db.webpage.create_index('timestamp', expireAfterSeconds=expires.total_seconds())

	def __contains__(self,url):
		'Should return true if item is in self, false otherwise.'
		try:
			self[url]
		except KeyError:
			return False
		else:
			return True

	def __getitem__(self,url):
		'get the html cache file of this url'
		record=self.db.webpage.find_one({'_id':url})
		if record:
			#return record['result']
			#record = {'result': result, 'timestamp': datetime.utcnow()}
			return record['result']
		else:
			raise KeyError(url + 'does not exist')

	def __setitem__(self,url,result):
		'save the result of this url'
		record = {'result': result, 'timestamp': datetime.datetime.utcnow()}
		self.db.webpage.update({'_id':url},{'$set':record},upsert=True)

	def clear(sef):
		self.db.webpage.drop()

if __name__=='__main__':
	cache=MongoCache()
	url='http://money.163.com/'
	print cache[url]
