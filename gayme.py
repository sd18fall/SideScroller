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
import random
import math


# ==============================================================================
#                                  Setup
# ==============================================================================
# arduinoSerialData = serial.Serial('com11',9600) #com11 can be changed to whatever port arduino is connected to

tock = 0        # timer by number of cycles
jumpDuration = 10 # must be even
increment = 5       # number of pixels to step when moving
screenx = 800    # game window width
screeny = 500    # game window height
size = (screenx,screeny)

pygame.init()
GameWindow = pygame.display.set_mode(size)

alive = True


# ==============================================================================
#                                  Classes
# ==============================================================================

class Model:
    """The game's model contains all the parts currently tracked as a part of the game.
    Attributes: size, player, blocks, enemies
    Methods: add_block, add_enemy, update, floorTest
    """
    def __init__(self, size, px=screenx*1/2, py=screeny*3/4):
        self.size = size
        self.player = Player(px, py)    # place a Player character
        self.blocks = []        # list of Block objects
        self.enemies = []       # list of Enemy objects

    def add_block(self,num_block, screen=GameWindow):
        """Add a randomly generated set of blocks anywhere onscreen"""
        for i in range(num_block):
            self.blocks.append(Block(random.randint(0,screenx),random.randint(0,screeny)))
        for i in self.blocks:
            i.appear(screen)

    def add_enemy(self,num_enemy, screen=GameWindow):
        for i in range(num_enemy):
            self.enemies.append(Enemy(random.randint(0,screenx),random.randint(0,screeny)))
        for i in self.enemies:
            i.appear(screen)

    def update(self):
        self.player.update(self.blocks)

    def appear(self):
        for block in self.blocks:
            block.appear()
        for enemy in self.enemies:
            enemy.appear()
        self.player.appear()

    def floorTest(self):
        """For testing purposes. Generates a floor block and some random blocks to the right."""
        self.blocks.append(Block(0, screeny*4/5, width=600, height=15, color=(255,255,0)))
        self.blocks.append(Block(random.randint(400,600),random.randint(350,425)))

class Character:
    '''
    Defines the basic features of a character in the game.
    Player and Enemy classes will inherit from this.

    Attributes: x, y, v (y-velocity), size, sprite
                jumpStart (a tock time), midJump (boolean)
    Methods: update, appear, rect, collision
    '''
    def __init__(self, x, y, v=0, size=25, sprite=None):
        self.x = x
        self.y = y
        self.v = v
        self.size = size
        self.sprite = sprite
        self.jumpStart = None # when did the jump start (in tocks)

    def update(self, blockSet):
        self.collision(blockSet)
        self.y = self.y + self.v

    def rect(self):
        """Makes a pygame Rect object for the character.
        Must be updated for any new x-y values, and called as charName.rect()"""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def appear(self, screen=GameWindow):
        #draw the sprite at x, y
        pygame.draw.rect(screen, (0,255,0), self.rect())

    def jump(self, tock):
        if self.jumpStart is None:
            # If we haven't started jumping already, make the current tock the start time.
            self.jumpStart = tock

        if tock - self.jumpStart > jumpDuration-2:
            # If we're over the jump duration since we started jumping, stop.
            self.jumpStart = None
        elif tock - self.jumpStart <= (jumpDuration-2)/2:
            # Rise for the first half of the jump
            self.v = -increment
        elif tock - self.jumpStart > (jumpDuration-2)/2:
            # Fall for the second half of the jump
            self.v = increment

    def collision(self, blockSet):
        """Detect characters colliding with blocks and bump them back appropriately"""
        floorFlag = False
        # Convert things into rect form and use pygame's collildelistall rect method
            # to find all collisions
        char = self.rect()
        blockRects = []
        blockList = [block.rect() for block in blockSet]

        indicies = char.collidelistall(blockRects)
        print(indicies)

        # For each block that we collided with, check which side of the character
            # is within the block's space.
            # Then, move character the opposite direction.
        for i in indicies:
            thisBlock = blockSet[i]

            # if self.y + self.size <= thisBlock.y + thisBlock.h and self.y - self.size >= thisBlock.y - thisBlock.h:
            if math.isclose((self.y+self.size), (thisBlock.y+(thisBlock.h)/2), abs_tol=(thisBlock.h)/2):
                self.y = thisBlock.y - self.size
                self.v = 0
                floorFlag = True
            # elif self.y <= thisBlock.y + thisBlock.h and self.y + self.size >= thisBlock.y + thisBlock.h:
            elif math.isclose(self.y, (thisBlock.y+(thisBlock.h)/2), abs_tol=(thisBlock.h)/2):
                self.y += 3*increment

            if not floorFlag and self.x + self.size >= thisBlock.x - thisBlock.w and self.x + self.size <= thisBlock.x + thisBlock.w:
                self.x -= 3*increment
                print('hit right')
            elif not floorFlag and self.x >= thisBlock.x - thisBlock.w and self.x <= thisBlock.x + thisBlock.w:
                self.x += 3*increment
                print('hit left')

        # If none of these collisions is a floor, and we're not currently jumping, fall.
        if not self.jumpStart == None and not floorFlag:
            self.v = increment

