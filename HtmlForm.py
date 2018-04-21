from HtmlElement import HtmlElement
from HtmlInput import HtmlInput
from bs4 import BeautifulSoup
from urlparse import urlparse
import urlparse
from Endpoint import Endpoint

class HtmlForm(HtmlElement):
	
	def __init__(self, url, htmlForm):
		HtmlElement.__init__(self, htmlForm)
		parser = BeautifulSoup(str(htmlForm), "html.parser")
		
		form = parser.find("form")
		if form is not None:
			self.url = url
			self.action = form['action'] if 'action' in form.attrs.keys() else "/"
			self.method = form['method'] if 'method' in form.attrs.keys() else "GET"
			self.method = self.method.upper()
			self.inputs = []
			inputs = form.findAll("input")
			for input_ in inputs:
				self.inputs.append(HtmlInput(input_))
		else:
			"!!! Bad form tag\n{0}".format(htmlForm)

	def get_endpoint(self):
		e = Endpoint(self.url, self.method)
		targetUrl = urlparse.urljoin(e.get_url_till_path(), self.action)
		return Endpoint(targetUrl, self.method)

	def __str__(self):
		return "HTML Form {{\nPage: {0}\nMethod: {1} Action: {2}\n".format(self.url, self.method, self.action) + "\n" + \
				"\n".join([`str(input_)` for input_ in self.inputs]) + "\n}\n"
