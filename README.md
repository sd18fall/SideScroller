# [Team_Name]
## A Game-like Thing by Anya and Liz

### How it works
The main program, gayme.py, uses python3 and pygame to generate a simple game world.  
The world includes your player, enemy characters, floors and blocks.
Navigate the world while dodging enemies and blockades to see how far you can go!

### Hardware Setup
You will need:
1 Arduino Uno, 1 Ultrasonic sensor, 4 male-to-female cables, and a USB to connect your Arduino to your laptop.

Setup the circuit with ground going to ground, VCC going to 5V, trig going to digital Pin 3, and echo going to digital pin 2.

### Prerequisites
Our game requires python3, pygame, and pySerial to run. We will go through the installation of these three libraries. You will also need the Arduino IDE to upload code to your arduino.

Download Arduino IDE here: https://www.arduino.cc/en/Main/Software
Download Anaconda here: http://docs.continuum.io/anaconda/install/

When asked to prepend the path to anaconda to your .bashrc file, respond yes.

Next download pygame using
'''pip install pygame'''

Last, install pySerial, which allows the script to read the Serial monitor of an Arduino using
'''pip install pyserial'''

### Installation
Once you have downloaded the prerequisites you are ready to install the game.

Do so by running
'''git clone https://github.com/sd18fall/final-project-team_name'''

Open Arduino IDE, and upload Sonar.ino to your Arduino. Check that everything works by opening the Serial monitor and ensuring that values are printed around 13000 with no hand over the sensor, and between 200 and 1000 with a hand over the sensor.

Open your computer's terminal and navigate to the folder.

Run '''python3 gayme.py'''

### Where it's headed
Currently, our game uses keyboard inputs to run. The game input will be eventually be analog, rather than keyboard-based. A setup of two IR sensors with an Arduino will give the user control over the magnitude of
their actions for a unique gaming experience.

### Why we're doing this
Mostly, we're here to learn, with a focus on using classes, premade libraries,
and planning a project. Inside of all that, we're looking to make a usable
and fun game. We hope you enjoy!

### Authors
Anya Jensen - [AnyaCakes](https://github.com/AnyaCakes)
Liz Leadley - [LizLeadley](https://github.com/LizLeadley)

### Attribution
Song: Daily Dosage by Rob Belfiore https://www.freesoundtrackmusic.com/
