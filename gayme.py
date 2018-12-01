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

import pdb


# ==============================================================================
#                                  Setup
# ==============================================================================
# arduinoSerialData = serial.Serial('com11',9600) #com11 can be changed to whatever port arduino is connected to

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

    def add_block(self,num_block, screen=GameWindow, end_block = False):
        """Add a randomly generated set of blocks anywhere onscreen"""
        counter = 0
        if end_block == True:
            for block in self.blocks:
                if block.x > 650:
                    counter +=1
            if counter < 1:
                self.blocks.append(Block((800), random.randint(0,screeny)))
        if end_block == False:
            for i in range(num_block):
                    self.blocks.append(Block(800/num_block*i,random.randint(0,screeny)))

        for i in self.blocks:
            i.appear(screen)

    def add_enemy(self,num_enemy, screen=GameWindow, endemy = False, spawn = random.randint(0,5)):
        counter = 0
        if endemy == True and spawn ==3:
            for enemy in self.enemies:
                if enemy.x > 650:
                    counter +=1
            if counter < 1:
                self.enemies.append(Enemy((800), random.randint(0,screeny)))
        if endemy == False:
            for i in range(num_enemy):
                    self.enemies.append(Enemy(random.randint(0,screenx),random.randint(0,screeny)))

        for i in self.enemies:
            i.appear(screen)

    def update(self, tock):
        self.player.update(self.blocks, self.enemies, tock)
        for block in self.blocks:
            block.update()
        for enemy in self.enemies:
            enemy.update(self.blocks, tock)
            enemy.shoot(self.player)

    def appear(self):
        for block in self.blocks:
            block.appear()
        for enemy in self.enemies:
            enemy.appear()
        self.player.appear()

    def floorTest(self):
        """For testing purposes. Generates a floor block and some random blocks to the right."""
        self.blocks.append(Block(0, screeny*4/5, width=600, height=25, color=(255,255,0)))
        self.blocks.append(Block(random.randint(400,600),random.randint(350,425)))

