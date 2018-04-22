from AttackModule import AttackModule

class LfiAttackModule(AttackModule):
	
	def __init__(self):
		AttackModule.__init__(self, "Local File Inclusion", "Server Side Code Injection")

	def attack():
		f=open('LfiPayload.txt','r')
		for i in f.readlines():

			ur = requests.get(url+'{}'.format(i))
			if "root" in ur.content:
				print 'Detected LFT'
				time.sleep(2)

