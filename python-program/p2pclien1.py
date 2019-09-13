import socket 
from _thread import *
import threading
import os
import time

def threaded(c):
	# print("hello") 
	while True: 
 
		data = c.recv(1024) 
		if not data: 
			print('Bye') 
			break

		data = data[::-1] 

		c.send(data)
	c.shutdown(socket.SHUT_RDWR)
	c.close()

def chunks(l, k):
	for i in range(0, len(l)-1, k):
		yield(l[i:i+k])

def Main():
	seed_ip = '127.0.0.1'
	seed_port = 12357
	seed_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	seed_s.connect((seed_ip, seed_port))
	node_list = ''
	while True:
		data = seed_s.recv(1024)
		if(not data):
			break
		node_list += str(data.decode('ascii'))
	
	# print(node_list)

	node_array = list(chunks((node_list.split(':')), 2))

	

	print(node_array)

	seed_s.shutdown(socket.SHUT_RDWR)
	seed_s.close()
	if os.fork() == 0:
		host = '127.0.0.1'

		port = 7900

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		time.sleep(5)
		s.connect((host, port))
		message = "client1"[::-1]
		while True:
			s.send(message.encode('ascii'))

			data = s.recv(1024)

			print('Recieved :', str(data.decode('ascii')))
			ans = input('\nDo you want to send the message again? :')
			if ans == 'y':
					continue
			else:
					break
		s.shutdown(socket.SHUT_RDWR)
		s.close()
		os._exit(0)
	else:
		host = ""
		port = 4570
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))

		print("listeniing socket binded to port", port)

		s.listen(5)
		print("socket is listening")
		while True:
			c, addr = s.accept()

			print('Connected to :', addr[0], ':', addr[1])

			start_new_thread(threaded, (c,))
		s.shutdown(socket.SHUT_RDWR)
		s.close()
	
if __name__ == '__main__': 
	Main() 
