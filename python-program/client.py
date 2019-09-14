import socket 
from _thread import *
import threading
import os
import time
import random

neighbours = []
listening_port = 0
#used for recieving from each connection -- #TODO implement gossip protocol - on recieving message, check in ML and forward to neighbours(except from where recieived) only if not present
def threaded(c):
	while True: 
 
		data = c.recv(1024) 
		if not data: 
			print('Bye') 
			break
		print(data.decode('ascii')[::-1])
		# data = data[::-1] 

		# c.send(data)
	# c.shutdown(socket.SHUT_RDWR)
	c.close()

#function to split an array into even chunks
def chunks(l, k):
	for i in range(0, len(l)-1, k):
		yield(l[i:i+k])

def grandchlid_to_send(node):
	global listening_port
	host = node[0]
	port = int(node[1])
	print(node)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.connect((host, port))
	# print("connected to " + node[0]+':'+node[1])
	message = ("client at " + str(listening_port))[::-1]
	# s.send(message.encode('ascii'))
	# for i in range(10):
	s.send(message.encode('ascii'))
	print("Message sent to", node)
		# time.sleep(5)
	# s.shutdown(socket.SHUT_RDWR)
	s.close()

def Main():
	global neighbours
	seed_ip = '127.0.0.1'
	seed_port = 12380
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
	neighbours = random.choices(node_array, k=random.choice(list(range(1,min(5, len(node_array)+1))) if len(node_array)>0 else [0]))

	print(neighbours)

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
		print("socket is listening for incoming connections")
		while True:
			c, addr = s.accept()
			print('Start recieving from :', addr[0] + ':' + str(addr[1]))
			neighbours.append([addr[0],str(addr[1])])
			start_new_thread(threaded, (c,))
		s.close()

	else:
		for i in range(10):
			print(neighbours)
			for node in neighbours:
				child = 0
				if not os.fork():
					child = os.getpid()
					grandchlid_to_send(node)
					os._exit(0)
				else:
					children.append(child)
					continue
			time.sleep(5)
		for child in children:
			os.waitpid(child, 0)
		os._exit(0)

if __name__ == '__main__': 
	Main() 
# 0 implies child