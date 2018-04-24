from AttackModule import AttackModule
from Helpers import Helper
from AttackReport import AttackReport

class OpenRedirAttackModule(AttackModule):
	
	def __init__(self):
		AttackModule.__init__(self, "Open Redirect", "Open Redirect")

	def attack(self, endpoint):
		print "    Beginning attack -> Open Redirection"
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
		from bs4 import BeautifulSoup
		if res.ok:
			# HTTP 200
			if res.status_code == 200:
				# See if the page itself is the GitHub System Status page
				if "GitHub System Status" in res.text:
					return True

				# Otherwise look for meta tags dealing with HTML redirect
				bs = BeautifulSoup(res.text, "html.parser")
				metaTags = bs.findAll("meta")
				for meta in metaTags:
					httpEquiv = meta['http-equiv'] if 'http-equiv' in meta.attrs.keys() else ""
					content = meta['content'] if 'content' in meta.attrs.keys() else ""
					if httpEquiv.lower() == "refresh" and len(content.split(";")) == 2:
						if len(content.split(";")[1].split("=")) == 2:
							if content.split(";")[1].split("=")[1] == "https://status.github.com/messages":
								return True

				# Otherwise look for <script>
				scriptTags = bs.findAll("script")
				for script in scriptTags:
					if len(re.findall('document\.location = "(.*?)";', str(script))) > 0:
						matches = re.findall('document\.location = "(.*?)";', str(script))
						for match in matches:
							if match == "https://status.github.com/messages":
								return True
							
			# Probably one of the HTTP Redirect Status codes
			# Check for the 'Location' header
			elif "Location" in res.headers.keys() and res.headers['Location'] == "https://status.github.com/messages":
				return True

		return False
