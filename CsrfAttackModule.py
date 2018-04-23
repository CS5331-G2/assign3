import requests
from AttackModule import AttackModule
from Helpers import Helper
from AttackReport import AttackReport

class CsrfAttackModule(AttackModule):

	def __init__(self):
		AttackModule.__init__(self, "CSRF", "CSRF")

	def attack(self, endpoint):
		if endpoint.is_form() is not True:
			print "Target: {0}\n is not a form. Skipping!".format(endpoint.url)
			return

		self.csrf_found = False
		self.attack_succeeded = False
		self.attack_report = None

		if "csrftoken" in endpoint.htmlForm.get_form_data_dict():
			self, csrf_found = True
			print
			print "Inputs in form are:"
			for index, formData in enumerate(endpoint.htmlForm.get_form_data_dict()):
				print "[{0}] name:{1} value:{2}".format(index, formData, endpoint.htmlForm.get_form_data_dict()[formData])
			print
			print "Beginning attack (CSRF Token in Form) -> CSRF\nTarget: {0}".format(endpoint.url)

		else:
			client = requests.session()
			client.get(endpoint.url)
			if 'csrftoken' in client.cookies:
				self.csrf_found = True
				csrftoken = client.cookies['csrftoken']
				print "name:csrftoken value:(0)".format(csrftoken)
				print
				print "Beginning attack (CSRF Token in Cookie) -> CSRF\nTarget: {0}".format(endpoint.url)

				payload = {
					'csrftoken': csrftoken,
					'secret': '69'
				}

				r = client.post(endpoint.url, data=payload)

		if self.csrf_found is not True:
			print "Target: {0}\n no CSRF Token found. Skipping!".format(endpoint.url)
			return

		if self.attack_succeeded:
			print "    Finished attack -> VULNERABLE!\n"
		else:
			print "    Finished attack -> Nothing found!\n"

	def launch_attack(self, endpoint, payload):
		headers = {}
		endpoint.method.upper() == "POST"
		res = Helper.do_post_request(endpoint, headers, payload)

		if self.is_attack_successful(res):
			report = AttackReport(self.attackClass, endpoint, headers, payload, "")
			AttackReport.add_attack_report(report)
			return True

		return False

	def is_attack_successful(self, res):
		if res.ok:
			if res.status_code == 200:
				if any(match in res.text for match in CsrfAttackModule.unameStrings):
					return True
			else:
				print "WARNING: CsrfAttackModule, " + \
					"is_attack_successful, unrecognized status code: {0} for {1}".format(
						res.status_code, res.request.url)
		return False
