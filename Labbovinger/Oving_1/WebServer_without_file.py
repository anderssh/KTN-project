
#import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
#Fill in start
serverSocket.bind(('',1288))
serverSocket.listen(5)

#Fill in end
while True:
	#Establish the connection
	print 'Ready to serve...'
	(connectionSocket, addr) = serverSocket.accept()
	print 'Got connection from', addr[0], addr[1];
	try:
		connectionSocket.recv(1024)

		#Send one HTTP header line into socket
		connectionSocket.send('HTTP/1.0 200 OK\r\n')
		connectionSocket.send('Content-Type: text/html\r\n')
		connectionSocket.send('\r\n')
		connectionSocket.send("""
			<html>
			<body>
			<h1>Hello, World!</h1>
			</body>
			</html>
			""")
	except IOError:
		#Send response message for file not found
		print 'IOerror'
		connectionSocket.send('HTTP/1.1 404 Not Found\n\n')

		#Close client socket
		connectionSocket.close()
	except KeyboardInterrupt:
		print "asdfasdfsdfasdf"
		connectionSocket.close()
		serverSocket.close()
		raise

		


