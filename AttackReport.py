import json

class AttackReport(object):
	attacks = []

	@staticmethod
	def add_attack_report(attackReport):
		AttackReport.attacks.append(attackReport)

	@staticmethod
	def get_attack_report_by_class(attackClass):
		results = []
		for attack in AttackReport.attacks:
			print attack.attackClass
			if attack.attackClass == attackClass:
				results.append(attack)
		return results

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

	def serialize(obj):
		s = {}
		s['class'] = obj.attackClass
		s['endpoint'] = obj.endpoint.url
		s['method'] = obj.endpoint.method
		s['params'] = obj.formData
		if obj.attackClass == "Command Injection":
			s['endpoint'] = obj.endpoint.get_path()
		return s

	def __str__(self):
		return json.dumps(self.serialize(), indent=2)
