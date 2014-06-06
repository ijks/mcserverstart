import socket
import configparser
import sys
from time import sleep

# load from config
config = configparser.ConfigParser()
config.read('client.ini')
HOST = config['main']['host']
PORT = int(config['main']['port']) # int() is needed because all config values are str by default

# defines the 'protocol' used for i/o
protocol = {
	'empty':'MCSERV_00',
	'req_on':'MCSERV_ON',
	'req_restart':'MCSERV_RS',
	'start_success':'MCSERV_OK',
	'start_already_running':'MCSERV_AR',
	'generic_error':'MCSERV_??',
	'server_error':'MCSERV_ER',
} 

def sendMsg(msg):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		sock.sendall(bytes(msg, 'utf-8'))
		return sock.recv(9)
	finally:
		sock.close()

if __name__ == '__main__':
	try:
		while True:
			start = input("Do you want to send a start request to this server? ip: {}:{}\ny/n: ".format(HOST, PORT))
			if start.lower() == 'y':
				response = str(sendMsg(protocol['req_on']), encoding='utf-8')
				break
			elif start.lower() == 'n':
				print("No? Then why did you even start me up... ;(")
				input("Press enter to exit.")
				sys.exit()
			else:
				print("Wha? I didn't get that. Repeat pls?")

		if response == protocol['start_success']:
			print("Success! The server should be running now.")
			input("Press enter to exit.")
			sys.exit()

		if response == protocol['start_already_running']:
			while True:
				restart = input("The server is already running. Do you want to restart it?\ny/n: ")
				if restart.lower() == 'y':
					response = str(sendMsg(protocol['req_restart']), encoding='utf-8')
					break
				elif restart.lower() == 'n':
					print("Alrighty then.")
					input("Press enter to exit.")
					sys.exit()
				else:
					print("Wha? I didn't get that. Repeat pls?")

		if response == protocol['empty'] or response == protocol['generic_error'] or response == protocol['server_error']:
			print("Something went wrong! I'm sorry... :/")
			input("Press enter to exit.")
			sys.exit()
	except Exception as e:
		print("There was an error... ;(\nThis is what it says:\n", e)
		input("Press enter to exit")