import socketserver
import configparser
import subprocess

serverProcess = None # yeah... i don't know another way to keep track of the server process outside of the request handler. maybe something with a separate server class, but meh

# config setup
config = configparser.ConfigParser()
config.read('server.ini')
DIR = str(config['main']['dir'])
SCRIPT = str(config['main']['script'])
PATH = DIR+SCRIPT

# defines the mini-protocol used for i/o
protocol = {
	'empty':'MCSERV_00',
	'req_on':'MCSERV_ON',
	'req_restart':'MCSERV_RS',
	'start_success':'MCSERV_OK',
	'start_already_running':'MCSERV_AR',
	'generic_error':'MCSERV_??',
	'server_error':'MCSERV_ER',
} 

def serverStart():
	global serverProcess

	serverProcess = subprocess.Popen(PATH, creationflags=subprocess.CREATE_NEW_CONSOLE)

def serverRestart():
	global serverProcess

	serverProcess.terminate()
	serverStart()


def serverRunning():
	global serverProcess

	if serverProcess == None or serverProcess.poll(): # if the server hasn't started yet, serverProcess is None, so we have to check for that too
		return False
	elif serverProcess.poll() == None: # poll() is None when the process is running
		return True
		

# server definition
class Handler(socketserver.BaseRequestHandler):
	def handle(self):
		self.data = str(self.request.recv(9), encoding='utf-8') # recieve a message and decode it into unicode
		self.response = protocol['empty']
		try:
			if self.data == protocol['req_on']:
				print("Server start request recieved. Source: {}".format(self.client_address))

				if serverRunning() == False:
					serverStart()
					print("Server started successfully!")
					self.response = protocol['start_success']
				elif serverRunning() == True:
					print("Server already on. Client might request a restart.")
					self.response = protocol['start_already_running']
			elif self.data == protocol['req_restart']:
				serverRestart()
				print("Client requested restart. Restart successful!")
				self.response = protocol['start_success']
			else:
				print("Unknown command recieved: \"{0}\" Source: {1}".format(self.data, self.client_address))
				self.response = protocol['generic_error']
		except Exception as e:
			self.response = protocol['server_error']
			raise
		finally:
			self.response = bytes(self.response, 'utf-8') # encode the message back into bytes for transfer
			self.request.sendall(self.response)

if __name__ == "__main__":
	HOST, PORT = "0.0.0.0", 25566
	
	server = socketserver.TCPServer((HOST, PORT), Handler)
	print("Listening on {}:{}".format(HOST, PORT))
	server.serve_forever()