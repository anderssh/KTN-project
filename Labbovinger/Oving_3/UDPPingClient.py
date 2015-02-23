import socket
from socket import *
#from time import *
import time
import datetime
UDP_IP = "localhost"
UDP_PORT_SERVER = 12004
UDP_PORT_CLIENT = 11005

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind((UDP_IP,UDP_PORT_CLIENT))
clientSocket.settimeout(1)

serverAdress = (UDP_IP,UDP_PORT_SERVER)
counter = 0

while counter < 10:
	counter += 1
	start = datetime.datetime.now()
	outgoingMessage = "Ping " + str(counter) + " " + str(start)
	clientSocket.sendto(outgoingMessage, serverAdress)
	try:
		reply, __ = clientSocket.recvfrom(1024)
		end = datetime.datetime.now()
		roundtime = end - start

		thePrint = reply[:-26] + str(roundtime.microseconds) +"ms"
		print thePrint
	except timeout:
		print ("Request timed out")