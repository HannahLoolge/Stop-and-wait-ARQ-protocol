import csv
import socket
import sys
import time

def calcChecksum(msg):
	s=0
	for i in range(0,len(msg), 2):
		a = ord(msg[i])
		b = ord(msg[i+1])
		s = s+ (a+(b << 8))

	s = s + (s>>16)
	s = ~s & 0xffff
	return s

TCP_IP = '0.0.0.0'
print "Enter port number\n"
TCP_PORT = int(sys.stdin.readline())
BUFFER_SIZE = int(raw_input("Enter buffer size : ") or "100000")

fr = open('ask.rtl', 'r')
read1 = csv.reader(fr)

for row in read1:
	print row[0] + " "+row[1]+" "+row[2]+" "
	hostT = row[1]
	portT = row[2]
	
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Socket successfully created\n"

tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))

tcpServer.listen(1)
print "socket is listening\n"

tcpCl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpCl.connect((hostT, int(portT)))

bl=False

while True:
	print "Multithreaded Python server : Waiting for connections from TCP clients...\n"
	(conn, (ip,port)) = tcpServer.accept() 
	print "[+] New server socket thread started for " + ip + ":" + str(port) + "\n"
	
	lst = []

	un = conn.recv(1024)
	print "Server received username: \n", un

	tcpCl.send(un)
	res = tcpCl.recv(1024)
	if res == "Verified username\n":
		conn.send(res)
		print res
		pw = conn.recv(1024)
		print "Server received password: \n", pw
		tcpCl.send(pw)
		res2 = tcpCl.recv(1024)
		if res2 == "Verified username and password\n" :
			conn.send(res2)
			bl=True
			while True:
				print('receiving data...')
				try:
					data = conn.recv(BUFFER_SIZE)
				except socket.error, ex:
					print ex
					break
				if not data:
					break
				lst.append(data)
		else:
			conn.send(res2)
			print res2
	else:
		conn.send(res)
		print res

	with open ('file11', 'wb') as f11:
		print 'file opened'
		for i in lst:
			f11.write(i)
		f11.close()


	if bl==True:
		for i in lst:
			print "sending data."
			tcpCl.sendall(i)
		tcpCl.close()


