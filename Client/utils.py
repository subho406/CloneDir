"""
Contains all the utilities used by client to calculate hash values of files in a directory	
"""

import os
import hashlib
import xxhash


##Constants area ##
buflen=2047  
mbmul=1024*1024
## Constants end##


def calcdirhash(dirname):
	hashdata=""
	dirs=os.listdir(dirname)
	i=0
	for subdirs,dirs,files in os.walk(dirname):
		subdirs+="/"
		for f in files:
			stat=os.stat(subdirs+f)
			hashdata+=f+"\t"+hashvalxx(subdirs+f)+"\t"+subdirs+f+"\t"+str(stat.st_size)
			hashdata+="\n"
			i=i+1
			print('\rProcessed '+str(i)+' files',end='')
								
	return hashdata


def hashvalxx(file):
	val=xxhash.xxh64()
	f=open(file,'rb')
	filelen=buflen
	buf=f.read(buflen)
	lim=100
	while buf!=b"":
		val.update(buf)
	
		buf=f.read(buflen)
		filelen+=buflen
	return val.hexdigest()

