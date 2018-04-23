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
		self.path = parser.path if len(parser.path) > 0 else "/"
		if len(parser.query) > 0 :
			self.path = parser.path + "?" + parser.query
		self.method = method
		self.isForm = False

	def mark_as_form(self, htmlForm):
		self.isForm = True
		self.htmlForm = htmlForm

	def is_form(self):
		return self.isForm

	def get_form(self):
		return self.htmlForm

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

	def get_path(self):
		if self.has_query_string():
			return self.path[:self.path.index("?")]
		else:
			return self.path;

	def get_query_string_dict(self):
		query_string_dict = {}		
		qs = self.get_query_string()
		if len(qs) > 0:
			keyValues = qs.split("&")
			for keyValue in keyValues:
				data = keyValue.split("=")
				if len(data) == 2:
					query_string_dict[data[0]] = data[1]
		return query_string_dict

	def get_scheme_and_host_url(self):
		return "{0}://{1}".format(self.scheme, self.host)

	def get_path_and_query_string(self):
		return self.path

	def __str__(self):
		return "Endpoint {{\nURL: {0}\n{1} {2}\nHOST: {3}\nFORM: {4}\n}}" \
				.format(self.url, self.method, self.path, self.host, self.isForm)

