from AttackModule import AttackModule

class RfiAttackModule(AttackModule):
	
	def __init__(self):
		AttackModule.__init__(self, "Remote File Inclusion", "Server Side Code Injection")
