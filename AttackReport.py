import json

class AttackReport(object):
	attackReportId = 1
	attacks = []

	@staticmethod
	def add_attack_report(attackReport):
		attackReport.id = AttackReport.attackReportId;
		AttackReport.attackReportId += 1
		AttackReport.attacks.append(attackReport)

	@staticmethod
	def get_attack_report_by_class(attackClass):
		results = []
		for attack in AttackReport.attacks:
			if attack.attackClass == attackClass:
				results.append(attack)
		return results

	def __init__(self, attackClass, endpoint, headers, formData, formId):
		self.id = -1
		self.attackClass = attackClass
		self.endpoint = endpoint
		self.headers = headers
		self.formData = formData
		self.formId = formId

	def get_attack_class(self):
		return self.attackClass
	
	def get_host(self):
		return self.endpoint.get_scheme_and_host_url()

	def serialize(obj):
		s = {}
		s['class'] = obj.attackClass
		s['id'] = obj.id
		s['endpoint'] = obj.endpoint.url
		s['method'] = obj.endpoint.method
		s['params'] = obj.formData
		s['headers'] = obj.headers
		if obj.attackClass == "CSRF":
			#some other form of parsing needed?
			s['form_id'] = obj.formId
		else:
			s['endpoint'] = obj.endpoint.get_path()
		return s

	def __str__(self):
		return json.dumps(self.serialize(), indent=2)
