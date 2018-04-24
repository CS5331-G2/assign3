import requests
from AttackModule import AttackModule
from Helpers import Helper
from AttackReport import AttackReport

class CsrfAttackModule(AttackModule):

	def __init__(self):
		AttackModule.__init__(self, "CSRF", "CSRF")

	def attack(self, endpoint):
		print "    Beginning attack -> CSRF"
		if endpoint.is_form() is not True:
			print "    Target: {0}\n    Is not a form. Skipping!".format(endpoint.url)
			print "    Finished attack -> Nothing found!\n"
			return

		self.csrf_found = False
		self.attack_succeeded = False
		self.attack_report = None

		if "csrftoken" in endpoint.htmlForm.get_form_data_dict():
			self.csrf_found = True
			print "    Inputs in form are:"
			for index, key in enumerate(endpoint.htmlForm.get_form_data_dict()):
				print "      [{0}] name:{1} value:{2}".format(index, key, endpoint.htmlForm.get_form_data_dict()[key])
			print "    Beginning attack (CSRF Token in Form) -> CSRF\n    Target: {0}".format(endpoint.url)

			payload = {}

			for index, key in enumerate(endpoint.htmlForm.get_form_data_dict()):
				key_string = list(endpoint.htmlForm.get_form_data_dict().keys())[index]
				if key_string == "csrftoken":
					payload[key_string] = endpoint.htmlForm.get_form_data_dict()[key_string]
				else:
					payload[key_string] = endpoint.htmlForm.get_form_data_dict()[key_string] + "_changed"

			self.attack_operation(endpoint, payload)

		else:
			client = requests.session()
			client.get(endpoint.url)
			if 'csrftoken' in client.cookies:
				self.csrf_found = True
				csrftoken = client.cookies['csrftoken']
				print "      name:csrftoken value:(0)".format(csrftoken)
				print
				print "    Beginning attack (CSRF Token in Cookie) -> CSRF\n    Target: {0}".format(endpoint.url)

				payload = {}

				for index, key in enumerate(endpoint.htmlForm.get_form_data_dict()):
					key_string = list(endpoint.htmlForm.get_form_data_dict().keys())[index]
					if key_string == "csrftoken":
						payload[key_string] = endpoint.htmlForm.get_form_data_dict()[key_string]
					else:
						payload[key_string] = endpoint.htmlForm.get_form_data_dict()[key_string] + "_changed"

				self.attack_operation(endpoint, payload)

		if self.csrf_found is not True:
			print "    no CSRF Token found. Skipping!".format(endpoint.url)
			return
		print "    Finished attack -> CSRF"

	def attack_operation(self, endpoint, payload):
		result = self.launch_attack(endpoint, payload)
		if result:
			self.attack_succeeded = True
			print "    [ CsrfAttack: {0} ] ->".format(payload),
			print result

		if self.attack_succeeded:
			print "    Finished attack -> VULNERABLE!\n"
		else:
			print "    Finished attack -> Nothing found!\n"

	def launch_attack(self, endpoint, payload):
		headers = {}
		res = None
		if endpoint.method.upper() == "GET":
			res = Helper.do_get_request(endpoint, headers, payload)
		elif endpoint.method.upper() == "POST":
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
				if "_changed" in req.text:
					return True
			else:
				print "WARNING: CsrfAttackModule, " + \
					"is_attack_successful, unrecognized status code: {0} for {1}".format(
						res.status_code, res.request.url)
		return False
