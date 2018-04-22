import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

url = []

class Crawler(CrawlSpider):
	name = "Crawler"
	allowed_domains = ['indianvisaonline.gov.in']
	start_urls =['https://indianvisaonline.gov.in/evisa/Registration']

	rules = (
		Rule(LinkExtractor(), callback='parse_item', follow=True),
		)

	def parse_item(self, response):
		url.append(response.url)

	def getItems(self):
		return url
