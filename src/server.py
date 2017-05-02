import threading
import time
import hwctrl.datacollect as dc
import bluetooth as bt
import json

class BTServer:
    '''
    BTServer creates our communication server and maintains connections
    between the Pi and the phone app.
    It maintains state information about the communication status
    (ie, are we sending data for graphing, recieving information for learning)
    and relays messages through the fifo to the brew.py script.
    '''
    def __init__(self):
        self.fifo_path = "/tmp/btcomm.fifo"
        self.state = 0
        self.zero_time = time.time()
        self.client_sock, self.server_sock = self.get_sockets()

    def start(self):
        '''
        A unified interface to start the necessary server components
        '''
        self.start_listener_thread(self.client_sock)

    def shutdown(self):
        '''
        A unified interfce to cleanly stop the necessary server componenets
        '''
        self.close_sockets(self.client_sock, self.server_sock)


    def get_time(self):
        '''
        Returns the time since inception
        '''
        return time.time() - self.zero_time

    def fifo_w(self, message=None):
        '''
        Handles writing to our fifo
        '''
        fifo = open(self.fifo_path, 'w')
        if message is not None:
            fifo.write(message)
        fifo.close()

    def fifo_r(self):
        '''
        Handles reading from the fifo
        '''
        fifo = open(self.fifo_path, 'r')
        message = "".join(fifo.readlines())
        fifo.close()
        return message

    def btlistener(self, socket):
        '''
        This is the function that the thread uses to listen on the bluetooth socket.
        The parameter is a socket.
        '''
        while True:
            try:
                received_data = socket.recv(1024)
                received_data.strip("\n")
                received_data = json.loads(received_data)
                if received_data == "dataReq":
                    print "Data start."
                    self.client_sock.send("data_begin".encode("utf-8"))
                    while True:
                        datapoint = self.gen_data()
                        print("Generated datapoint: ", datapoint)
                        self.client_sock.send((datapoint+"\n").encode("utf-8"))
                        print "After send"
                        self.client_sock.recv(1024)
                        if self.state == 2:
                            time.sleep(1)
                            print "slept"

                    self.client_sock.send("data_end".encode("utf-8"))
                    print "Data sent!"

                elif "start" in received_data:
                    self.fifo_w(received_data)
                    print "Received start command."
                    self.state = 2
                    self.client_sock.send("S_ACK".encode("utf-8"))
                elif type(received_data) == dict:
                    if 'survey_value' in received_data.keys():
                        self.fifo_w("reward"+str(received_data['survey_value']))
                else:
                    print "[ERROR] Recieved: " + str(received_data)
            except:
                return

    def get_sockets(self):
        '''
        Setup socket information
        returns a tuple of sockets: (client socket, server socket)
        '''
        self.server_sock = bt.BluetoothSocket(bt.RFCOMM)
        self.server_sock.bind(("", bt.PORT_ANY))
        self.server_sock.listen(1)
        port = self.server_sock.getsockname()[1]
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        #Advertise bluetooth service from controller
        bt.advertise_service(
            self.server_sock, "cody-Lenovo-B590",
            service_id=uuid,
            service_classes=[uuid, bt.SERIAL_PORT_CLASS],
            profiles=[bt.SERIAL_PORT_PROFILE],
            )
        # Wait for connections
        print "Waiting for connection on RFCOMM channel " + str(port)
        self.client_sock, client_info = self.server_sock.accept()
        print "Accepted connection from ", client_info
        return (self.client_sock, self.server_sock)

    def start_listener_thread(self, socket):
        '''
        Start the listener thread
        '''
        thread = threading.Thread(target=self.btlistener, args=(socket,))
        thread.daemon = True
        thread.start()

    def close_sockets(self, sock1, sock2):
        '''
        please close the sockets after you're done
        '''

        sock2.close()
        sock1.close()
        print "Connection closed."

    def gen_data(self):
        '''
        CONSIDER RENAMING THIS FUNCTIOn
        Generates the input json for pushing data to the phone
        '''
        names = ["\'temp\':", "\'co2\':", "\'grav\':", "\'time\':"]
        name_f = [dc.read_temp, dc.read_co2, lambda: 0, self.get_time]
        result = [name + str(name_f[index]()) for index, name in enumerate(names)]
        result = ",".join(result)
        result = "{" + result + "}"
        print "Final result: ", result
        return result


if __name__ == '__main__':
    server = BTServer()
    server.start()
    try:
        while True:
            #input loop
            data = raw_input(">")
            if len(data) == 0:
                break
    except IOError:
        pass
    server.shutdown()
