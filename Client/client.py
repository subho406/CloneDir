import socket
import utils
import os
import sys
import time
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
server=None


def connecttoengine():
	global server
	server=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
	try:
		server.connect('/tmp/clonedir')
		return 1
	except:
		print('Error occurred when connecting to CloneDir Engine... Check if Daemon is running.')
		return
	print('Connected to Engine')


def recvserverreply():
	if(server.recv(4)==b'#sc#'):    #Wait for reply from server
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
			print('\nSent file details to engine. Waiting for reply...')
		server.send(b'#id#')
		identity=server.recv(256).decode("utf-8")
		server.send(b'#sc#')
		numfiles=int(server.recv(256).decode("utf-8"))
		identifier.write(identity)  #After database has been affected we can write the .clonedir file 
		identifier.close() 
		print(str(numfiles)+' files to be uploaded.')
		for i in range(0,numfiles):
			server.send(b'#sc#')
			filetobesent=server.recv(1024).decode("utf-8")
			server.send(b'#sc#')
			data=filetobesent.split('\t')
			filename=data[0]
			hashvalue=data[1]
			location=data[2]
			size=int(data[3])
			sentsize=0
			filetosend=open(location,'rb')
			recvserverreply()
			#print('Sending file '+filename)
			nextdisplay=0
			while sentsize<size:
				buff=filetosend.read(1024)
				server.send(buff)
				sentsize=sentsize+len(buff)
				display=int((sentsize/size)*100)
				if display>=nextdisplay:
					#print('\r '+str(display)+'%',end='')
					nextdisplay=nextdisplay+1
			#print('\n')
			filetosend.close()
			recvserverreply()		
		server.close()

def recvfile(f):
	data=f.split('\t')
	filename=data[0]
	hashvalue=data[1]
	location=data[2]
	size=int(data[3])
	recvsize=0
	savefil=open(location,'wb')
	while recvsize<size :
		buff=server.recv(1024)
		savefil.write(buff)
		recvsize=recvsize+len(buff)
	savefil.close()
	#print('Received file '+filename)
	server.send(b'#sc#')

def restoredirectory(directory):
	try:
		if (os.path.isfile(directory+'.clonedir')==False):
			print('\nThe directory specified has not be backed up earlier')
			return 0
		identifier=open(directory+'.clonedir','r')
		server.send(b'#id#')
		if(recvserverreply()):
			server.send(str.encode(identifier.read()))
		if(recvserverreply()):
			server.send(b'#sc#')
			datalen=server.recv(1024)
		server.send(b'#sc#')
		data=server.recv(int(datalen.decode('utf-8'))).decode('utf-8')
		filelist=data.split('\n')
		currentfiles=utils.calcdirhash(directory).split('\n')
		lookupfiles={}
		neededfiles=[]
		for f in filelist:
			if len(f)>0:
				server.send(b'#sc#')
				recvfile(f)
				server.send(b'#sc#')
		return 1
	except:
		print('Receive Abort!')
		return 0
				
	


			




def syncdirectory(directory):
	try: 
		identifier=open(directory+'.clonedir','w')
		server.send(b'#hd#')
		hashdata=str.encode(utils.calcdirhash(directory))
		if(recvserverreply()):
			server.send(str.encode(str(len(hashdata))))
		if(recvserverreply()):
			server.send(hashdata)
		if(recvserverreply()):
			print('\nSent file details to engine. Waiting for reply...')
		server.send(b'#id#')
		identity=server.recv(256).decode("utf-8")
		server.send(b'#sc#')
		numfiles=int(server.recv(256).decode("utf-8"))
		identifier.write(identity)  #After database has been affected we can write the .clonedir file 
		identifier.close() 
		print(str(numfiles)+' files to be uploaded.')
		for i in range(0,numfiles):
			server.send(b'#sc#')
			filetobesent=server.recv(1024).decode("utf-8")
			server.send(b'#sc#')
			data=filetobesent.split('\t')
			filename=data[0]
			hashvalue=data[1]
			location=data[2]
			size=int(data[3])
			sentsize=0
			filetosend=open(location,'rb')
			recvserverreply()
			print('Sending file '+filename)
			nextdisplay=0
			while sentsize<size:
				buff=filetosend.read(1024)
				server.send(buff)
				sentsize=sentsize+len(buff)
				display=int((sentsize/size)*100)
				if display>=nextdisplay:
					print('\r '+str(display)+'%',end='')
					nextdisplay=nextdisplay+1
			print('\n')
			filetosend.close()
			recvserverreply()		
		server.close()
		return 1
	except :
		return 0


if __name__ == '__main__':
	args=sys.argv
	if(len(args)<=1):                        #First argument is filename when running from Python
		print('CloneDir Client utility\n\nBasic commands - \n\t1. <Directory name> -add  : Add a directory -restore')
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
				elif(args[i]=='-restore'):
					restoredirectory(directory)



