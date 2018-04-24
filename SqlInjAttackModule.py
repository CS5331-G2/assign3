from AttackModule import AttackModule
from Helpers import Helper
from AttackReport import AttackReport

class SqlInjAttackModule(AttackModule):

	def __init__(self):
		AttackModule.__init__(self, "SQL Injection", "SQL Injection")

	def attack(self, endpoint):
		print "    Beginning attack -> SqlInj"
		if endpoint.is_form() is not True:
			print "    Target: {0}\n    Is not a form. Skipping!".format(endpoint.url)
			return

		self.attack_succeeded = False
		self.attack_report = None

		print "    Inputs in form are:"
		for index, key in enumerate(endpoint.htmlForm.get_form_data_dict()):
			print "    [{0}] name:{1} value:{2}".format(index, key, endpoint.htmlForm.get_form_data_dict()[key])
		print "    Beginning attack (SQL Injection) -> SQL\n    Target: {0}".format(endpoint.url)

		f = open('SqlInjPayload.txt', 'r')
		for params, attackPattern in enumerate(f.readlines()):
			payload = {}
			for index, key in enumerate(endpoint.htmlForm.get_form_data_dict()):
				key_string = list(endpoint.htmlForm.get_form_data_dict().keys())[index]
				payload[key_string] = attackPattern.strip()

			result = self.launch_attack(endpoint, payload, attackPattern.strip())
			if result:
				self.attack_succeeded = True
				print "    [ SqlInjAttack: {0} params in table ] ->".format(params)
				print "    [ SqlInjAttack: {0} ] ->".format(payload)
				break

		if self.attack_succeeded:
			print "    Finished attack -> VULNERABLE!\n"
		else:
			print "    Finished attack -> Nothing found!\n"

	def launch_attack(self, endpoint, payload, attackPattern):
		headers = {}
		res = None
		if endpoint.method.upper() == "GET":
			res = Helper.do_get_request(endpoint, headers, payload)
		elif endpoint.method.upper() == "POST":
			res = Helper.do_post_request(endpoint, headers, payload)

		if res is not None and self.is_attack_successful(res, attackPattern):
			report = AttackReport(self.attackClass, endpoint, headers, payload, "")
			AttackReport.add_attack_report(report)
			return True

		return False

	def is_attack_successful(self, res, attackPattern):
		if res.ok:
			if res.status_code == 200:
				if "q1w2e3r4t5y6u7i8o9" in res.content and attackPattern not in res.content:
					return True
			else:
				print "WARNING: SqlInjAttackModule, " + \
					"is_attack_successful, unrecognized status code: {0} for {1}".format(
						res.status_code, res.request.url)
		return False
