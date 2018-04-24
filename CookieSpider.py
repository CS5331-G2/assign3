import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest

url = []

class Crawler(CrawlSpider):
	name = "Crawler"
	allowed_domains = ['ec2-54-251-169-51.ap-southeast-1.compute.amazonaws.com']
	start_urls = ['http://ec2-54-251-169-51.ap-southeast-1.compute.amazonaws.com:8080/', 
	'http://ec2-54-251-169-51.ap-southeast-1.compute.amazonaws.com:8081',
	'http://ec2-54-251-169-51.ap-southeast-1.compute.amazonaws.com:8083/']

	rules = (
		Rule(LinkExtractor(), callback='parse_item', follow=True),
		)

	def request(self, url, callback):
		request = scrapy.Request(url=url, callback='callback')
		request.cookies['cookie'] = 1
		return request

	def start_requests(self):
		for i, url in enumerate(self.start_urls):
			yield Request(url, callback=self.parse_item)

	def parse_item(self, response):
		# Extract All links in the particular response page
		links = LinkExtractor().extract_links(response)
		for link in links:
			is_allowed = False
			for allowed_domain in self.allowed_domains:
				if allowed_domain in link.url:
					is_allowed = True

			if is_allowed and link.url not in url:
				url.append(link.url)
				yield Request(link.url, callback=self.parse_item)
			elif is_allowed and response.url not in url:
				url.append(response.url)

	def getItems(self):
		return url
