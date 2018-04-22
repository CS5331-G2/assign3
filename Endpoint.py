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
		self.isForm = False

	def mark_as_form(self):
		self.isForm = True

	def is_form(self):
		return self.isForm

	def get_url_till_path(self):
		return self.scheme + "://" + self.host + self.path

	def has_query_string(self):
		try:
			self.path.index("?") >= 0
			return True
		except:
			return False

	def get_query_string(self):
		if self.has_query_string():
			return self.path[self.path.index("?") + 1:]
		else:
			return "";

	def __str__(self):
		return "Endpoint {{\nURL: {0}\n{1} {2}\nHOST: {3}\nFORM: {4}\n}}" \
				.format(self.url, self.method, self.path, self.host, self.isForm)

