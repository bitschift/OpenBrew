[![Stories in Ready](https://badge.waffle.io/bitschift/OpenBrew.png?label=ready&title=Ready)](https://waffle.io/bitschift/OpenBrew)
# brew.ai
brew.ai is the automated, autonomous brewing device to bring the power of machine learning into the hands of the ametur brewer, allowing the creation of new recipies tailored to the brewers taste.
This is accomplished by using general reinforcemtnt learning (Q-Learning) powered from the users feedback of each brew.
This feedback is gleaned via an Android app, and sent back to the controlling software.

## Setup and Installation
### Hardware

### Software
##### Depependencies
###### Raspberry Pi
- Keras

which requires

- SciPy
- Numpy
Build and installation instructions for Raspbian can be found [here](https://github.com/bitschift/brew.ai/tree/connor/READMEs/src/ai#keras-with-theano-on-raspberry-pi-b).

#### Rasberry Pi
The reposityory can be cloned onto a Raspberry Pi with the properly connected hardware, and run with [`src/launch.sh`](https://github.com/bitschift/brew.ai/blob/master/src/brew.py)
At this point, the software on the Pi will be waiting for confirmation from the Android app, and runs without further intervention.

#### Android
