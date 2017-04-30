# Interface
This is the code for the interface for Brew.AI. This is an Android app compatible with Android API level 23+.
Here are some screenshots of the app.

![main](http://i.imgur.com/X0Y3qCug.png) ![prebrew](http://i.imgur.com/TIELruL.png) ![survey](http://i.imgur.com/FNvLpOn.png)

Raspberry Pi Package Requirements:

|Package Name|
|:----:|
| `bluez`|
| `pybluez` (pip install)|


There are 4 things that need to be set up for this part to work:

* Pairing the phone and the raspberry pi
* The Anroid app
* The `server.py` script (This is a testing script. The actual script is in `brew.ai/src`)
* the fifo listener (This is for testing by itself. The brewing script in the `brew.ai/src` has a fifo listener inside it.)

### Pairing (Android)
First open `/etc/bluetooth/main.conf` and on the line that says `DisablePlugins = ` add `pnat`.

After that, run the command ```sudo invoke–rc.d bluetooth restart```.

Once that is finished, the devices need to be paired. To pair the two devices you must run ```bash sudo hciconfig hci piscan ```. This will make the pi visible and available to be paired with.

### Python scripts (Pi)
Before you run any of the python scripts, run this command ```mkfifo /tmp/btcomm.fifo```. This will create the fifo that the two scripts use to communicate.

After they are paired and the fifo is created, run `server.py` (with sudo) and `test.py`.



### Android App
To connect the Android to the pi, press the `connect` button. Then to start the brewing process, press start.
You will be taken to a page so that you can customize your batch. After you submit your alterations, the brewing will start.
After the `server.py` script is done generating data, you will be taken to a survey activity where you can give feedback to the device.
This is only for testing purposes. All the data is randomly generated. The real script gathers data from the sensors.
