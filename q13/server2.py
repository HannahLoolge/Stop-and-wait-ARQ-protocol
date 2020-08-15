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
BUFFER_SIZE = int(raw_input("Enter buffer size : ") or "10000")
BUFFER_SIZE = 10000
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
tcpCl.settimeout(0.5)
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
			bl=True
			conn.send(res2)
			while True:
				print('receiving data...')
				try:
					data = conn.recv(BUFFER_SIZE)
				except socket.error, ex:
					print ex
					break
				if not data:
					break
				sth = calcChecksum(data)
				# print "checksumcal "+str(sth)
				zeros=5-(len(str(sth))%5)
				if zeros==5:
					zeros=0
				pad_str=""
				for i in range(zeros):
					pad_str=pad_str+"0"
				data = data + pad_str + str(sth)
				# print "len of data before pushing "+str(len(data))
				# print "data:- "+data+"\n\n\n\n\n"
				lst.append(data)
		else:
			conn.send(res2)
			print res2
	else:
		conn.send(res)
		print res

	x=0
	if bl==True:
		for i in lst:	
			if x%10!=0:	
				# print "len of i "+str(len(i))
				# print "data:- "+i
				tcpCl.sendall(i)
			else:
				print "OYOYOYOYOYOYOY"
				j = i[:-10]+'abcde'+i[-5:]
				tcpCl.sendall(i)
			print "last check "+i[-5]+i[-4]+i[-3]+i[-2]+i[-1]
			while True:
				try: 
					r2 = tcpCl.recv(2)
					print r2
					break
				except socket.timeout:
					tcpCl.sendall(i)
			time.sleep(0.1)
			x+=1
		tcpCl.close()

