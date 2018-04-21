from urlparse import urlparse


# This class is used to identify all the URLs with their METHODS
# 

class Endpoint(object):
	
	def __init__(self, url, method):
		parser = urlparse(url)
		self.url = url
		self.scheme = parser.scheme
		self.host = parser.hostname
		if parser.port is not None:
			self.host = self.host + ":" + str(parser.port)
		self.path = parser.path if parser.path.__len__() > 0 else "/"
		if parser.query.__len__() > 0 :
			self.path = parser.path + "?" + parser.query
		self.method = method

	def get_url_till_path(self):
		return self.scheme + "://" + self.host + self.path

	def __str__(self):
		return "Endpoint {{\nURL: {0}\n{1} {2}\nHOST: {3}\n}}".format(self.url, self.method, self.path, self.host)

