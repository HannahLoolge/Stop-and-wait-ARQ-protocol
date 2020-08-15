import csv
import sys
import socket
from threading import Thread 
from SocketServer import ThreadingMixIn

def calcChecksum(msg):
	s=0
	for i in range(0,len(msg), 2):
		a = ord(msg[i])
		b = ord(msg[i+1])
		s = s+ (a+(b << 8))

	s = s + (s>>16)
	s = ~s & 0xffff
	return s

def extr(data):
	s = data[-5]
	s = s+data[-4]
	s = s+data[-3]
	s = s+data[-2]
	s = s+data[-1]
	return int(s)

class ClientThread(Thread):
	"""docstring for ClientThread"""
	def __init__(self, conn, ip, port, lst, b, bl):
		Thread.__init__(self) 
		self.conn = conn
		self.ip = ip
		self.port = port
		self.lst = lst
		self.b = b # to store whether the username and pwd is verified
		self.bl = bl
		print "[+] New server socket thread started for " + ip + ":" + str(port) + "\n"

	def run(self):
		un = self.conn.recv(BUFFER_SIZE)
		print "Server received username: \n", un
		if pwd.get(un)!=None:
			print "Verify username\n"
			M = ("Verified username\n")
			self.conn.send(M)
			pw = self.conn.recv(BUFFER_SIZE)
			print "Server received password: \n", pw
			if pwd[un]==pw:
				M2 = ("Verified username and password\n")
				self.conn.send(M2)
				self.b = True
			else:
				M2 = "Incorrect Password\n"
				self.conn.send(M2)
		else:
			M = ("Username does not exist\n")
			self.conn.send(M)

		print "111111"

		# if self.b == True:
		print "333333"
		while True:
			print "receiving data"
			data = self.conn.recv(BUFFER_SIZE+5)
			if not data:
				break
			# print "LEN OF DATA "+str(len(data))
			cks = int(data[-5:])
			print 'cksyo '+str(cks)
			data = data[:-5]
			ccks = calcChecksum(data)
			print 'ccksyo '+str(ccks)
			if ccks == cks:
				re = 'cr'
				self.conn.send(re)
				self.lst.append(data)
			else:
				print "error detected........................."
		print "222222"

with open('login_credentials.csv', 'r') as file:
	reader = csv.reader(file)
	pwd = {}
	for row in reader:
		pwd[row[0]] = row[1]

bl1 = []
bl2 = []
b1 = False
b2 = False
lst1 = []
lst2 = []

TCP_IP = '0.0.0.0'
print "Enter the port number\n"
TCP_PORT = int(sys.stdin.readline())
BUFFER_SIZE = int(raw_input("Enter buffer size : ") or "10000")
BUFFER_SIZE = 10000
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Socket successfully created\n"

tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))

threads = []

tcpServer.listen(1)
print "socket is listening\n"
	
print "Multithreaded Python server : Waiting for connections from TCP clients...\n"
(conn1, (ip1,port1)) = tcpServer.accept() 
newthread1 = ClientThread(conn1,ip1,port1,lst1, b1, bl1)
newthread1.start()
threads.append(newthread1)

print "Multithreaded Python server : Waiting for connections from TCP clients...\n"
(conn2, (ip2,port2)) = tcpServer.accept() 
newthread2 = ClientThread(conn2,ip2,port2,lst2, b2, bl2)
newthread2.start()
threads.append(newthread2)

print"444444"
newthread1.join()		
print"555555"
newthread2.join()
print "lst1"
print "lst2"

with open ('file1', 'wb') as f1:
	# print 'file opened'
	for i in range(len(lst1)):
		f1.write(lst1[i])
	f1.close()

with open ('file2', 'wb') as f2:
	# print 'file opened 2'
	for i in range(len(lst2)):
		f2.write(lst2[i])
	f2.close()

boo = False
with open ('file1', 'rb') as f1:
	# print 'file1 opened'
	l1 = f1.read(BUFFER_SIZE)
	with open ('file2', 'rb') as f2:
		# print 'file2 opened'
		l2 = f2.read(BUFFER_SIZE)
		with open('received_file', 'wb') as f:
			print 'file r_f opened'
			while ((l1) or (l2)):
				if boo==False:
					f.write(l1)
					l1 = f1.read(BUFFER_SIZE)
					boo=True
				else:
					f.write(l2)
					l2 = f2.read(BUFFER_SIZE)
					boo=False
			if boo==False:
				f.write(l1)
				boo=True
			else:
				f.write(l2)
				boo=False
		f.close()
	f2.close()
f1.close() 


