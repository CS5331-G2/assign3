from Helpers import Helper
from Endpoint import Endpoint
from Spider import Crawler
from scrapy.crawler import CrawlerProcess

# Run the webspider, from the list of URLs obtained, build the Endpoints
# Assume the list below is the list of URLs crawled and returned to us.
spider = Crawler()
process = CrawlerProcess({
			'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
			})
process.crawl(spider)
process.start()
crawledUrls = spider.getItems()

# crawledUrls = [
# 	"https://indianvisaonline.gov.in/evisa/Registration", 
# 	"https://indianvisaonline.gov.in/evisa/CompletePartially", 
# 	"https://indianvisaonline.gov.in/evisa/PaymentCheck", 
# 	"https://indianvisaonline.gov.in/evisa/PrintApplication"
# ]



# ^ the above URLs should likely be crawled via a "GET" request,
# we log them down in the Endpoint object.
endpoints = []
for url in crawledUrls:
	endpoints.append(Endpoint(url, "GET"))

print "========================================================="
print "Visited endpoints {"
for endpoint in endpoints:
	print endpoint
print "}"


print "========================================================="
# We can then crawl all the endpoints to look for forms in each of them
forms = []
for endpoint in endpoints:
	forms.extend(Helper.form_scrapper(endpoint.url))

for form in forms:
	print form
