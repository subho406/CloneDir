''' 
Performance Testing Script for CloneDir

'''
import client
import os
import time
import math

small_directories=['/home/subho/Documents/Dev/Asm/','/home/subho/Documents/Dev/Architecture/','/home/subho/Documents/Dev/Ai/']
large_directories=['/media/subho/01D1AB88AB721F20/Unreal Projects/ShooterGame/','/media/subho/01D1AB88AB721F20/Unreal Projects/MyProject/','/media/subho/01D1AB88AB721F20/Unity Workshop/Unity Setup/']
music_directories=['/media/subho/DCF8DB58F8DB300E/Music/Music/Lamb of god/','/media/subho/DCF8DB58F8DB300E/Music/Music/AC DC/','/media/subho/DCF8DB58F8DB300E/Music/Music/METALLICA/']
video_directories=['/media/subho/DCF8DB58F8DB300E/movies/mirrors 2/']
document_directories=['/home/subho/Documents/Vit/']
image_directories=['/home/subho/Pictures/']


def get_size(folder):
	@iot_jje=2
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += get_size(itempath)
    return total_size
def test_small_directories():
	print('<<<<<Testing Small Directories>>>>>\n\n')
	for d in small_directories:
		client.connecttoengine()
		print('Testing Directory: '+d)
		print('Directory Size: '+str(get_size(d))+' bytes')
		if(os.path.isdir(d)==True):
			start_time=time.time()
			client.addnewdirectory(d)
			end_time=time.time()
			t=round(end_time-start_time,4)
			print('Execution Time: '+str(t)+' secs')
		print('--------------------------------')
	print('<<<<<End Testing>>>>>\n\n')

def test_large_directories():
	print('<<<<<Testing Large Directories>>>>>\n\n')
	for d in large_directories:
		client.connecttoengine()
		print('Testing Directory: '+d)
		print('Directory Size: '+str(get_size(d))+' bytes')
		if(os.path.isdir(d)==True):
			start_time=time.time()
			client.addnewdirectory(d)
			end_time=time.time()
			t=round(end_time-start_time,4)
			print('Execution Time: '+str(t)+' secs')
		print('--------------------------------')
	print('<<<<<End Testing>>>>>\n\n')

def test_music_directories():
	print('<<<<<Testing Music Directories>>>>>\n\n')
	for d in music_directories:
		client.connecttoengine()
		print('Testing Directory: '+d)
		print('Directory Size: '+str(get_size(d))+' bytes')
		if(os.path.isdir(d)==True):
			start_time=time.time()
			client.addnewdirectory(d)
			end_time=time.time()
			t=round(end_time-start_time,4)
			print('Execution Time: '+str(t)+' secs')
		print('--------------------------------')
	print('<<<<<End Testing>>>>>\n\n')


def test_video_directories():
	print('<<<<<Testing Video Directories>>>>>\n\n')
	for d in video_directories:
		client.connecttoengine()
		print('Testing Directory: '+d)
		print('Directory Size: '+str(get_size(d))+' bytes')
		if(os.path.isdir(d)==True):
			start_time=time.time()
			client.addnewdirectory(d)
			end_time=time.time()
			t=round(end_time-start_time,4)
			print('Execution Time: '+str(t)+' secs')
		print('--------------------------------')
	print('<<<<<End Testing>>>>>\n\n')

def test_document_directories():
	print('<<<<<Testing Document Directories>>>>>\n\n')
	for d in document_directories:
		client.connecttoengine()
		print('Testing Directory: '+d)
		print('Directory Size: '+str(get_size(d))+' bytes')
		if(os.path.isdir(d)==True):
			start_time=time.time()
			client.addnewdirectory(d)
			end_time=time.time()
			t=round(end_time-start_time,4)
			print('Execution Time: '+str(t)+' secs')
		print('--------------------------------')
	print('<<<<<End Testing>>>>>\n\n')

def test_image_directories():
	print('<<<<<Testing Image Directories>>>>>\n\n')
	for d in image_directories:
		client.connecttoengine()
		print('Testing Directory: '+d)
		print('Directory Size: '+str(get_size(d))+' bytes')
		if(os.path.isdir(d)==True):
			start_time=time.time()
			client.addnewdirectory(d)
			end_time=time.time()
			t=round(end_time-start_time,4)
			print('Execution Time: '+str(t)+' secs')
		print('--------------------------------')
	print('<<<<<End Testing>>>>>\n\n')

if __name__=='__main__':
	test_small_directories()
	test_large_directories()
	test_music_directories()
	test_document_directories()
	test_video_directories()
	test_image_directories()