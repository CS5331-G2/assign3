from Helpers import Helper
from Endpoint import Endpoint

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



# ^ the above URLs should likely be crawled via a "GET" request,
# we log them down in the Endpoint object.
endpoints = []
for url in crawledUrls:
	endpoints.append(Endpoint(url, "GET"))


print "========================================================="
# We can then crawl all the endpoints to look for forms in each of them
forms = []
for endpoint in endpoints:
	forms.extend(Helper.form_scrapper(endpoint.url))

for form in forms:
	endpoints.append(form.get_endpoint())
	

print "========================================================="
print "Visited endpoints {"
for endpoint in endpoints:
	print endpoint
print "}"
