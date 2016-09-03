"""
	Local Version of the main CloneDir Engine

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
		
def connecttoport(port):
	global listener
	listener=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
	if os.path.exists( "/tmp/clonedir" ):
  		os.remove( "/tmp/clonedir" )
	listener.bind("/tmp/clonedir")
if __name__ == '__main__':
	connecttodb()
	insertdata(None)
	connecttoport(10280)
	print(dbcursor.fetchall())
	dbcursor.execute('select * from file_details;')
	print(dbcursor.fetchall())
	dbconn.commit()