class Character:
    '''
    Defines the basic features of a character in the game.
    Player and Enemy classes will inherit from this.

    Attributes: x, y, v (y-velocity), size, sprite
                jumpStart (a tock time), midJump (boolean)
    Methods: update, appear, rect, collision
    '''
    def __init__(self, x, y, vx = 0, vy = 0, size = 25, sprite = None, ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.sprite = sprite
        self.jumpStart = None # when did the jump start (in tocks)

    def update(self, blockSet, tock):
        self.collision(blockSet)
        if self.jumpStart != None:
            self.jump(tock)
        self.y = self.y + self.vy
        self.x = self.x + self.vx
        self.x-=increment


    def rect(self):
        """Makes a pygame Rect object for the character.
        Must be updated for any new x-y values, and called as charName.rect()"""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def jump(self, tock):
        if self.jumpStart is None:
            # If we haven't started jumping already, make the current tock the start time.
            self.jumpStart = tock

        # if tock - self.jumpStart > jumpDuration-2:
        #     # If we're over the jump duration since we started jumping, stop.
        #     self.jumpStart = None
        if tock - self.jumpStart < (jumpDuration)/2:
            # Rise for the first half of the jump
            self.vy = -(2*increment)
        else:
            # If we're not rising, stop 'jumping'. Falling is taken care of elsewhere.
            self.jumpStart = None
            self.vy = 0
        # elif tock - self.jumpStart > (jumpDuration-2)/2:
        #     # Fall for the second half of the jump
        #     self.vy = increment

    def collision(self, blockSet):
        """Detect characters colliding with blocks and bump them back appropriately"""
        floorFlag = False
        # Convert things into rect form and use pygame's collildelistall rect method
            # to find all collisions
        char = self.rect()
        blockRects = [block.rect() for block in blockSet]

        indicies = char.collidelistall(blockRects)

        # For each block that we collided with, check which side of the character
            # is within the block's space.
            # Then, move character the opposite direction.
        for i in indicies:
            thisBlock = blockRects[i]
            if thisBlock.left <= char.right and char.right <= thisBlock.right\
                and char.right <= thisBlock.centerx:
                print('hit right')
                self.x = thisBlock.left - self.size
                self.vx = 0
            if thisBlock.left <= char.left and char.left <= thisBlock.left\
                and char.left >= thisBlock.centerx:
                print('hit left')
                self.x = thisBlock.right
                self.vx = 0
            if thisBlock.bottom >= char.top and char.top >= thisBlock.top\
                and char.top >= thisBlock.centery:
                print('hit top')
                self.jumpStart = None
                self.y = thisBlock.bottom
                self.vy += increment
            if thisBlock.bottom >= char.bottom and char.bottom >= thisBlock.top\
                and char.bottom <= thisBlock.centery:
                print('hit floor')
                self.y = thisBlock.top - self.size +1
                self.vy = 0
                floorFlag = True
                self.jumpStart = None

        # If none of these collisions is a floor, and we're not currently jumping, fall.
        if self.jumpStart == None and not floorFlag:
            print('fall')
            self.vy = increment
        elif self.jumpStart != None:
            print('free jump')

class Enemy(Character):
    """Class for enemy characters, inheriting from the general Character."""
    def appear(self, screen=GameWindow):
        #draw the sprite at x, y
        pygame.draw.rect(screen, (255,0,0), self.rect())
    def shoot(self,  player, difficulty = 1):
        self.projectile = Projectile(self.x,self.y)
        self.projectile.appear(GameWindow)
        self.projectile.update()
        if difficulty == 1:
            pass
        elif difficulty ==2:
            self.projectile.go('left')
        elif difficulty ==3:
            self.projectile.aimed_shot(player, self)


class Projectile(Enemy):
    '''Class for projectiles that enemies shoot'''
    def appear(self, GameWindow):
        pygame.draw.ellipse(GameWindow, (255,0,0), self.rect())

    def go(self, direction):
        if direction == 'left':
            self.vx = -1
            self.vy = 0
        elif direction == 'right':
            self.vx = 1
            self.vy = 0
        elif direction == 'down':
            self.vy = 1
            self.vx = 0
        else:
            self.vy = -1
            self.vx = 0

    def aimed_shot(self,player,enemy):
        x_dist = player.x-enemy.x
        y_dist = player.y - enemy.y
        self.vx=x_dist/100
        self.vy=y_dist/100

    def update(self):
        self.x+=self.vx
        self.y+=self.vy

    def vanish(self):
        #Temporary hiding code
        # TODO: this.
        self.x = screenx+10
        self.y = screeny+10
        self.vx = 0
        self.vy = 0

    def collision(self, blockSet):
        """
        Converts all walls into rectangles and uses pygame's colliderect
        rect method to find any collisions. In case of a collision, vanish is called."""
        char = self.rect()
        for block in blockSet:
            if char.colliderect(block.rect()):
                self.vanish()

class Player(Character):
    """Class for player, inheriting from general Character.
    New Attributes:
    New Methods: enemyEncounter
    """
    def appear(self, screen=GameWindow):
        #draw the sprite at x, y
        pygame.draw.rect(screen, (0,255,0), self.rect())

    def enemyEncounter(self, enemySet):
        """tl;dr: If you're touching an enemy, die.
        Converts all characters into rectangles and uses pygame's colliderect
        rect method to find any collisions. In case of a collision, die() is called."""
        char = self.rect()
        for enemy in enemySet:
            if char.colliderect(enemy.rect()):
                die()

    def onScreen(self, screenx, screeny):
        if self.y > screeny or self.y < 0 or self.x < 0:
            # If you go offscreen up, down, or left, die.
            die()

    def update(self, blockSet, enemySet, tock):
        self.onScreen(screenx, screeny)
        if self.jumpStart != None:
            self.jump(tock)
        self.y = self.y + self.vy
        #self.x = self.x + self.vx
        self.enemyEncounter(enemySet)
        self.collision(blockSet)



class Block():
    """Class for rectangular blocks for the characters to navigate.
    Attributes: x, y, w (width), h (height), color
    Methods: rect, appear
    """
    def __init__(self, x, y, width=150, height=20, color=(0,0,150)):
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

    def update(self):
        self.x-=increment

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
        while event.key == pygame.K_UP:
            self.model.player.jump(tock)
            self.model.update(tock)
        while event.key == pygame.K_LEFT:
            self.model.player.vx = -increment
            self.model.update(tock)
        while event.key == pygame.K_RIGHT:
            self.model.player.vx = increment
            self.model.update(tock)



# ==============================================================================
#                                 Functions
# ==============================================================================

def update(tock):
    """Calls all the update and draw functions for one frame step"""
    counter = 0
    model.update(tock)
    model.add_block(1,GameWindow, True)
    model.add_enemy(1,GameWindow, True)
    view.draw()
    time.sleep(1)


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
model.add_block(5, GameWindow)
model.add_enemy(5, GameWindow)
model.add_block(1, GameWindow, True)
model.floorTest()
controller = KeyboardController(model)

while not alive:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            die()

        controller.handle_event(event,tock)

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

    for tock in range(1, 50):
        update(tock)
        tock += 1
    die()

    '''
    #reads serial output of arduino
    while (1==1):
        if (arduinoSerialData.inWaiting()>0):
            myData = arduinoSerialData.readline()
            print myData
    '''

    print('that testing sure did happen')
