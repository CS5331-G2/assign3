from bs4 import BeautifulSoup
import requests


url = 'https://indianvisaonline.gov.in/evisa/Registration'

page = requests.get(url).text
soup = BeautifulSoup(page, "html.parser")

forms = soup.findAll("form")
#form1 = forms[0]
#print(form1)
#print (form1.input['id'])

for currForm in forms:
    formAction = currForm['action']
    formMethod = currForm['method']
    #formId = currForm['id']
    print("--------------------------")
    print("FORM")
    print("--------------------------")
    print("Action: " + formAction)
    print("Method: " + formMethod)
    print("--------------------------")
    print("INPUTS")
    print("-------------------------")

    #print("Form ID: " + formId)

    inputs = currForm.findAll("input")

    for currInput in inputs:
        inputType = currInput['type']
        inputId = currInput['id']
        inputName = currInput['name']

        print ("Type: " + inputType)
        print ("ID: " + inputId)
        print ("Name: " + inputName)
        print("\n")
