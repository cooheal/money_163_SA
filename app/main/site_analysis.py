# -*- coding = utf-8 -*-
import builtwith
import whois
def sit_analysis(url):
	'利用python相关模块分析网站技术及所有者信息'
	site=builtwith.parse(url)
	site.update(whois.whois(url))
	return site

if __name__=='__main__':
	url='http://money.163.com/'
	sit_analysis(url)