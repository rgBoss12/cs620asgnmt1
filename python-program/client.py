import socket 
from _thread import *
import threading
import os
import time
import random

#used for recieving from each connection
def threaded(c):
	while True: 
 
		data = c.recv(1024) 
		if not data: 
			print('Bye') 
			break
		print(data[::-1])
		# data = data[::-1] 

		# c.send(data)
	# c.shutdown(socket.SHUT_RDWR)
	c.close()

#function to split an array into even chunks
def chunks(l, k):
	for i in range(0, len(l)-1, k):
		yield(l[i:i+k])

def grandchlid_to_send(node):
	host = node[0]
	port = int(node[1])
	print(node)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.connect((host, port))
	print("connected to " + node[0]+':'+node[1])
	message = ("client at " + node[1])[::-1]
	# s.send(message.encode('ascii'))
	for i in range(10):
		s.send(message.encode('ascii'))
		time.sleep(5)
	# s.shutdown(socket.SHUT_RDWR)
	s.close()

def Main():
	seed_ip = '127.0.0.1'
	seed_port = 12357
	seed_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	seed_s.connect((seed_ip, seed_port))

	listening_port = seed_s.getsockname()[1]

	node_list = ''
	while True:
		data = seed_s.recv(1024)
		if(not data):
			break
		node_list += str(data.decode('ascii'))
	
	node_array = list(chunks((node_list.split(':')), 2))

	

	print(node_array)

	# seed_s.shutdown(socket.SHUT_RDWR)
	seed_s.close()
	children = []

	#parent process (this one) starts listening for incoming connections from other clients 
	child = os.fork()        
	if child:
		host = ""
		port = listening_port
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))

		print("listening socket binded to port", port)

		s.listen(5)
		print("socket is listening")
		while True:
			c, addr = s.accept()

			print('Connected to :', addr[0], ':', addr[1])

			start_new_thread(threaded, (c,))
		# s.shutdown(socket.SHUT_RDWR)
		s.close()
		# break
	else:
		# print('a')
		for node in random.choices(node_array, k=random.choice(list(range(1,min(5, len(node_array)+1))) if len(node_array)>0 else [0])):
			child = 0
			if not os.fork():
				child = os.getpid()
				grandchlid_to_send(node)
				# print('a')
				os._exit(0)
			else:
				children.append(child)
				continue
		for child in children:
			os.waitpid(child, 0)
		os._exit(0)
if __name__ == '__main__': 
	Main() 
# 0 implies child