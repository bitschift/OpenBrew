import os
import sys

path = "/tmp/btcomm.fifo"
#os.mkfifo(path)
fifo = open(path, 'r')
while 1:
    for line in fifo:
        print line + ","
    fifo = open(path, 'r')
fifo.close()
