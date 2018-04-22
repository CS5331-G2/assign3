
class AttackModule(object):
	
	def __init__(self, moduleName, attackClass):
		self.moduleName = moduleName
		self.attackClass = attackClass

	def __str__(self):
		return "{0} Attack Module, Class: {1}".format(self.moduleName, self.attackClass)

	def attack(self, endpoint):
		print "Not implemented! " + self.__str__()
