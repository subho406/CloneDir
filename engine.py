"""
	Local Version of the Main CloneDir Engine

			
			Engine Protocol
	
	1. Hash Data 
		1.1 #hd#
		1.2 Data size
		1.3 Hash data
	2. Files request
		2.1 #filesrequestbegin# <File request goes here> #filesrequestend#

"""
import sqlite3
import socket
import os
import math

dbconn=None
dbcursor=None
listener=None
buffsize=16
buff=b''
#Instruction codes
keywords={b'#hd#':0}
#Instruction codes end
readkeyword=True
readsize=False
receivedata=False
datarecvsize=0
datasize=None
databuffer=''
def connecttodb():
	global dbcursor
	global dbconn
	dbconn = sqlite3.connect('./engine/engine.db')
	dbcursor=dbconn.cursor()
	dbcursor.execute("create table if not exists file_details(filehash varchar2(64) PRIMARY KEY,filename varchar2(256),size int,timestamp varchar2(20));")

def insertdata(data):
	try:
		dbcursor.execute('insert into file_details values("test5","djjd",2002,"2gdd");')
	except sqlite3.Error as er:
		print('Error: '+er.message)
		
def connecttoport(port=None):
	global listener
	listener=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
	if os.path.exists( "/tmp/clonedir" ):
  		os.remove( "/tmp/clonedir" )
	listener.bind("/tmp/clonedir")

def checkhashmatch(hashval):
	if(keywords[b'#hd#']==hashval):
		readkeyword=False
		readsize=True
		return
	

def findinst():
	global buff
	global readkeyword
	global readsize
	print(buff)
	if(buff==b'#hd#'):
		readkeyword=False
		readsize=True
		return True


		




def startdaemon():
	listener.listen()
	global buff
	global readkeyword
	global receivedata
	global readsize
	global datarecvsize
	global datasize
	global databuffer
	print('CloneDir Daemon Running...')
	while True:
		c,addr=listener.accept()
		while True:
			data=c.recv(256)
			if(data==b''):
				print('Session closed!')
				buff=b''
				c.close()
				break
			buff=data 
			if(readkeyword==True):
				if(findinst()):
					c.send(b'#sc#')
			elif(readsize==True):
				c.send(b'#sc#')
				datasize=int(bytes.decode(data))
				readsize=False
				receivedata=True
			elif (receivedata==True):
				datarecvsize=datarecvsize+len(buff)
				if(datarecvsize<datasize):
					databuffer=databuffer+bytes.decode(data)
				else:
					c.send(b'#sc#')
					print(databuffer)
					databuffer=''
				
				


			
			

			


if __name__ == '__main__':
	connecttodb()
	for key,value in keywords.items():
		wordhash=0
		for i in range(0,4):  
			wordhash=wordhash+key[i]*math.pow(256,3-i)
		keywords[key]=wordhash
	connecttoport()
	startdaemon()

