# Interfacing with brew.ai Hardware with a Teensy 2.0 and Raspberry Pi

brew.ai uses data from sensors to decide what the hardware should do. Currently, these
modules are working:

  - Temperature sensor
  - Water level sensor
  - Heating
  - Modulated stirring

### Receiving Data from Sensors
Sensor data will be sent in JSON packets to the learning agent, in this format:
```javascript
  "packets": {
    "packet": [
      {
        "temperature": " ",
        "waterLevel": " "
      }
    ]
  }
```
Temperature will be sent in units of degrees, Celsius. Water level will be a delta in centimeters
over the time of brewing.

### Controlling Stirring and Temperature
The command listener looks for a command and a value.
For instance, to set temperature to 60C, send this command:
` t 60 `

Here are the various commands:

| Implement     | Command  | Value                                  |
| ------------- | -------- | -------------------------------------- |
| Stirring      | `s`      | Speed from 0 (stopped) to 10 (full)    |
| Temperature   | `t`      | Desired temperature in °C              |
