
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

	def script_location_scrapper(url):
		import requests
		import re
		from bs4 import BeautifulSoup
		url = "http://ec2-54-251-169-51.ap-southeast-1.compute.amazonaws.com:8080/random.php"
		parser = BeautifulSoup(requests.get(url, verify=False).text, "html.parser")
		scripts = parser.findAll("script")
		index = 0
		possible_urls = []
		possible_url_sigs = [
		]
		for script in scripts:
			matches = re.findall('document\.location = document\.location\.href \+ "(.*?)";', str(script))
			for match in matches:
				possible_urls.append(match)

		result = []
		for possible_url in possible_urls:
			result.append(url + possible_url)

		return result

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
		# WARNING: SSL Verification has been intentionally disabled!
		return requests.post(endpoint.url, verify=False, headers=dictHeaders, data=dictFormData)
		

	@staticmethod
	def do_get_request(endpoint, dictHeaders, dictFormData):
		import requests
		# WARNING: SSL Verification has been intentionally disabled!
		return requests.get(endpoint.get_url_till_path(), verify=False, headers=dictHeaders, params=dictFormData)

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
					"# Headers: {0}".format(json.dumps(attackResult.headers)),
					"# Params: {0}".format(json.dumps(attackResult.formData)),
					"# Method: {0}".format(json.dumps(attackResult.endpoint.method)),
					"import requests",
					"dictHeaders={0}".format(json.dumps(attackResult.headers)),
					"dictFormData={0}".format(json.dumps(attackResult.formData)),
					"",
					"# WARNING: SSL Verification has been intentionally disabled!"
				]
				if attackResult.endpoint.method.upper() == "GET":
					fileContent.append("url=\"{0}\"".format(attackResult.endpoint.get_url_till_path()))
					fileContent.append("r = requests.get(url, verify=False, headers=dictHeaders, params=dictFormData)")
				elif attackResult.endpoint.method.upper() == "POST":
					fileContent.append("url=\"{0}\"".format(attackResult.endpoint.url))
					fileContent.append("r = requests.post(url, verify=False, headers=dictHeaders, data=dictFormData)")
				fileContent.append("print r.text")

				directory = attackClass.lower().replace(" ", "-")
				path = "generated_exploits/{0}.py".format(str(attackResult.id))
				print "Generated: {0}".format(path)
				with open(path, "w") as outputFile:
					for line in fileContent:
						outputFile.write(line + "\n")
					outputFile.close()













