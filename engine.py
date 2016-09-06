"""
	Local Version of the Main CloneDir Engine

			
			Engine Protocol
	
	1. Hash Data 
		1.1 #hashdatabegin# <Some data here> #hashdataend#
	2. Files request
		2.1 #filesrequestbegin# <File request goes here> #filesrequestend#

"""
import sqlite3
import socket
import os

dbconn=None
dbcursor=None
listener=None

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

def startdaemon():
	listener.listen()
	print('CloneDir Daemon Running...')
	while True:
		c,addr=listener.accept()
		while True:	
			data=c.recv(100)
			if(data==b''):
				print('Session closed!')
				c.close()
				break
			print(data)


if __name__ == '__main__':
	connecttodb()
	connecttoport()
	startdaemon()

