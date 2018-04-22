from AttackModule import AttackModule
from LfiAttackModule import LfiAttackModule

class RfiAttackModule(LfiAttackModule):
	
	def __init__(self):
		AttackModule.__init__(self, "Remote File Inclusion")
