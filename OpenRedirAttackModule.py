from AttackModule import AttackModule
from Helpers import Helper
from AttackReport import AttackReport

class OpenRedirAttackModule(AttackModule):
	
	def __init__(self):
		AttackModule.__init__(self, "Open Redirect", "Open Redirect")

	def attack(self, endpoint):
		self.attack_succeeded = False
		self.attack_report = None

		payload = "https://status.github.com/messages"
		result = self.launch_attack(endpoint, payload)

		if result:
			self.attack_succeeded = True
			print "    [Open Redirect: {0}] -> {1}".format(payload, result)

		if self.attack_succeeded:
			print "    Finished attack --> VULNERABLE\n"
		else:
			print "    Finished attack --> Nothing found!\n"

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
				report = AttackReport(self.attackClass, endpoint, headers, formData, "")
				AttackReport.add_attack_report(report)
				return True

		return False

	def is_attack_successful(self, res):
		if res.ok:
			if res.status_code == 200:
				if "GitHub System Status" in res.text:
					return True
			else:
				return False
		return False