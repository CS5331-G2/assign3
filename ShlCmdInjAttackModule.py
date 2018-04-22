from AttackModule import AttackModule

class ShlCmdInjAttackModule(LfiAttackModule):
	
	def __init__(self):
		AttackModule.__init__(self, "Shell Command Injection")
