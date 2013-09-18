import sys
import imp
from twisted.protocols import basic
from twisted.internet import stdio,reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log,signals
from rwvs.spiders.rwvs_spider import RwvsSpider
import curl

def closesession(fn):
	def close(*args):
		var = args
		fn(var)
		exit(0)
	return close

@closesession
def security_note(str):
	print str 

@closesession
def security_info(str):
	print str

@closesession
def security_warning(str):
	print str

@closesession
def security_hole(str):
	print str

def CheckCMD(url):
	import cms
	for c in cmslist:
		path,key,name = c.split('------')
		uri = url + path
		code,_,res,errcode,_,errstr = curl.curl(uri)
		if code != 200:
			continue
		if res.find(key) != -1:
			print 'spot %s' % name
			break

def CheckService(url):
	service = CheckCMS(url)

	# spider = RwvsSpider(url=url)
	# crawler = Crawler(Settings())
	# crawler.configure()
	# crawler.crawl(spider)
	# crawler.start()
	return service

class PluginLauncher(basic.LineReceiver):
	from os import linesep as delimiter
	def __init__(self,mod,url):
		self.mod = mod
		self.url = url

	def connectionMade(self):
		try:
			module = __import__('plugins.%s' % self.mod,fromlist=['audit'])
		except ImportError:
			geterror('plugin %s not found.' % self.mod)
			return
		audit = getattr(module,'audit')
		assign = getattr(module,'assign')

		CheckService(url)
		try:
			if assign:
				audit(self.url)
		except Exception,e:
			print e.args
			exit(0)

	def dataReceived(self,data):
		if data == 'Abort':
			print data
			if reactor.running:
				reactor.stop()
		
def main():
	if len(sys.argv) < 3:
		return
	mod = sys.argv[1]
	url = sys.argv[2]

	stdio.StandardIO(PluginLauncher(mod,url))
	reactor.run()

if __name__=='__main__':
	main()
	