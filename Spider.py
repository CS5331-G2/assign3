import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

url = []

class Crawler(CrawlSpider):
	name = "Crawler"
	allowed_domains = ['target.com']
	start_urls = ['http://target.com']

	rules = (
		Rule(LinkExtractor(), callback='parse_item', follow=True),
		)

	def parse_item(self, response):
		url.append(response.url)

	def getItems(self):
		return url
