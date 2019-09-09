# import socket programming library 
import socket 

# import thread module 
from _thread import *
import threading 

# print_lock = threading.Lock() 

# thread fuction 
def threaded_recv():
	host = ""

	port = 7890
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))

	print("listeniing socket binded to port", port)

	s.listen()
	while True:
		c, addr = s.accept

		print('Connected to :', addr[0], ':', addr[1])

		while True:
			data = c.recv(1024)
			if not data:
					break
			c.send(data)
		c.close()
	s.close()

def threaded_send():
	host = '127.0.0.1'

	port = 4567

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.bind((host, 4568))
	print("socket binded to port", 4568)

	s.connect((host, port))
	message = "client1"[::-1]
	while True:
		s.send(message.encode('ascii'))

		data = s.recv(1024)

		print('Recieved :', str(data.encode('ascii')))
		ans = input('\nDo you want to send the message again? :')
		if ans == 'y':
				continue
		else:
				break
	s.close()


def Main():
	start_new_thread(threaded_send, ())
	start_new_thread(threaded_recv, ()) 
	# host = "" 
	
	# port = 1547
	# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	# s.bind((host, port)) 
	# print("socket binded to port", port) 

	# # put the socket into listening mode 
	# s.listen(5) 
	# print("socket is listening") 

	# # a forever loop until client wants to exit 
	# while True: 

	# 	# establish connection with client 
	# 	c, addr = s.accept() 

	# 	# lock acquired by client 
	# 	# print_lock.acquire() 
	# 	print('Connected to :', addr[0], ':', addr[1]) 

	# 	# Start a new thread and return its identifier 
	# 	start_new_thread(threaded, (c,)) 
	# s.close() 


if __name__ == '__main__': 
	Main() 
