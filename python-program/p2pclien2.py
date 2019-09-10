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
	c.close()

def Main():
	if os.fork() == 0:
		host = '127.0.0.1'

		port = 4567

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		time.sleep(5)
		s.connect((host, port))
		message = "client2"[::-1]
		while True:
			s.send(message.encode('ascii'))

			data = s.recv(1024)

			print('Recieved :', str(data.decode('ascii')))
			ans = input('\nDo you want to send the message again? :')
			if ans == 'y':
					continue
			else:
					break
		s.close()
		os._exit(0)
	else:
		host = ""
		port = 7890
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))

		print("listeniing socket binded to port", port)

		s.listen(5)
		print("socket is listening")
		while True:
			c, addr = s.accept()

			print('Connected to :', addr[0], ':', addr[1])

			start_new_thread(threaded, (c,))
		s.close()
	
if __name__ == '__main__': 
	Main() 
