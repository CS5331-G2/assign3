
class Helper:

	# This method retrieves all forms in from a given URL
	@staticmethod
	def form_scrapper(url):
		import requests
		from bs4 import BeautifulSoup
		from HtmlForm import HtmlForm

		parser = BeautifulSoup(requests.get(url).text, "html.parser")
		forms = parser.findAll("form")
		form_list = []
		for f in forms:
			form_list.append(HtmlForm(url, f))
		
		return form_list

