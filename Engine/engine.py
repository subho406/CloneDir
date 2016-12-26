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
		if(os.path.exists('./data')==False):
			os.mkdir('./data')
		dbcursor.execute('create table xxhashvals(hashvalue text primary key,filename text);')
		print('Setting things for the first time')
		dbconn.commit()
		return 1
	except sqlite3.Error as er:
		print('Error: '+er.args[0])
		return 0

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
	return 1
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
	if(c.recv(4)==b'#sc#'):    #Wait for reply from server
		return True		
	else:
		print('Client Lost')
def recvfile(c,f):
	data=f.split('\t')
	filename=data[0]
	hashvalue=data[1]
	location=data[2]
	size=int(data[3])
	recvsize=0
	savefil=open('./data/'+hashvalue+str(size),'wb')
	while recvsize<size :
		buff=c.recv(1024)
		savefil.write(buff)
		recvsize=recvsize+len(buff)
	savefil.close()
	filedata='"'+hashvalue+str(size)+'","'+filename+'"'
	insertdata('xxhashvals', filedata)
	print('recv')
	c.send(b'#sc#')

def restoredirectoryrequest(c):
	try:
		print('Restore Directory Request Received!')
		c.send(b'#sc#')
		identity=c.recv(256).decode("utf-8")
		dbcursor.execute('select * from '+identity+';')
		filesdata=dbcursor.fetchall()
		print(filesdata)
		data=''
		for f in filesdata:
			filename=f[0]
			hashvalue=f[1]
			location=f[2]
			size=str(f[3])
			data=data+'\n'+filename+'\t'+hashvalue+'\t'+location+'\t'+size
		c.send(b'#sc#')  #Successful generation of the data
		if(recvclientreply(c)):
			c.send(str.encode(str(len(data))))
		if(recvclientreply(c)):
			c.send(str.encode(data))
		for f in filesdata:
			filename=f[0]
			hashvalue=f[1]
			location=f[2]
			size=f[3]
			recvclientreply(c)
			print('Sending file '+filename)
			nextdisplay=0
			sentsize=0
			filetosend=open('./data/'+hashvalue+str(size),'rb')
			while sentsize<size:
				buff=filetosend.read(1024)
				c.send(buff)
				sentsize=sentsize+len(buff)
				display=int((sentsize/size)*100)
				if display>=nextdisplay:
					print('\r '+str(display)+'%',end='')
					nextdisplay=nextdisplay+1
			print('\n')
			filetosend.close()
			recvclientreply(c)
		c.close()
	except:
		print('\nSome files could not be restored\n')
		c.close()





	
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
	for n in neededfiles:
		recvclientreply(c)
		c.send(str.encode(n))
		recvclientreply(c)
		c.send(b'#sc#')
		print(n)
		recvfile(c,n)

	
	

		

def startdaemon():
	listener.listen()
	print('CloneDir Daemon Running...')
	while True:
		c,addr=listener.accept()
		recvdata=c.recv(5)
		if(recvdata==b'#hd#'):
			adddirectoryrequest(c)
		elif(recvdata==b'#id#'):
			restoredirectoryrequest(c)




					

if __name__ == '__main__':
	connecttodb()
	init()
	connecttoport()
	startdaemon()


