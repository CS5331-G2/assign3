from AttackModule import AttackModule

class SqlInjAttackModule(LfiAttackModule):
	
	def __init__(self):
		AttackModule.__init__(self, "SQL Injection")
