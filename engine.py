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
def init():
	try:
		dbcursor.execute('create table if not exists xxhashvals(hashvalue primary key,filename text,startpointer text,endpointer int);')
		print('Setting things for the first time')
		dbconn.commit()
	except sqlite3.Error as er:
		print('Error: '+er.args[0])

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
		dbcursor.execute('insert into '+tablename+' values('+data+');')
	except sqlite3.Error as er:
		print('Error: '+er.args[0])
def createdirectorytable(tablename):
	try:
		dbcursor.execute('create table '+tablename+'(filename text,hashval varchar(80),location text,size int);')
		dbconn.commit()
	except sqlite3.Error as er:
		print('Error: '+er.args[0])

def connecttoport(port=None):
	global listener
	listener=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
	if os.path.exists( "/tmp/clonedir" ):
  		os.remove( "/tmp/clonedir" )
	listener.bind("/tmp/clonedir") 

def recvclientreply(c):
	if(c.recv(5)==b'#sc#'):    #Wait for reply from server
		return True		
	else:
		print('Client Lost')

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
	createdirectorytable(val)
	hashdata=hashdata.split("\n")
	neededfiles=[]
	for h in hashdata:
		data=h.split('\t')
		if(len(data)==4):
			filename=data[0]
			hashvalue=data[1]
			location=data[2]
			size=data[3]
			values='"'+filename+'"'+',"'+hashvalue+'"'+',"'+location+'",'+size
			insertdata(val,values)
			dbcursor.execute('select * from xxhashvals where hashvalue="'+hashvalue+str(size)+'";')
			fetchdata=dbcursor.fetchall()
			if(len(fetchdata)==0):
				neededfiles.append(h) 
	dbconn.commit()
	print('Added a new folder\nThe following files need to be uploaded')
	print(neededfiles)
	if(recvclientreply(c)):
		c.send(str.encode(str(len(neededfiles))))
		
	
	

		

def startdaemon():
	listener.listen()
	print('CloneDir Daemon Running...')
	while True:
		c,addr=listener.accept()
		if(c.recv(5)==b'#hd#'):
			adddirectoryrequest(c)


					

if __name__ == '__main__':
	connecttodb()
	init()
	connecttoport()
	startdaemon()


