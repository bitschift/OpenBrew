# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

import threading
import time
import src.hwctrl.datacollect as dc
import src.hwctrl.modulecontrol as mc
from bluetooth import *

fifo_path = "/tmp/btcomm.fifo"
state = 0
zero_time = time.time()

def get_time():
    '''
    Returns the time since inception
    '''
    return time.time() - zero_time

def fiforw(message=None):
    '''
    DEPRECATED
    '''
    if message is None:
        fifo = open(fifo_path, 'r')
        string = ""
        for line in fifo:
            string += line
        return string
    fifo = open(fifo_path, 'w')
    fifo.write(message)
    fifo.close()

def fifo_w(message=None):
    '''
    Handles writing to our fifo
    '''
    global fifo_path
    fifo = open(fifo_path, 'w')
    if message is not None:
        fifo.write(message)
    fifo.close()

def fifo_r():
    '''
    Handles reading from the fifo
    '''
    global fifo_path
    fifo = open(fifo_path, 'r')
    message = "".join(fifo.readlines())
    return message

def btlistener(socket):
    '''
    This is the function that the thread uses to listen on the bluetooth socket.
    The parameter is a socket.
    '''
    global state
    while True:
        try:
            data = socket.recv(1024)
            if data == "dataReq\n":
                print "Data start."
                client_sock.send("data_begin".encode("utf-8"))
                while True:
                    datapoint = gen_input()
                    print("Generated datapoint: ", datapoint)
                    client_sock.send((datapoint+"\n").encode("utf-8"))
                    print "After send"
                    client_sock.recv(1024)
                    if state == 2:
                        time.sleep(1)
                        print "slept"

                client_sock.send("data_end".encode("utf-8"))
                print "Data sent!"
            elif data == "start\n":
                fifo_w("start")
                print "Received start command."
                state = 2
                client_sock.send("S_ACK".encode("utf-8"))
            else:
                print "Recieved: " + str(data)
        except:
            return

def get_sockets():
    '''
    Setup socket information
    returns a tuple of sockets: (client socket, server socket)
    '''
    server_sock = BluetoothSocket(RFCOMM)
    server_sock.bind(("", PORT_ANY))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    
    #Advertise bluetooth service from controller
    advertise_service(
        server_sock, "cody-Lenovo-B590",
        service_id=uuid,
        service_classes=[uuid, SERIAL_PORT_CLASS],
        profiles=[SERIAL_PORT_PROFILE], 
        )
    
    # Wait for connections
    print "Waiting for connection on RFCOMM channel " + str(port)
    client_sock, client_info = server_sock.accept()
    print "Accepted connection from ", client_info
    return (client_sock, server_sock)

def start_listener_thread(socket):
    '''
    Start the listener thread
    '''
    thread = threading.Thread(target=btlistener, args=(socket,))
    thread.daemon = True
    thread.start()

def close_sockets(sock1, sock2):
    '''
    please close the sockets after you're done
    '''

    sock2.close()
    sock1.close()
    print "Connection closed."

def gen_input():
    '''
    CONSIDER RENAMING THIS FUNCTIOn
    Generates the input json for pushing data to the phone
    '''
    names = ["\'temp\':", "\'co2\':", "\'grav\':", "\'time\':"]
    name_f = [dc.read_temp, dc.read_co2, lambda: 0, get_time]
    result = [name + str(name_f[index]()) for index, name in enumerate(names)]
    result = ",".join(result)
    result = "{" + result + "}"
    print "Final result: ", result
    return result


if __name__ == '__main__':
    client_sock, server_sock = get_sockets()
    start_listener_thread(client_sock)

    #Sender Daemon
    try:
        while True:
            #input loop
            data = raw_input(">")
            if len(data) == 0:
                break
    except IOError:
        pass

    close_sockets(client_sock, server_sock)
