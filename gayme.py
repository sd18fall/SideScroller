"""This is a game. It will have cool input.
It was made by Anya and Liz."""

# ==============================================================================
#                                  Libraries
# ==============================================================================
import pygame
from pygame.locals import *
#used to connect to arduino
import serial #must install pySerial using 'pip install pyserial'

# ==============================================================================
#                                  Classes
# ==============================================================================
'''
class Model:
    def __init__(self, size):
        self.size = size
        self.player = Player()
        self.enemy = Enemy()
'''

class Character:
    '''
    Defines the basic features of a character in the game
    Attributes: x, y, size, sprite
    Methods: jump, shoot, appear
    '''
    def __init__(self, x, y, sprite=None, size=25):
        self.x = x
        self.y = y
        self.size = size
        self.sprite = sprite
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def appear(self, screen):
        #draw the sprite at x, y
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(screen, (0,255,0), self.rect)

    def up(self):
        self.y -=1

    def down(self):
        self.y+=1




class Enemy(Character):
    '''
    Defines the enemies in the pygame
    Plan on using
    '''
    pass


class Player(Character):
    pass


class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    def appear(self, screen):
        #draw the sprite at x, y
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, (255,0,0), self.rect)

    def collision(self):
        pass




# ==============================================================================
#                                  Setup
# ==============================================================================
# arduinoSerialData = serial.Serial('com11',9600) #com11 can be changed to whatever port arduino is connected to


# ==============================================================================
#                                 Functions
# ==============================================================================
#defines what happens in event of collisions
#calls your classes and pictures and stuff
#appropriately moves things

def update():
    # if not collision(below) or char.up:
    #     cahr.doqn

    #if spacebar
    #    char.up

    #if char hitting Enemy
    #   die
    pygame.display.update()
    pass

def calibrate():
    """Calibrate the IR sensors"""
    print("Please hold your hands at your comfortable lower limit")
    # Do arduino magic
    print("Please hold your hands at your comfortable upper limit")
    # Do arduino magic
    print("Please remove your hands from the sensors")
    # Do arduino magic

def die():
    print("Game over, loser")
    pygame.quit()
    global alive
    alive = False

# ==============================================================================
#                                  Main
# ==============================================================================
pygame.init()
alive = True

# TODO:
# make an empty window
# Add a floor
# Add a wall
# place your character in the middle
# Move the character

screenx = 800
screeny = 500

jon = Character(screenx/2, screeny*2/3)
wallE = Block(450,200,5,50)
floorE = Block(200,150,75,10)
pygame.display.set_mode((screenx, screeny))


while alive:

    GameWindow = pygame.display.set_mode((screenx, screeny))
    jon.appear(GameWindow)
    wallE.appear(GameWindow)
    floorE.appear(GameWindow)

    update()
    if input("What do? ") == 'Die':
        die()
    jon.x += 10
    jon.y -= 10


# ==============================================================================
#                                 Testing
# ==============================================================================
if __name__ != "__main__":
    pygame.init()


    '''
    #reads serial output of arduino
    while (1==1):
        if (arduinoSerialData.inWaiting()>0):
            myData = arduinoSerialData.readline()
            print myData
    '''
    print('that sure did happen')

    pygame.quit()
