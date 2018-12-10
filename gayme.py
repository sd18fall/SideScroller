'''This is a game made by team [Team_Name], made up of Anya and Liz.
The game itself is a side-scroller, with intended inputs of IR sensors.'''

# ==============================================================================
#                                  Libraries
# ==============================================================================
import pygame
import time
from pygame.locals import *
#used to connect to arduino
# import serial #must install pySerial using 'pip install pyserial'

import math
from model import Model
from view import View
import pdb


# ==============================================================================
#                                  Setup
# ==============================================================================

tock = 0          # timer by number of cycles
increment = 8     # number of pixels to step when moving
screenx = 800     # game window width
screeny = 500     # game window height
size = (screenx,screeny)
alive = False

pygame.init()
GameWindow = pygame.display.set_mode(size)


playlist = list()
playlist.append ( "daily_dosage-rob_belfiore.mp3" )
pygame.mixer.music.load ( playlist.pop() )
pygame.mixer.music.play(-1)

# ==============================================================================
#                                  Classes
# ==============================================================================

# In Other Files

# ==============================================================================
#                                 Functions
# ==============================================================================
def title():
    '''Show the title screen'''
    print (alive)
    model.drawTitle(GameWindow)
    model.checkSwipe()
    pygame.display.update()
    if model.start == True:
        start()


def start():
    '''Initializes all the beginning pieces of the game'''
    global alive
    alive = True
    model.add_background(GameWindow, True)
    model.add_block(10, GameWindow, False, True)
    model.add_block(10, GameWindow)
    model.add_enemy(5, GameWindow)
    model.add_block(1, GameWindow, True)

def update(tock):
    '''Calls all the update and draw functions for one frame step'''
    counter = 0
    #print('***ba-', end="\n")
    model.update(tock, GameWindow, increment)
    #print('***bam', end="\n")
    model.add_block(1,GameWindow, True)
    model.add_enemy(1,GameWindow, True)
    model.add_background(GameWindow)
    view.draw(screenx)
    time.sleep(.01)
    if model.endGame:
        time.sleep(5)
        die()


def die():
    '''Ends the game by False-ing the while loop variable'''
    print("You died! Play again.")
    pygame.quit()
    global alive
    alive = False



# ==============================================================================
#                                  Main
# ==============================================================================
GameWindow = pygame.display.set_mode(size)
model = Model(size)
view = View(model, GameWindow)
#model.sonar.reset()
while alive == False:
    title()

while alive:
    update(tock)
    pygame.event.pump()
    tock += 1




# ==============================================================================
#                                 Testing
# ==============================================================================
if __name__ != "__main__":

    # pygame.init()

    for i in range(20):
        update(tock)
        pygame.event.pump()
        tock += 1

    # #model.player.vx = increment
    # update(tock)
    # tock += 1
    # # model.player.jump(tock)
    #
    # #for tock in range(1, 1000):
    # #    update(tock)
    # #    tock += 1



    print('that testing sure did happen')
