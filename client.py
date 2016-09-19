import socket
import utils
import os
import socket
import sys

server=None


def connecttoengine():
	global server
	server=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
	try:
		server.connect('/tmp/clonedir')
	except:
		print('Error occurred when connecting to CloneDir Engine... Check if Daemon is running.')
	print('Connected to Engine')

def recvserverreply():
	if(server.recv(5)==b'#sc#'):    #Wait for reply from server
		return True		
	else:
		print('Error Communicating with server')
		exit()
def addnewdirectory(directory):
	hashdata=str.encode(utils.calcdirhash(directory))
	server.send(b'#hd#')
	if(recvserverreply()):
		server.send(str.encode(str(len(hashdata))))
	if(recvserverreply()):
		server.send(hashdata)
	if(recvserverreply()):
		print('Successfully sent data')
	while True:
		print(server.recv(10))

def syncdirectory(directory):
	print('Syncing Directory')

if __name__ == '__main__':
	args=sys.argv
	if(len(args)<=1):                        #First argument is filename when running from Python
		print('CloneDir Client utility\n\nBasic commands - \n\t1. -add <Directory name> Add a directory')
		exit()
	else:
		global globalargs
		connecttoengine()
		directory=args[1]
		if(os.path.exists(directory)):
			print('Proper directory')
		else:
			print('Invalid directory.')
			exit()
		for i in range(2,len(args)):
				if(args[i]=='-add'):
					addnewdirectory(directory)
				elif(args[i]=='-sync'):
					syncdirectory(directory)



	

