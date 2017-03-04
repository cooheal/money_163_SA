# -*- coding = utf-8 -*-
import re
import download
url='http://www.163.com/'
html=download.download_page(url)
urls=re.findall('<a href="(.*?)">(.*?)</a>')
