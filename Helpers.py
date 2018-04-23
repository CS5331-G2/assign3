
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
	def href_scraper(url):
		import requests
		from urlparse import urljoin
		from bs4 import BeautifulSoup

		soup = BeautifulSoup(requests.get(url, verify=False).text, "html.parser")

		url_list = []
		for a in soup.findAll('a', href=True):
			url_list.append(urljoin(url, a['href']))
		return url_list


	@staticmethod
	def do_post_request(endpoint, dictHeaders, dictFormData):
		import requests
		return requests.post(endpoint.url, headers=dictHeaders, data=dictFormData)
		

	@staticmethod
	def do_get_request(endpoint, dictHeaders, dictFormData):
		import requests
		return requests.get(endpoint.url, headers=dictHeaders, params=dictFormData)

	@staticmethod
	def generate_attack_report():
		import json
		from AttackReport import AttackReport
		attackClasses = [
			"SQL Injection",
			"Server Side Code Injection",
			"Directory Traversal",
			"Open Redirect",
			"CSRF",
			"Command Injection",
		]
		report = []
		
		for attackClass in attackClasses:
			attackResults = AttackReport.get_attack_report_by_class(attackClass)
			hosts = []
			results = {}
			for attackResult in attackResults:
				if attackResult.get_host() not in hosts:
					hosts.append(attackResult.get_host())
					results[attackResult.get_host()] = []
				results[attackResult.get_host()].append(attackResult)
			
			classReport = {}
			classReport['class'] = attackClass
			classReport['results'] = results
			report.append(classReport)

		return report

	@staticmethod
	def generate_attack_scripts():
		import json
		import os
		import shutil
		import urllib
		from AttackReport import AttackReport

		if os.path.isdir("generated_exploits"):
			shutil.rmtree("generated_exploits")

		os.makedirs("generated_exploits");

		attackClasses = [
			"Command Injection",
			"SQL Injection",
			"Server Side Code Injection",
			"Directory Traversal",
			"Open Redirect",
			"CSRF",
		]

		for attackClass in attackClasses:
			attackResults = AttackReport.get_attack_report_by_class(attackClass)
			for attackResult in attackResults:
				fileContent = [
					"# Host: {0}".format(attackResult.endpoint.get_scheme_and_host_url()),
					"# Endpoint: {0}".format(attackResult.endpoint.get_path_and_query_string()),
					"# Params: {0}".format(json.dumps(attackResult.formData)),
					"# Method: {0}".format(json.dumps(attackResult.endpoint.method)),
					"import requests",
					"dictHeaders={0}".format(json.dumps(attackResult.headers)),
					"dictFormData={0}".format(json.dumps(attackResult.formData)),
				]
				if attackResult.endpoint.method.upper() == "GET":
					if len(attackResult.formData) > 0:
						fileContent.append("url=\"{0}?{1}\"".format(
							attackResult.endpoint.get_url_till_path(),
							urllib.urlencode(attackResult.formData)))
					else:
						fileContent.append("url=\"{0}\"".format(attackResult.endpoint.get_url_till_path()))
						
					fileContent.append("r = requests.get(url, headers=dictHeaders, data=dictFormData)")
				elif attackResult.endpoint.method.upper() == "POST":
					fileContent.append("url=\"{0}\"".format(attackResult.endpoint.url))
					fileContent.append("r = requests.post(url, headers=dictHeaders, data=dictFormData)")
				fileContent.append("print r.text")

				directory = attackClass.lower().replace(" ", "-")
				path = "generated_exploits/{0}.py".format(str(attackResult.id))
				print "Generated: {0}".format(path)
				with open(path, "w") as outputFile:
					for line in fileContent:
						outputFile.write(line + "\n")
					outputFile.close()













