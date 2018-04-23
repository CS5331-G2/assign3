import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

url = []

class Crawler(CrawlSpider):
	name = "Crawler"
	allowed_domains = ['www.wsb.com', 'target.com']
	start_urls = ['http://www.wsb.com', 'http://target.com']

	rules = (
		Rule(LinkExtractor(), callback='parse_item', follow=True),
		)

	def request(self, url, callback):
		request = scrapy.Request(url=url, callback=callback)
		request.cookies['cookie'] = 1
		return request

	def start_requests(self):
		for i, url in enumerate(self.start_urls):
			yield self.request(url, self.parse_item)

	def parse_item(self, response):
		url.append(response.url)

	def getItems(self):
		return url
