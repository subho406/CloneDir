"""
	Local Version of the Main CloneDir Engine

			
			Engine Protocol
	
	1. Hash Data 
		1.1 #hd#
		1.2 Data size
		1.3 Hash data
	2. Files request
		2.1 #filesrequestbegin# <File request goes here> #filesrequestend#


			Database 

	1. Table for every new Directory
		filename text
		hashval varchar(80)
		location text
		size int


"""

import sqlite3
import socket
import os
import math

dbconn=None
dbcursor=None
listener=None
def generatedirectoryidentity():
	if(os.path.exists('./engine/clonedir')):
		data=open('./engine/clonedir','r')
		val=data.readline()
		val=int(val[2::])+1
		val='cd'+str(val)
		data.close()
		data=open('./engine/clonedir','w')
		data.write(val)
		data.close()
		return val
	else:
		data=open('./engine/clonedir','w')
		val='cd1'
		data.write(val)
		data.close()
		return val
def connecttodb():
	global dbcursor
	global dbconn
	dbconn = sqlite3.connect('./engine/engine.db')
	dbcursor=dbconn.cursor()
	#dbcursor.execute("create table if not exists file_details(filehash varchar2(64) PRIMARY KEY,filename varchar2(256),size int,timestamp varchar2(20));")
def dbcommit():
	dbconn.commit()
def insertdata(tablename,data):
	try:
		dbcursor.execute('insert into file_details values("test5","djjd",2002,"2gdd");')
	except sqlite3.Error as er:
		print('Error: '+er.message)
def createdirectorytable(tablename):
	try:
		dbcursor.execute('create table '+tablename+'(filename text,hashval varchar(80),location text,size int);')
		dbconn.commit()
	except sqlite3.Error as er:
		print('Error: '+er.message)

def connecttoport(port=None):
	global listener
	listener=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
	if os.path.exists( "/tmp/clonedir" ):
  		os.remove( "/tmp/clonedir" )
	listener.bind("/tmp/clonedir") 


def adddirectoryrequest(c):
	c.send(b'#sc#')
	datasize=int(c.recv(256).decode("utf-8"))
	c.send(b'#sc#')
	datarecv=0
	hashdata=''
	while datarecv<datasize:
		data=c.recv(256)
		datarecv=datarecv+len(data)
		hashdata=hashdata+data.decode("utf-8")
	c.send(b'#sc#')
	val=generatedirectoryidentity()
	if(c.recv(5)==b'#id#'):
		c.send(str.encode(val))
	hashdata=hashdata.split("\n")
	for h in hashdata:
		data=h.split('\t')
		if(len(data)==4):
			filename=data[0]
			hashvalue=data[1]
			location=data[2]
			size=data[3]
			print(size)
	createdirectorytable(val)
	

		

def startdaemon():
	listener.listen()
	print('CloneDir Daemon Running...')
	while True:
		c,addr=listener.accept()
		if(c.recv(5)==b'#hd#'):
			adddirectoryrequest(c)


					

if __name__ == '__main__':
	connecttodb()
	connecttoport()
	startdaemon()


