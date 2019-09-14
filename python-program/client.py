import socket 
from _thread import *
import threading
import os
import time
import random

lock = threading._RLock()
socks = []
# neighbours = []
listening_port = 0
#used for recieving from each connection -- #TODO implement gossip protocol - on recieving message, check in ML and forward to neighbours(except from where recieived) only if not present
def threaded(c):
	while True: 
		print("hello")
		data = c.recv(1024) 
		if not data: 
			print('Bye') 
			break
		print(data.decode('ascii')[::-1])
		# data = data[::-1] 

		# c.send(data)
	# c.shutdown(socket.SHUT_RDWR)
	c.close()

def listen_th():
	global listening_port
	global socks
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

		## increase in neighbours : to start sending message to them as well
		lock.acquire()
		socks.append(c)
		
		# print(neighbours)
		lock.release()
		# start_new_thread(threaded, (c,))
		thread = threading.Thread(target=threaded, args=(c,))
		thread.start()
	s.close()

#function to split an array into even chunks
def chunks(l, k):
	for i in range(0, len(l)-1, k):
		yield(l[i:i+k])

def grandchild_to_send(sock, node):
	global listening_port
	# host = node[0]
	# port = int(node[1])
	# print(node)
	# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	thread1 = threading.Thread(target=threaded, args=(sock,))
	thread1.start()
	# s.connect((host, port))
	# # print("connected to " + node[0]+':'+node[1])
	message = ("client at " + str(sock.getsockname()[1]))[::-1]
	# s.send(message.encode('ascii'))
	# for i in range(10):
	sock.send(message.encode('ascii'))
	print("Message sent to", str(sock.getpeername()[1]))
		# time.sleep(5)
	# s.shutdown(socket.SHUT_RDWR)
	# s.close()

def Main():
	global socks
	global listening_port

	## connects to the seed
	seed_ip = '127.0.0.1'
	seed_port = 12395

	seed_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	seed_s.connect((seed_ip, seed_port))

	listening_port = seed_s.getsockname()[1]
	
	## gets list of total active clients
	node_list = ''
	while True:
		data = seed_s.recv(1024)
		if(not data):
			break
		node_list += str(data.decode('ascii'))
	
	node_array = list(chunks((node_list.split(':')), 2))
	print(node_array)

	## pick your neighbours
	# lock.acquire()
	neighbours = random.choices(node_array, k=random.choice(list(range(1,min(5, len(node_array)+1))) if len(node_array)>0 else [0]))

	print(neighbours)
	# lock.release()
	## connection with seed closed
	seed_s.close()
	# children = []

	# child = os.fork()        
	## parent process (this one) starts listening for incoming connections from other clients 
	
	thread = threading.Thread(target=listen_th, args=())
	thread.start()

	# else:
	# socks = []
	# lock.acquire()
	# n1 = neighbours
	# lock.release()
	for node in neighbours:
		host = node[0]
		port = int(node[1])
		print(node)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, port))
		socks.append(s)
	old_length = len(neighbours)
	children = []
	for i in range(10):
		# print(neighbours)
		# lock.acquire()
		# n2 = neighbours
		# lock.release()
		# print(len(n2))
		# for node in n2[old_length:]:
		# 	host = node[0]
		# 	port = int(node[1])
		# 	print(node)
		# 	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# 	s.connect((host, port))
		# 	# print("connected to " + node[0]+':'+node[1])
		# 	# message = ("client at " + str(listening_port))[::-1]
		# 	socks.append(s)
		indx = 0
		for sock in socks:
			indx += 1
			child = 0
			print(indx)
			if not os.fork():
				child = os.getpid()
				grandchild_to_send(sock, indx)
				os._exit(0)
			else:
				children.append(child)
				continue
		# old_length = len(n2)
		time.sleep(5)
	for child in children:
		os.waitpid(child, 0)
	for sock in socks:
		sock.close()
		# os._exit(0)

if __name__ == '__main__': 
	Main() 
# 0 implies child