"""This is a game made by team [Team_Name], made up of Anya and Liz.
The game itself is a side-scroller, with intended inputs of IR sensors."""

# ==============================================================================
#                                  Libraries
# ==============================================================================
import pygame
import time
from pygame.locals import *
#used to connect to arduino
import serial #must install pySerial using 'pip install pyserial'

import math
from model import Model
from view import View
from calibrate_sonar import SonarController
import pdb


# ==============================================================================
#                                  Setup
# ==============================================================================

tock = 0        # timer by number of cycles
jumpDuration = 16 # must be even
increment = 8       # number of pixels to step when moving
screenx = 800    # game window width
screeny = 500    # game window height
size = (screenx,screeny)

pygame.init()
GameWindow = pygame.display.set_mode(size)

alive = True


# ==============================================================================
#                                  Classes
# ==============================================================================

# In Other Files

# ==============================================================================
#                                 Functions
# ==============================================================================

def update(tock):
    """Calls all the update and draw functions for one frame step"""
    counter = 0
    model.update(tock, GameWindow)
    model.add_block(1,GameWindow, True)
    model.add_enemy(1,GameWindow, True)
    model.add_background(GameWindow)
    view.draw(screenx)
    time.sleep(.01)

def die():
    """Ends the game by False-ing the while loop variable"""
    print("You died! Play again.")
    pygame.quit()
    global alive
    alive = False



# ==============================================================================
#                                  Main
# ==============================================================================

model = Model(size)
# Initialize arduino for sonar
arduinoSerialData = serial.Serial(model.sonar.port, 9600)
view = View(model, GameWindow)
model.add_background(GameWindow, True)
model.add_block(10, GameWindow)
model.add_enemy(5, GameWindow)
model.add_block(1, GameWindow, True)
#model.floorTest()

while not alive:

    update(tock)

    tock += 1



# ==============================================================================
#                                 Testing
# ==============================================================================
if __name__ == "__main__":

    pygame.init()


    model.player.vx = 3*increment
    update(tock)
    tock += 1
    model.player.jump(tock)

    for tock in range(1, 1000):
        update(tock)
        tock += 1

        sonarH = sonar.data()
        print(sonarH)
        # if (arduinoSerialData.inWaiting()>0):
        #         myData = arduinoSerialData.readline()
        #         print( myData)


    print('that testing sure did happen')
