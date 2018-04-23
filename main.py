from Helpers import Helper
from Endpoint import Endpoint
from AttackModule import AttackModule
from LfiAttackModule import LfiAttackModule
from RfiAttackModule import RfiAttackModule
from ShlCmdInjAttackModule import ShlCmdInjAttackModule
from AttackReport import AttackReport
from Spider import Crawler
from scrapy.crawler import CrawlerProcess

# disable verbosive logs from our libraries
import logging
logging.getLogger("requests").setLevel(logging.CRITICAL + 1)
logging.getLogger("urllib3").setLevel(logging.CRITICAL + 1)
logging.getLogger('scrapy').setLevel(logging.CRITICAL + 1)
logging.getLogger('scrapy').propagate = False

# Run the webspider, from the list of URLs obtained, build the Endpoints
print "========================================================="
print "Running web spider!"
print ""
spider = Crawler()
process = CrawlerProcess({
			'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
			})
process.crawl(spider)
process.start()
crawledUrls = spider.getItems()

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
# All attack modules inherit from the AttackModule class.
# By default, the attack() method is to be invoked to perform the
# respective attacks.
attack_modules = [
	#LfiAttackModule(), # add modules as you implement them here
	#RfiAttackModule(),
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
			print "Target: {0}".format(endpoint.url)
			module.attack(endpoint)
print ""

print "========================================================="
print "Trying to attack endpoints with query strings"
for endpoint in endpoints:
	if endpoint.has_query_string():
		for module in attack_modules:
			print "Target: {0}".format(endpoint.url)
			module.attack(endpoint)
print ""


print "========================================================="
print "Trying to attack remaining endpoints"
for endpoint in endpoints:
	if True not in (endpoint.is_form(), endpoint.has_query_string()):
		for module in attack_modules:
			print "Target: {0}".format(endpoint.url)
			module.attack(endpoint)
print ""


print "========================================================="
print "Total number of attacks: {0}".format(len(AttackReport.attacks))
for attack in AttackReport.attacks:
	print attack



