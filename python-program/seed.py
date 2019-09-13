# # first of all import the socket library 
# import socket
# from array import *			 

# # next create a socket object 
# s = socket.socket()		 
# print("Socket successfully created")

# # reserve a port on your computer in our 
# # case it is 12345 but it can be anything 
# port = 12357	

# # Next bind to the port 
# # we have not typed any ip in the ip field 
# # instead we have inputted an empty string 
# # this makes the server listen to requests 
# # coming from other computers on the network 
# s.bind(('', port))		 
# print("socket binded to %s" %(port))

# # put the socket into listening mode 
# s.listen(5)	 
# print("socket is listening")

# # a forever loop until we interrupt it or 
# # an error occurs
# CL=[[]]

# while True: 
# 	c, addr = s.accept()	 
# 	print('Got connection from', addr)

# 	CL.append([addr[0],str(addr[1])])
# 	print(CL)
	
# 	str1 =''
	
# 	for i in CL:
# 		str1 = str1.join(i)
# 	print(str1)
# 	c.send(str1.encode('ascii'))

# 	c.shutdown(socket.SHUT_RDWR)
# 	c.close() 


import socket
from array import *          

s = socket.socket()      
print("Socket successfully created")

port = 12357   

s.bind(('', port))       
print("socket binded to %s" %(port))

s.listen(5)  
print("socket is listening")

CL=[[]]

while True: 
	c, addr = s.accept()     
	print('Got connection from', addr)

	CL.append([addr[0],str(addr[1])])
	print(CL)
	
	str1 =''
	
	for i in CL:
		for j in i:
			str1 = str1 + j + ":"

	# str1 = str1.join(i)
	print(str1)
	c.send(str1.encode('ascii'))

	c.shutdown(socket.SHUT_RDWR)
	c.close() 

s.shutdown(socket.SHUT_RDWR)
s.close()