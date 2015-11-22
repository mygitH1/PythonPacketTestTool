
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket
import os
import sys
import subprocess


# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

	recvBuff = ""
	tmpBuff = ""
	while len(recvBuff) < numBytes:
		sys.stdout.flush()
		tmpBuff =  sock.recv(numBytes)
		if not tmpBuff:
			break
		recvBuff += tmpBuff
	return recvBuff

listenPort=1234
if len(sys.argv)==2:
	listenPort = int(sys.argv[1])
	
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcomeSock.bind(('', listenPort))
welcomeSock.listen(1)
print "Waiting for connections on port num:",listenPort
clientSock, addr = welcomeSock.accept()
print "Accepted connection from client: ", addr
print "\n"

while True:
	action=clientSock.recv(1024)
	if action=="get":
		fileName=clientSock.recv(1024)
		
		fileObj = open(fileName, "r")
		fileData=fileObj.read()
		clientSock.send(fileData)
		print "SUCCESS"
	elif action=="put":	
			fileData = ""
			recvBuff = ""
			fileSize = 0	
			fileSizeBuff = ""
			fileSizeBuff = recvAll(clientSock, 10)
			fileSize = int(fileSizeBuff)
			
			# print "The file size is "+fileSize+" Bytes"
			fileData = recvAll(clientSock, fileSize)
			
			filename=clientSock.recv(1024)
			fpw=open(filename,"w")
			fpw.write(fileData)
			fpw.close()
			print "SUCCESS"
	elif action=="ls":
			print "SUCCESS"
	elif action=="quit":
		exit(0)
	else:
                print "FAILURE"
		#exit(0)
	# elif action=="ls":
		# s=""
		# p = subprocess.Popen('dir /b', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		# for line in p.stdout.readlines():
			# s+=line+"\n"
		# clientSock.send(s)
		
		
clientSock.close()
