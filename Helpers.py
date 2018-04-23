
class Helper:

	# This method retrieves all forms in from a given URL
	@staticmethod
	def form_scrapper(url):
		import requests
		from bs4 import BeautifulSoup
		from HtmlForm import HtmlForm
		
		# WARNING: SSL Verification has been intentionally disabled!
		parser = BeautifulSoup(requests.get(url, verify=False).text, "html.parser")
		forms = parser.findAll("form")
		form_list = []
		for f in forms:
			form_list.append(HtmlForm(url, f))
		
		print "[{0} Forms] <- {1}".format(len(form_list), url)
		return form_list

	@staticmethod
	def do_post_request(endpoint, dictHeaders, dictFormData):
		import requests
		return requests.post(endpoint.url, headers=dictHeaders, data=dictFormData)
		

	@staticmethod
	def do_get_request(endpoint, dictHeaders, dictFormData):
		import requests
		return requests.get(endpoint.url, headers=dictHeaders, data=dictFormData)
		

