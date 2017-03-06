'download webpage from website using url'
# -*- coding = utf-8 -*-
import urllib2
import re
import datetime
import time

DEFAULT_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
DEFAULT_DELAY=5

class Download():
	"""download webpage form website"""
	def __init__(self, user_agent=DEFAULT_AGENT,cache=None,delay=DEFAULT_DELAY):
		self.user_agent = DEFAULT_AGENT
		self.cache=cache
		self.throttle=Throttle(delay)

	def __call__(self,url):
		result=None
		#the search result in cache
		if self.cache:
			try:
				result=self.cache[url]
			except KeyError as e:
				#url not in cache
				pass
			else:
				if 500<=result['code']<=600:
					# server error so ignore result from cache and re-download
					result=None

		if result is None:
			# result was not loaded from cache so still need to download
			headers={'User_Agent':self.user_agent}
			self.throttle.wait(url)
			result=self.download(url,headers)

			if self.cache:
				# save result to cache
				self.cache[url]=result
		return result['html']

	def download(self,url,headers):
		request = urllib2.Request(url,headers=headers)
		try:
			response = urllib2.urlopen(request)
			html = response.read()
			html=html.decode('gbk').encode('utf-8')
			code = response.code
		except urllib2.URLError as e:
			#print 'Download error',e.reason
			html = ''
			if hasattr(e,'code'):
				code = e.code
			else:
				code = None
		return {'html':html,'code':code}

class Throttle:
	"""Throttle downloading by sleeping between requests to same domain"""
	def __init__(self, delay):
		self.delay = delay
		'amount of delay between downloads for each domain'
		self.domains = {}
	def wait(self,url):
		domain=urllib2.urlparse.urlparse(url).netloc
		last_accessed=self.domains.get(domain)
		if self.delay>0 and last_accessed is not None:
			#sleep_secs=(self.delay-datetime.datetime.now-last_accessed).total_seconds()
			sleep_secs=self.delay-(datetime.datetime.now()-last_accessed).seconds
			if sleep_secs>0:
				#if the sleep_secs is biger than 0, then need to sleep for sleep_secs seconds
				print sleep_secs
				time.sleep(sleep_secs)
		#update the last access_time of every domain
		self.domains[domain]=datetime.datetime.now()