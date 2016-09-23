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
	identifier=open(directory+'.clonedir','w')
	server.send(b'#hd#')
	hashdata=str.encode(utils.calcdirhash(directory))
	if(recvserverreply()):
		server.send(str.encode(str(len(hashdata))))
	if(recvserverreply()):
		server.send(hashdata)
	if(recvserverreply()):
		print('Sent file details to engine. Waiting for reply...')
	server.send(b'#id#')
	identity=server.recv(256).decode("utf-8")
	server.send(b'#sc#')
	numfiles=int(server.recv(256).decode("utf-8"))
	identifier.write(identity)  #After database has been affected we can write the .clonedir file 
	identifier.close() 
	print(str(numfiles)+' files to be uploaded.')
	server.send(b'#sc#')
	for i in range(0,numfiles):
		a=2 #Send each file one by one
	server.close()

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



	

