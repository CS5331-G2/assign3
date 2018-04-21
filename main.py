from Helpers import Helper
from Endpoint import Endpoint

# Run the webspider, from the list of URLs obtained, build the Endpoints
# Assume the list below is the list of URLs crawled and returned to us.
crawledUrls = [
	"https://indianvisaonline.gov.in/evisa/Registration", 
	"https://indianvisaonline.gov.in/evisa/CompletePartially", 
	"https://indianvisaonline.gov.in/evisa/PaymentCheck", 
	"https://indianvisaonline.gov.in/evisa/PrintApplication"
]



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
