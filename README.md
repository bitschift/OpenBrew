[![Stories in Ready](https://badge.waffle.io/bitschift/OpenBrew.png?label=ready&title=Ready)](https://waffle.io/bitschift/OpenBrew)
# brew.ai
brew.ai is the automated, autonomous brewing device to bring the power of machine learning into the hands of the ametur brewer, allowing the creation of new recipies tailored to the brewers taste.
This is accomplished by using general reinforcemtnt learning (Q-Learning) powered from the users feedback of each brew.
This feedback is gleaned via an Android app, and sent back to the controlling software.

## Setup and Installation
### Hardware
brew.ai must be run on built brewing hardware, which at a minimum must include a Raspberry Pi, temperature and fermentation sensing modules, and heat and stir control modules. Without these components, the software will not work correctly. Instructions to interface the hardware with Raspberry Pi software can be found [here](https://github.com/bitschift/brew.ai/tree/master/src/hwctrl).

Alternatively to the Raspberry Pi, there is support for controlling the hardware on a Teensy, however this functionality is deprecated.

### Software
##### Depependencies
###### Raspberry Pi
- Bluez
- PyBluez
- Keras

which requires

- SciPy
- Numpy
Build and installation instructions for Raspbian can be found [here](https://github.com/bitschift/brew.ai/tree/master/src/ai#keras-with-theano-on-raspberry-pi-b).

#### Rasberry Pi
The reposityory can be cloned onto a Raspberry Pi with the properly connected hardware, and run with [`src/launch.sh`](https://github.com/bitschift/brew.ai/blob/master/src/launch.sh)
At this point, the software on the Pi will be waiting for confirmation from the Android app, and runs without further intervention.

#### Android

This app requires Android API version 23+. It connects with the Raspberry Pi via Bluetooth.
Before you can connect the app to the Pi, you will need to pair the two devices.
Once all the previous steps have been followed, you should be able to push start and it will brew a batch of mead!
