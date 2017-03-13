There are 4 things that need to be set up for this part to work:
  Pairing the phone and the raspberry pi
  The Anroid app
  The server script
  the fifo listener

#Pairing (Android)
To pair the two devices you must run ```bash sudo hciconfig hci piscan ```. This will make the pi visible and available to be paired with.

#Python scripts (Pi)
After they are paired, run the server script (with sudo if needed) and the fifo listener.
After running these two things, start the android app.

#Android App
To connect the Android to the pi, press the open button. Then to start the brewing process, press start.

  The Python app behind this on the pi just generates a random set of data and sends a point out every 1 second.
