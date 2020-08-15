import csv
import sys
import socket
from threading import Thread 
from SocketServer import ThreadingMixIn

def alternateL(lst1, lst2):
	return [sub[item] for item in range(len(lst2)) 
                      for sub in [lst1, lst2]] 

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
			# try:
			data = self.conn.recv(BUFFER_SIZE)
			# except socket.error, ex:
			# 	print ex
			# 	break
			if not data:
				break
			self.lst.append(data)
			print self.port

		print "222222"
		# return self.bl 


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
BUFFER_SIZE = 100000

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Socket successfully created\n"

tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))

threads = []

tcpServer.listen(1)
print "socket is listening\n"
	
#while len(bl1) == 0 and len(bl2) == 0:	
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
# while len(bl1)==0 and len(bl2)==0:
# 	print "here"
# 	if len(bl1)>0 and len(bl2)>0:
# 		break

# if len(bl1)>0 and len(bl2)>0:
print "lst1"
# for i in lst1:
# 	print i 

print "lst2"
# for i in lst2:
# 	print i

with open ('file1', 'wb') as f1:
	print 'file opened'
	for i in lst1:
		f1.write(i)
	f1.close()

with open ('file2', 'wb') as f2:
	print 'file opened 2'
	for i in lst2:
		f2.write(i)
	f2.close()

# with open('received_file', 'wb') as f:
# 	print 'file opened'
# 	alt = alternateL(lst1, lst2)
# 	for i in alt:
# 		f.write(i)
# 	f.close()
boo = False
with open ('file1', 'rb') as f1:
	print 'file1 opened'
	l1 = f1.read(BUFFER_SIZE)
	with open ('file2', 'rb') as f2:
		print 'file2 opened'
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


