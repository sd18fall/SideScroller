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
import pdb


# ==============================================================================
#                                  Setup
# ==============================================================================
arduinoSerialData = serial.Serial('com21',9600) #com11 can be changed to whatever port arduino is connected to

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



class View():
    def __init__(self, model, screenincrementGameWindow):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height) """
        self.model = model
        self.screen = GameWindow

    def draw(self):
        """ Draw the current game state to the screen """
        # draw a gradient background
        if self.model.endgame == False:
            for i in range(screenx):
                pygame.draw.line(self.screen,(i/8+40,i/20+20,i/7+70),(i,0),(i,700))

            self.model.appear(self.screen)
        if self.model.endgame == True:
            for i in range(screenx):
                    pygame.draw.line(self.screen,(i/8+40,0,0),(i,0),(i,700))
        pygame.display.update()






# ==============================================================================
#                                 Functions
# ==============================================================================

def update(tock):
    """Calls all the update and draw functions for one frame step"""
    counter = 0
    model.update(tock, GameWindow)
    model.add_block(1,GameWindow, True)
    model.add_enemy(1,GameWindow, True)
    view.draw()
    time.sleep(.01)


def calibrate():
    """Function to guide the user to calibrate the sensors.
    Incomplete; requires arduino magic at thsi time."""
    print("Please hold your hands at your comfortable lower limit")
    # Do arduino magic
    print("Please hold your hands at your comfortable upper limit")
    # Do arduino magic
    print("Please remove your hands from the sensors")
    # Do arduino magic

def die():
    """Ends the game by False-ing the while loop variable"""
    print("You died! Play again.")
    pygame.quit()
    global alive
    alive = False
    # while 1:
    #     pass



# ==============================================================================
#                                  Main
# ==============================================================================

model = Model(size)
view = View(model, GameWindow)
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
            #reads serial output of arduino

        if (arduinoSerialData.inWaiting()>0):
                myData = arduinoSerialData.readline()
                print( myData)






    print('that testing sure did happen')
