#AI Software
The AI implemented here is a general Q-learning agent, implemented with a neural network to approximate the traditional Q-table. The traditional Q-table is strictly bound in dimension and requires a finite number of states in the system. The state consists of continuous measurements like temperature or CO2 levels. This requires a neural network be used to avoid an infinite size table for Q-learning. Otherwise, the Q-learning process proceeds like normal. The state-action-reward history is utilized by the Bellman update function, which is used to calculate the target weights for the neural network, which is trained through standard back propagation.

This is implemented in the learning agent in `qlearning.py`. A basic simulator was contrusted to test the rough learning ability of the agent to identify any major bugs, which is written in `simulator.py` and `simple_training.py`.

# Keras with Theano on Raspberry Pi B+
With [PR #3266](https://github.com/Theano/Theano/pull/3266/files), Theano made its compilation process compatible for different ARM architectures, including the Raspberry Pi. This makes it possible to install and setup Keras with the Theano backend with only a few hours of work.
This guide was made possible by the following blog posts:

[http://wyolum.com/numpyscipymatplotlib-on-raspberry-pi/](http://wyolum.com/numpyscipymatplotlib-on-raspberry-pi/)

[http://www.pyimagesearch.com/2016/07/18/installing-keras-for-deep-learning/](http://www.pyimagesearch.com/2016/07/18/installing-keras-for-deep-learning/)

Together, they had enough information to create a full list of instructions for installing Keras and Theano on the Raspberry Pi.

## Instructions
First satisfy the runtime and buildtime dependeicies:
### Numpy
```bash
sudo apt-get install python-numpy
```
### Scipy
```bash
sudo apt-get install libblas-dev
sudo apt-get install liblapack-dev
sudo apt-get install python-dev        # Possibly already installed
sudo apt-get install libatlas-base-dev # Optional, for faster execution
sudo apt-get install gfortran
sudo apt-get install python-setuptools # Possibly already installed
sudo easy_install scipy
```
The last step is synonmous with installing scipy through `pip`, and can be done with that method.
Either way, installing scipy will take **several hours**.

### Theano
First, we have a few more dependencies to get
```bash
sudo pip install scikit-learn
sudo pip install pillow
sudo pip install h5py
```
With these dependencies met, we can install a stable Theano release from the git source
```bash
sudo pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git
```
### Keras
The installation can occur with the command:
```bash
sudo pip install keras
```
After Keras is installed, you will want to edit the Keras configuration file `~/.keras/keras.json` to use Theano instead of the default TensorFlow backend.
This requires changing two lines. The first change is: 
```json
"image_dim_ordering": "tf"  --> "image_dim_ordering": "th"
```
and the second:
```json
"backend": "tensorflow" --> "backend": "theano"
```

(The final file should look like the example below)
```json
{
    "image_dim_ordering": "th", 
    "epsilon": 1e-07, 
    "floatx": "float32", 
    "backend": "theano"
}
```

# Testing
Now, pull up an interactive Python terminal and attempt to ```import Keras```. This will take a minute, but no errors should occur with a full installation of the packages listed above.
