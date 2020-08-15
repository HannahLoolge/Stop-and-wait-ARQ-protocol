import socket
import sys

print "Enter host 1 name"
host1 = str(sys.stdin.readline())
#port = 6040
print "Enter host 2 name"
host2 = str(sys.stdin.readline())

print "Enter port 1 number"
port1 = int(sys.stdin.readline())

print "Enter port 2 number"
port2 = int(sys.stdin.readline())
#print "Enter frame size"
BUFFER_SIZE = 100000

bl=False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.connect((host1, port1))

M1 = raw_input("Client enter username:\n")
s.send(M1)
i=0

data = s.recv(1024)
if data == "Verified username\n":
	print data
	M2 = raw_input("Client enter password:\n")
	s.send(M2)
	res1 = s.recv(1024)

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s2.connect((host2, port2))
s2.send(M1)

data = s2.recv(1024)
if data == "Verified username\n":
	print data
	M2 = raw_input("Client enter password:\n")
	s2.send(M2)
	res2 = s2.recv(1024)

lst1=[]
lst2=[]

if res1 == "Verified username and password\n" and res2 == "Verified username and password\n":	
	print res1
	filename='kalidasa.txt'
	f = open(filename,'rb')
	l = f.read(BUFFER_SIZE)
	i=0
	while (l):
		i+=1
		print i
		if bl==False:
			s.sendall(l)
			lst1.append(l)
			bl=True
			print "Sent"
		else:
			s2.sendall(l)
			lst2.append(l)
			bl=False
			print "Sent else"
#			#print('Sent ',repr(l))
		l = f.read(BUFFER_SIZE)

	if bl==False:
		s.sendall(l)
		lst1.append(l)
		bl=True
		print "Sent"
	else:
		s2.sendall(l)
		lst2.append(l)
		bl=False
		print "Sent else"
	
	f.close()

	with open ('file1c', 'wb') as f1c:
		print 'file opened'
		for i in lst1:
			f1c.write(i)
		f1c.close()

	with open ('file2c', 'wb') as f2c:
		print 'file opened'
		for i in lst2:
			f2c.write(i)
		f2c.close()



elif data == "Verified username\n":
	print "Username and password didn't match\n"	
else:
	print "Username does not exist\n"

s.close()
s2.close()
