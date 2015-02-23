
#import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
serverSocket.bind(('',1290))
serverSocket.listen(5)

while True:
	#Establish the connection
	print 'Ready to serve...'
	(connectionSocket, addr) = serverSocket.accept()
	print 'Got connection from', addr[0], addr[1];
	try:
		message = connectionSocket.recv(2048)
		#print message
		#print message
		filename = message.split()[1];
		f = open(filename[1:])
		outputdata = f.read()
		f.close()

		#Send one HTTP header line into socket
		connectionSocket.send('HTTP/1.0 200 OK\r\n')
		connectionSocket.send('Content-Type: text/html\r\n\r\n')

		#Send the content of the requested file to the client
		connectionSocket.send(outputdata)

	except IOError:
		#Send response message for file not found
		print 'IOerror'
		connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n404')
		#Close client socket
		connectionSocket.close()

serverSocket.close()
	

