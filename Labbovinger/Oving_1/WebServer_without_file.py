
#import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
#Fill in start
serverSocket.bind(('',1291))
serverSocket.listen(5)

#Fill in end
while True:
	#Establish the connection
	print 'Ready to serve...'
	(connectionSocket, addr) = serverSocket.accept()
	print 'Got connection from', addr[0], addr[1];
	try:
		message = connectionSocket.recv(1024)
		#ripnt message
		print message.split()[1]
		#Send one HTTP header line into socket
		#Fill in start
		connectionSocket.send('HTTP/1.0 200 OK\n')
		connectionSocket.send('Content-Type: text/html\n')
		connectionSocket.send('\n')
		connectionSocket.send("""
			<html>
			<body>
			<h1>Hello, World!</h1>
			</body>
			</html>
			""")
	except IOError:
		#Send response message for file not found
		#Fill in start
		print 'IOerror'
		connectionSocket.send('HTTP/1.1 404 Not Found\n\n')
		#Fill in end
		#Close client socket
		#Fill in start
		connectionSocket.close()
		#Fill in end
	finally:
		connectionSocket.close()
		serverSocket.close()
	break

