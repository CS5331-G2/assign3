from AttackModule import AttackModule

class CsrfAttackModule(AttackModule):

	def __init__(self):
		AttackModule.__init__(self, "CSRF", "CSRF")

	def attack(self, endpoint):
		if endpoint.is_form() is not True:
			print "Target: {0}\nIs not a form. Skipping!".format(endpoint.url)
			return

		if "csrftoken" in endpoint.htmlForm.get_form_data_dict():
			print "Beginning attack -> CSRF\nTarget: {0}".format(endpoint.url)
			print "Inputs in form are:"

			for formData in endpoint.htmlForm.get_form_data_dict():
				print "name:{0} value:{1}".format(formData, endpoint.htmlForm.get_form_data_dict()[formData])
