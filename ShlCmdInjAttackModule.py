from AttackModule import AttackModule

class ShlCmdInjAttackModule(AttackModule):
	
	def __init__(self):
		AttackModule.__init__(self, "Shell Command Injection", "Command Injection")
