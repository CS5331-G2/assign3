from HtmlElement import HtmlElement

class HtmlInput(HtmlElement):
	
	def __init__(self, htmlInput):
		HtmlElement.__init__(self, htmlInput)
		from bs4 import BeautifulSoup
		parser = BeautifulSoup(str(htmlInput), "html.parser")
		
		input_ = parser.find("input")
		if input_ is not None:
			self.name = input_['name'] if 'name' in input_.attrs.keys() else ""
			self.type = input_['type'] if 'type' in input_.attrs.keys() else "text"
			self.value = input_['value'] if 'value' in input_.attrs.keys() else ""
		else:
			"!!! Bad input tag\n{0}".format(htmlInput)

	def __str__(self):
		return "HTML Input {{ Name: '{0}', Type: '{1}', Value: '{2}' }}".format(self.name, self.type, self.value)
