import csv
import socket
import sys
from threading import Thread 
from SocketServer import ThreadingMixIn

def alternateL(lst1, lst2):
	return [sub[item] for item in range(len(lst2)) 
                      for sub in [lst1, lst2]] 

with open('login_credentials.csv', 'r') as file:
	reader = csv.reader(file)
	pwd = {}
	for row in reader:
		pwd[row[0]] = row[1]

TCP_IP = '0.0.0.0'
print "Enter the port number\n"
TCP_PORT = int(sys.stdin.readline())
BUFFER_SIZE = 100000

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Socket successfully created\n"

tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
bl=0

tcpServer.listen(1)
print "socket is listening\n"

print 'file opened'
print "Multithreaded Python server : Waiting for connections from TCP clients...\n"
(conn, (ip,port)) = tcpServer.accept() 
print "[+] New server socket thread started for " + ip + ":" + str(port) + "\n"

if bl == 0 :
	un = conn.recv(1024)
	print "Server received username: \n", un
	if pwd.get(un)!=None:
		print "Verify username\n"
		M = ("Verified username\n")
		conn.send(M)
		pw = conn.recv(1024)
		print "Server received password: \n", pw
		if pwd[un]==pw:
			M2 = ("Verified username and password\n")
			conn.send(M2)
			bl=1
		else:
			M2="Incorrect Password\n"
			conn.send(M2)
	else:
		M = ("Username does not exist\n")
		conn.send(M)
		

(conn1, (ip1, port1)) = tcpServer.accept()

if bl == 1:
	un = conn1.recv(1024)
	print "Server received username: \n", un
	if pwd.get(un)!=None:
		print "Verify username\n"
		M = ("Verified username\n")
		conn1.send(M)
		pw = conn1.recv(1024)
		print "Server received password: \n", pw
		if pwd[un]==pw:
			M2 = ("Verified username and password\n")
			conn1.send(M2)
			bl=2
		else:
			M2="Incorrect Password\n"
			conn1.send(M2)
	else:
		M = ("Username does not exist\n")
		conn1.send(M)

lst1 = []
lst2 = []

if bl>=2:
	while True:
		print('receiving data aaaaaaaaaaaa 1...')
		try:
			M3 = conn.recv(BUFFER_SIZE)
		except socket.error, ex:
			print ex
			print "Client " + ip + " "+ str(port) + "is exiting\n"
			break
		if not M3:
			break
		print port
		lst1.append(M3)

	while True:
		print('receiving data aaaaaaaaaaaa 2...')
		try:
			M3 = conn1.recv(BUFFER_SIZE)
		except socket.error, ex:
			print ex
			print "Client " + ip1 + " "+ str(port1) + "is exiting\n"
			break
		if not M3:
			break
		print port1
		lst2.append(M3)

with open('received_file', 'wb') as f:
	alt = alternateL(lst1, lst2)
	for i in alt:
		f.write(i)

conn1.close()
conn.close()