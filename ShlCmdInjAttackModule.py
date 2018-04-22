from AttackModule import AttackModule

# Dangerous inputs for PHP based web servers
# https://www.kevinlondon.com/2015/07/26/dangerous-python-functions.html
# https://github.com/PortSwigger/command-injection-attacker
#

class ShlCmdInjAttackModule(AttackModule):
	
	def __init__(self):
		AttackModule.__init__(self, "Shell Command Injection", "Command Injection")
