# -*- coding = utf-8 -*-
import urllib2
import re
import csv

DEFAULT_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

class Download():
	"""download webpage form website"""
	def __init__(self, user_agent=DEFAULT_AGENT,cache=None):
		self.user_agent = DEFAULT_AGENT
		self.cache=cache

	def __call__(self,url):
		result=None
		#the search result in cache
		if self.cache:
			try:
				result=self.cache[url]
			except KeyError as e:
				#url not in cache
				raise
			else:
				if 500<=result['code']<=600:
					# server error so ignore result from cache and re-download
					result=None

		if result is None:
			# result was not loaded from cache so still need to download
			headers={'User_Agent':self.user_agent}
			result=self.download(url,headers)
			if self.cache:
				# save result to cache
				self.cache[url]=result
		return result['html']

	def download(self,url,headers):
		request=urllib2.Request(url,headers=headers)
		try:
			response=urllib2.urlopen(request)
			html=response.read()
			code=response.code
		except urllib2.URLError as e:
			#print 'Download error',e.reason
			html=''
			if hasattr(e,'code'):
				code=e.code
			else:
				code=None
		return {'html':html,'code':code}
