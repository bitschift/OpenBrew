# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
import threading
import random
import json
import os
import sys
import stat, os

fifo_path = "/tmp/btcomm.fifo"
state = 0

def fiforw(message):
    if(message == None):
        fifo = open(fifo_path, 'r')
        string = ""
        for line in fifo:
            string += line
        return string
    fifo = open(fifo_path, 'w')
    fifo.write(message)
    fifo.close()

#This is the function that the thread uses to listen on the bluetooth socket.
#The parameter is a socket.
def btlistener(socket):
	while 1:
		try:
			data = socket.recv(1024)
			if data == "dataReq\n":
				print("Data start.")
				client_sock.send("data_begin".encode("utf-8"))

				data = gen_input(True)
				data = data.split("|")
				for chunk in data:
					client_sock.send((chunk+"\n").encode("utf-8"))
					client_sock.recv(1024)
				client_sock.send("data_end".encode("utf-8"))
				print( "Data sent!")
			elif data == "start\n":
				fiforw("start")
				print("Received start command.")
				state = 2
			else:
				print("Recieved: %s" % data)
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
	advertise_service(
			   server_sock, "cody-Lenovo-B590",
	                   service_id = uuid,
	                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
	                   profiles = [ SERIAL_PORT_PROFILE ], 
	                 )
                   
	#Wait for connections
	print("Waiting for connection on RFCOMM channel %d" % port)
	client_sock, client_info = server_sock.accept()
	print("Accepted connection from ", client_info)
	return (client_sock, server_sock)
'''
def find_device():
	device = None
	n = None
	server_sock=BluetoothSocket( RFCOMM )
	server_sock.bind(("",PORT_ANY))
	server_sock.listen(1)
	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
	advertise_service(
			   server_sock, "cody-Lenovo-B590",
	                   service_id = uuid,
	                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
	                   profiles = [ SERIAL_PORT_PROFILE ], 
	                 )
	near_devices = discover_devices(lookup_names = True)
	for addr,name in near_devices:
		print "Name: " + name + " Address: " + addr
		if name == "BrewAIUI":
			device = addr
			n = name
	near_devices = find_service(address = addr)
	for services in near_devices:
		print " Name: %s" % (services["name"])
		print " Description: %s" % (services["description"])
		print " Protocol: %s" % (services["protocol"])
		print " Provider: %s" % (services["provider"])
		print " Port: %s" % (services["port"])
		print " Service id: %s" % (services["service-id"])
	
	client_sock=BluetoothSocket( RFCOMM )
	client_sock.bind(("",PORT_ANY))
	client_sock.connect((device, near_devices[0]["port"]))
	return client_sock
'''

#Start the listener thread
def start_listener_thread(socket):
    
	t = threading.Thread(target=btlistener, args = (client_sock,))
	t.daemon = True
	t.start()

#please close the sockets after you're done
def close_sockets(sock1, sock2):
	sock2.close()
	sock1.close()
	print("Connection closed.")

def gen_input(rand):
	names = ["\'temp\':", "\'co2\':", "\'grav\':", "\'time\':"]
	#tmp = "{"
	tmp = ""

	if rand == True:
		for i in range(1, 100):
			tmp += "{"
			for j in  range(0, 3):
				tmp += names[j] + str(round(random.uniform(0, 30), 5)) +","
			tmp += names[3] + str(i)
			tmp += "}"
			if i != 99:
				tmp += "|"
	else:
		for i in range(1, 100):
			tmp += "{"
			for j in  range(0, 3):
				tmp += names[j] + str(j) + ","
			tmp += names[3] + str(i)
			tmp += "}"
			if i != 99:
				tmp += "|"
	#tmp += "}"
	return tmp
'''
	array = []
	for i in range(1, 100):
		array += (round(random.uniform(0, 30), 5), round(random.uniform(0, 30), 5), round(random.uniform(0, 30), 5), i)
	return json.dumps(array.__dict__)
'''


#print gen_input(False)



client_sock, server_sock = get_sockets()
start_listener_thread(client_sock)

if not stat.S_ISFIFO(os.stat(fifo_path).st_mode):
    os.mkfifo(fifo_path)
#Sender Daemon
try:
    while True:
	    #input loop
        #data = raw_input(">")
        #if len(data) == 0: break
	    #data += '\n' #concatenate a delimiter
        if state == 2:
            time.sleep(2)
            data = gen_input(True).split('|')[0]
            client_sock.send(data.encode('utf-8'))
except IOError:
    pass

close_sockets(client_sock, server_sock)

'''

	listener
		forever
			data = recv
			split data by semicolon
			if data[0] == Brewing
				Tell program to stop
			elseif data[0] == BrewData
				Send batch data[1]
			elseif data[0] == SurveyData
				Give data to AI
			elseif data[0] == PreBrew
				if SuggActReq
					Send AI's suggestion
				elseif Instruct Send
					Prepare to receive data
					Give data to AI and microcontroller
				
				
'''
