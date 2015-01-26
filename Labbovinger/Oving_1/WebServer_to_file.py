
#import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
serverSocket.bind(('',1291))
serverSocket.listen(5)

while True:
	#Establish the connection
	print 'Ready to serve...'
	(connectionSocket, addr) = serverSocket.accept()
	print 'Got connection from', addr[0], addr[1];
	try:
		message = connectionSocket.recv(1024)
		#print message
		print message.split()[1]
		f = open(message.split()[1])
		outputdata = f.read()

		#Send one HTTP header line into socket
		connectionSocket.send('HTTP/1.0 200 OK\n')
		connectionSocket.send('Content-Type: text/html\n')
		#Send the content of the requested file to the client
		for i in range(0, len(outputdata)):
			connectionSocket.send(outputdata[i])
			connectionSocket.close()
	except IOError:
		#Send response message for file not found
		print 'IOerror'
		#connectionSocket.send('HTTP/1.1 404 Not Found\n\n')
		#Close client socket
		connectionSocket.close()
	serverSocket.close()

