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

	def parse_item(self, response):
		url.append(response.url)

	def getItems(self):
		return url