class Enemy(Character):
    """Class for enemy characters, inheriting from the general Character."""
    pass


class Player(Character):
    """Class for player, inheriting from general Character.
    New Attributes:
    New Methods: enemyEncounter
    """
    def enemyEncounter(self, enemySet):
        """tl;dr: If you're touching an enemy, die.
        Converts all characters into rectangles and uses pygame's colliderect
        rect method to find any collisions. In case of a collision, die() is called."""
        char = self.rect()
        for enemy in enemySet:
            if char.colliderect(enemy.rect()):
                die()

    def onScreen(self, screeny):
        if self.y > screeny:
            die()

    def update(self, blockSet, enemySet=[]):
        self.onScreen(screeny)
        self.collision(blockSet)
        self.enemyEncounter(enemySet)
        self.y = self.y + self.v

class Block:
    """Class for rectangular blocks for the characters to navigate.
    Attributes: x, y, w (width), h (height), color
    Methods: rect, appear
    """
    def __init__(self, x, y, width=20, height=50, color=(255,0,0)):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.color = color

    def rect(self):
        """Makes a pygame Rect object to display and test for collisions."""
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def appear(self, screen=GameWindow):
        pygame.draw.rect(screen, self.color, self.rect())


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
        for i in range(screenx):
            pygame.draw.line(self.screen,(i/8+40,i/20+20,i/7+70),(i,0),(i,700))

        self.model.appear()
        pygame.display.update()

class KeyboardController():
    """ Handles keyboard input to control the character """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event,tock):
        """ Up and down presses modify the y of the player """
        if event.type != pygame.locals.KEYDOWN:
            return
        if event.key == pygame.K_UP:
            self.model.player.jump(tock)
            #self.model.player.y-=5
            self.model.update
        if event.key == pygame.K_LEFT:
            self.model.player.x -= increment
            #self.model.player.y-=5
            self.model.update
        if event.key == pygame.K_RIGHT:
            self.model.player.x += increment
            #self.model.player.y-=5
            self.model.update



# ==============================================================================
#                                 Functions
# ==============================================================================

def update(tock):
    """Calls all the update and draw functions for one frame step"""
    model.update()
    view.draw()
    time.sleep(.001)
    #model.player.jump(tock)
    #model.player.x += increment

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



# ==============================================================================
#                                  Main
# ==============================================================================

model = Model(size)
view = View(model, GameWindow)
model.add_block(5, GameWindow)
model.floorTest()
controller = KeyboardController(model)

while alive:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            die()
        controller.handle_event(event,tock)

    update(tock)

    #if input("What do? ") == 'Die':
    #    die()

    tock += 1



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
    print('that testing sure did happen')

    pygame.quit()
