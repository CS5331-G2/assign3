import json

class AttackReport(object):
	attacks = []

	def add_attack_report(attackReport):
		AttackReport.attacks.append(attackReport)

	def __init__(self, attackClass, endpoint, headers, formData):
		self.attackClass = attackClass
		self.endpoint = endpoint
		self.headers = headers
		self.formData = formData

	def get_attack_class(self):
		return self.attackClass
	
	def get_host(self):
		return self.endpoint.get_scheme_and_host_url()

	def get_json_dict(self):
		s = {}
		if self.attackClass == "Command Injection":
			s['endpoint'] = self.endpoint.get_path()
			s['params'] = self.formData
			s['method'] = self.endpoint.method
		return s

	def __str__(self):
		s = {}
		s['class'] = self.attackClass
		s['endpoint'] = self.endpoint.url
		s['method'] = self.endpoint.method
		s['params'] = self.formData
		if self.attackClass == "Command Injection":
			s['endpoint'] = self.endpoint.get_path()
		return json.dumps(s, indent=2)
