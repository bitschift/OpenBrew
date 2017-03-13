import os
import sys

path = "/tmp/btcomm.fifo"
#os.mkfifo(path)
while True:
	for line in open(path, "r"):
		print line
