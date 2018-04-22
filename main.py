from Helpers import Helper
from Endpoint import Endpoint
from AttackModule import AttackModule
from LfiAttackModule import LfiAttackModule
from RfiAttackModule import RfiAttackModule
from ShlCmdInjAttackModule import ShlCmdInjAttackModule
from Spider import Crawler
from scrapy.crawler import CrawlerProcess

# Run the webspider, from the list of URLs obtained, build the Endpoints
# Assume the list below is the list of URLs crawled and returned to us.
crawledUrls = [
	"http://www.wsb.com", 
	"http://www.wsb.com/index.html.orig", 
	"http://www.wsb.com/Assignment2/", 
	"http://www.wsb.com/Assignment2/sample/sample.php", 
	"http://www.wsb.com/Assignment2/case01.php",
	"http://www.wsb.com/Assignment2/case02.php",
	"http://www.wsb.com/Assignment2/case03/case03.php",
	"http://www.wsb.com/Assignment2/case04.php",
	"http://www.wsb.com/Assignment2/case05.php",
	"https://www.wsb.com/Assignment2/case06.php",
	"http://www.wsb.com/Assignment2/case07.php",
	"http://www.wsb.com/Assignment2/case08.php",
	"http://www.wsb.com/Assignment2/case09.php",
	"http://www.wsb.com/Assignment2/case10-2.php",
	"http://www.wsb.com/Assignment2/case10.php",
]
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
print "Crawled {0} endpoints!".format(len(endpoints))
print ""


print "========================================================="
print "Revisiting endpoints to check if forms are present"
# We can then crawl all the endpoints to look for forms in each of them
forms = []
for endpoint in endpoints:
	forms.extend(Helper.form_scrapper(endpoint.url))

for form in forms:
	endpoints.append(form.get_endpoint())



print "========================================================="
print "Selected attack modules:"
attack_modules = [
	LfiAttackModule(),
	RfiAttackModule(),
	ShlCmdInjAttackModule()
]
for module in attack_modules:
	print module
print ""

print "========================================================="
print "Trying to attack endpoints with forms"
for endpoint in endpoints:
	if endpoint.is_form():
		for module in attack_modules:
			module.attack(endpoint)
print ""

print "========================================================="
print "Trying to attack endpoints with query strings"
for endpoint in endpoints:
	if endpoint.has_query_string():
		for module in attack_modules:
			module.attack(endpoint)
print ""



#print "========================================================="
#print "Visited endpoints {"
#for endpoint in endpoints:
#	print endpoint
#print "}"
