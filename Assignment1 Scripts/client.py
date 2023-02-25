import socket
import sys
import os
from socket import *
#define constant
BUFFER_SIZE = 1024
ACTIVE_MODE = "1"
PASSIVE_MODE = "2"

#def main(argv):



serverName = 'hostname'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('input lowercase sentence:')#raw_input no longer valid
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()


