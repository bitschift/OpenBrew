# Interfacing with brew.ai Hardware with just a Raspberry Pi

brew.ai uses data from sensors to decide what the hardware should do. Currently, these
modules are working:

  - Temperature sensor
  - Water level sensor
  - Heating
  - Modulated stirring

### Running brew.ai from a Raspberry Pi
Once all hardware components are connected, the 'brew.py' script will begin the brewing process. 

### Receiving Data from Sensors
Sensor data will be stored in an SQLite db on the Pi, in this table:
```SQL
  CREATE TABLE data
( id int NOT NULL,
  temp int,
  waterlevel int,
  time TIMESTAMP CURRENT_TIMESTAMP,
  CONSTRAINT data_pk PRIMARY KEY (id)
);
```
Temperature will be stored in units of degrees, Celsius. Water level will be a delta in centimeters
over the time of brewing.

To collect data, the datacollect.py service must be instantiated in the background, and will store sensor
readings in the db every 10 minutes.

### Controlling Stirring and Temperature
The command listener in `modulecontrol.py` looks for a command and a value.
For instance, to set temperature to 60C from the shell, run this command:
`sudo python modulecontrol.py t 60 `

Here are the various commands:

| Implement     | Command  | Value                                  |
| ------------- | -------- | -------------------------------------- |
| Stirring      | `s`      | Speed from 0 (stopped) to 100 (full)   |
| Temperature   | `t`      | Desired temperature in °C              |
