
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





















