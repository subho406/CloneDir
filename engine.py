import sqlite3
import socket

dbconn=None
dbcursor=None

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
		

if __name__ == '__main__':
	connecttodb()
	insertdata(None)
	print(dbcursor.fetchall())
	dbcursor.execute('select * from file_details;')
	print(dbcursor.fetchall())
	dbconn.commit()
