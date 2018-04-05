import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class Links(scrapy.Item):
	link = scrapy.Field()

class crawler(CrawlSpider):
	name = "crawler"
	allowed_domains = ['comp.nus.edu.sg']
	start_urls =['http://www.comp.nus.edu.sg']

	rules = (
		Rule(LinkExtractor(), callback='parse_item', follow=True),
		)

	def parse_item(self, response):
		item = Links()
		item['link'] = response.url
		yield item
