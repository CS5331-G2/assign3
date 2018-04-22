from AttackModule import AttackModule

class PhpCodeInjAttackModule(AttackModule):
	
	def __init__(self):
		AttackModule.__init__(self, "PHP Code Injection", "Server Side Code Injection")
