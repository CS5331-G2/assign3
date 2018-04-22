from AttackModule import AttackModule

class CsrfAttackModule(AttackModule):
	
	def __init__(self, htmlInput):
		AttackModule.__init__(self, "CSRF")
