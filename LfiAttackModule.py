from AttackModule import AttackModule

class LfiAttackModule(AttackModule):
	
	def __init__(self):
		AttackModule.__init__(self, "Local File Inclusion")
