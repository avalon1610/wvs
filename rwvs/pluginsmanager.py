import sys
import imp
from twisted.protocols import basic
from twisted.internet import stdio,reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log,signals
from spiders.rwvs_spider import RwvsSpider
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

def CheckCMS(url):
	from cms import cmslist
	
	url = url.rstrip('/')
	for c in cmslist:
		queue = []
		for url_info in c:
			info = url_info.split('------')
			if len(info) == 3:
				path,key,name = info
			else:
				path,regx,key,name = info
			uri = url+path
			queue.append(uri)

		print 'checking %s' % name
		results = []
		def show(x):
			code = x.getinfo(x.HTTP_CODE)
			print code, x.getinfo(x.EFFECTIVE_URL)
			if code == 200:
				results.append(x)

		curl.curlm(queue,show)
		for r in results:
			if r.content.getvalue().lower().find(key) != -1:
				print 'spot %s' % name
				return key
	
	return None

def SubDomainScan(url):
	domain = url.split(':')[1].strip('/')
	code,head,res,errcode,_,errstr=curl.curl('-d domain=%s&b2=1 http://i.links.cn/subdomain/' % domain)
	if code == 200:
		import lxml.html
		dom = lxml.html.fromstring(res.replace('\x00','').decode('utf-8', 'ignore'))
		domainlist = dom.xpath("//div[@class='domain']/a")
		for d in domainlist:
			print d.attrib['href']

def CheckService(url):
	SubDomainScan(url)
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

		CheckService(self.url)
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

# for test
def test():
	if len(sys.argv) < 2:
		return
	url = sys.argv[1]
	CheckService(url)

if __name__=='__main__':
	# main()
	test()
	