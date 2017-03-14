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
import time
import hwctrl.datacollect as dc
import hwctrl.modulecontrol as mc

fifo_path = "/tmp/btcomm.fifo"
state = 0

zero_time = time.time()
def get_time():
    '''
    '''
    
    return time.time() - zero_time

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
    while True:
        try:
            data = socket.recv(1024)
            if data == "dataReq\n":
                print("Data start.")
                client_sock.send("data_begin".encode("utf-8"))
                while(True):
                    datapoint = gen_input()
                    print("Generated datapoint: ", datapoint)
                    client_sock.send((datapoint+"\n").encode("utf-8"))
                    print("After send")
                    client_sock.recv(1024)
                    if state == 2:
                        time.sleep(1)
                        print("slept")

                client_sock.send("data_end".encode("utf-8"))
                print( "Data sent!")
            elif data == "start\n":
                fiforw("start")
                print("Received start command.")
                state = 2
                client_sock.send("S_ACK".encode("utf-8"))
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

def gen_input():
    names = ["\'temp\':", "\'co2\':", "\'grav\':", "\'time\':"]
    name_f= [dc.read_temp, dc.read_co2, lambda: 0, get_time]
    result = [name + str(name_f[index]()) for index, name in enumerate(names)]
    result = ",".join(result)
    result = "{" + result + "}"
    print "Final result: ", result
    return result


client_sock, server_sock = get_sockets()
start_listener_thread(client_sock)

#if not stat.S_ISFIFO(os.stat(fifo_path).st_mode):
#    os.mkfifo(fifo_path)
#Sender Daemon
try:
    while True:
        #input loop
        data = raw_input(">")
        if len(data) == 0: break
        #data += '\n' #concatenate a delimiter
#        if state == 2:
#            time.sleep(2)
#            data = gen_input(True).split('|')[0]
#            client_sock.send(data.encode('utf-8'))
except IOError:
    pass

close_sockets(client_sock, server_sock)
