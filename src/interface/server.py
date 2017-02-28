# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
import threading
import random


#This is the function that the thread uses to listen on the bluetooth socket.
#The parameter is a socket.
def btlistener(socket):
	while 1:
		try:
			data = socket.recv(1024)
			print("received: %s" % data)
		except:
			return

#Setup socket information
#returns a tuple of sockets
# client socket, then server socket
def get_sockets():
	server_sock=BluetoothSocket( RFCOMM )
	server_sock.bind(("",PORT_ANY))
	server_sock.listen(1)
	port = server_sock.getsockname()[1]
	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
	
	#Advertise bluetooth service from controller
	advertise_service( server_sock, "SampleServer",
	                   service_id = uuid,
	                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
	                   profiles = [ SERIAL_PORT_PROFILE ], 
	                    )
                   
	#Wait for connections
	print("Waiting for connection on RFCOMM channel %d" % port)
	client_sock, client_info = server_sock.accept()
	print("Accepted connection from ", client_info)
	return (client_sock, server_sock)

#Start the listener thread
def start_listener_thread(socket):
	t = threading.Thread(target=btlistener, args = (client_sock,))
	t.daemon = True
	t.start()

#please close the sockets after you're done
def close_sockets(sock1, sock2):
	sock1.close()
	sock2.close()
	print("Connection closed.")

def gen_input():
	tmp = "{"
	for i in range(1, 100):
		tmp += "{"
		for j in  range(0, 3):
			tmp += "\"" + str(random.uniform(0, 30)) + "\","
		tmp += "\"" + str(i) + "\""
		tmp += "}|"
	tmp += "}"
	return tmp

#print gen_input()


client_sock, server_sock = get_sockets()
start_listener_thread(client_sock)

#Sender Daemon
try:
    while True:
	#input loop
        data = raw_input(">")
        if len(data) == 0: break
	if data == "doit":
		client_sock.send("data_begin".encode("utf-8"))
		data = client_sock.recv(1024).decode("utf-8")
		print data
		if data == "ACK":
			data = gen_input()
			data.split("|")
			for chunk in data:
				chunk += "\n"
				client_sock.send(chunk.encode("utf-8"))
				client_sock.recv(1024)
		
	else:
		data += '\n' #concatenate a delimiter
	        client_sock.send(data.encode('utf-8'))
except IOError:
    pass

close_sockets(client_sock, server_sock)
