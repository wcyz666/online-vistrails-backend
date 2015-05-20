import web
import subprocess

urls = (
	'/vistrails', 'vistrails'
)

class vistrails:

	def POST(self):
		i = web.data()
		print i
		subprocess.call(['rm','-f','nodes.json'])
		subprocess.call(['rm','-f','/media/sdb/falcone/nodes-to-vt/result.txt'])

		with open('nodes.json', 'w') as f:
			f.write(i)

		subprocess.call(['python','translate.py'])
		subprocess.call(['python','/media/sdb/falcone/vistrails/vistrails/run.py','-b','/media/sdb/falcone/nodes-to-vt/output.xml'])
		

		with open('/media/sdb/falcone/nodes-to-vt/result.txt', 'r') as f:
			s = f.read()
			f.close()
		
		web.header('Access-Control-Allow-Origin', '*')
		print s
		return sw

if __name__ == '__main__':
	app = web.application(urls, globals())
	app.run()
