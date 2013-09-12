from urlparse import urlparse
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from rwvs.items import DmozItem

class DmozSpider(BaseSpider):
	name = 'dmoz'
	def __init__(self,**kw):
		super(DmozSpider,self).__init__(**kw)
		url = kw.get('url') or kw.get('domain')
		if not url.startswith('http://') and not url.startswith('https://'):
			url = 'http://%s/' % url

		self.url = url
		self.allowed_domains = [urlparse(url).hostname.lstrip('www.')]
		self.start_urls = [
			'http://www.dmoz.org/Computers/Programming/Languages/Python/Books/',
			'http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/'
		]
		self.link_extractor = SgmlLinkExtractor()
		self.cookies_seen = set()

	# def start_request(self):
	# 	return [Request(self.url,callback=self.parse)]

	def parse(self,response):
		hxs = HtmlXPathSelector(response)
		sites = hxs.select('//ul/li')
		items = []
		for site in sites:
			item = DmozItem()
			title = site.select('a/text()').extract()
			link = site.select('a/@href').extract()
			desc = site.select('text()').extract()
			print 'title',title
			print 'link',link
			print 'desc',desc