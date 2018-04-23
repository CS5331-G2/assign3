import requests
from AttackModule import AttackModule

class CsrfAttackModule(AttackModule):

	def __init__(self):
		AttackModule.__init__(self, "CSRF", "CSRF")

	def attack(self, endpoint):
		if endpoint.is_form() is not True:
			print "Target: {0}\nIs not a form. Skipping!".format(endpoint.url)
			return

		if "csrftoken" in endpoint.htmlForm.get_form_data_dict():
			print
			print "Beginning attack (CSRF Token in Form) -> CSRF\nTarget: {0}".format(endpoint.url)
			print "Inputs in form are:"

			for index, formData in enumerate(endpoint.htmlForm.get_form_data_dict()):
				print "[{0}] name:{1} value:{2}".format(index, formData, endpoint.htmlForm.get_form_data_dict()[formData])

		client = requests.session()
		client.get(endpoint.url)
		if 'csrftoken' in client.cookies:
			csrftoken = client.cookies['csrftoken']
			print
			print "Beginning attack (CSRF Token in Cookie) -> CSRF\nTarget: {0}".format(endpoint.url)

			payload = {
				'csrftoken': csrftoken,
				'tag': '69'
			}

			r = client.post(endpoint.url, data=payload)
