"""This is a game. It will have cool input.
It was made by Anya and Liz."""

# ==============================================================================
#                                  Libraries
# ==============================================================================
import pygame
from pygame.locals import *
#used to connect to arduino
import serial #must install pySerial using 'pip install pyserial'
import random
import math

screenx = 800
screeny = 500
# ==============================================================================
#                                  Classes
# ==============================================================================

class Model:
    def __init__(self, size, px=screenx*1/2, py=screeny*3/4):
        self.size = size
        self.player = Player(px, py)
        self.blocks = []
        self.enemies = []

    def add_block(self,num_block, screen):
        for i in range(num_block):
            self.blocks.append(Block(random.randint(0,800),random.randint(0,400)))
        for i in self.blocks:
            i.appear(screen)

    def add_enemy(self,num_enemy, screen):
        for i in range(num_enemy):
            self.enemies.append(Enemy(random.randint(0,800),random.randint(0,400)))
        for i in self.enemies:
            i.appear(screen)

    def update(self):
        self.player.update(self.blocks)

    def floorTest(self):
        self.blocks.append(Block(0, screeny*4/5, width=600, height=15, color=(255,255,0)))
        self.blocks.append(Block(random.randint(400,600),random.randint(350,425)))

class Character:
    '''
    Defines the basic features of a character in the game
    Attributes: x, y, v (y-velocity), size, sprite
    Methods: jump, update, appear, collision
    '''
    def __init__(self, x, y, v=0, size=25, sprite=None):
        self.x = x
        self.y = y
        self.v = v
        self.size = size
        self.sprite = sprite
        self.jumpStart = None
        self.midJump = False

    def update(self, blockSet):
        self.collision(blockSet)
        self.y = self.y + self.v
        self.appear(GameWindow)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def appear(self, screen):
        #draw the sprite at x, y
        pygame.draw.rect(screen, (0,255,0), self.rect())

    def jump(self, tock):
        if self.jumpStart is None:
            self.jumpStart = tock
            self.midJump = True

        if tock - self.jumpStart > jumpDuration-2:
            self.jumpStart = None
            self.midJump = False
        elif tock - self.jumpStart <= (jumpDuration-2)/2:
            self.v = -increment
        elif tock - self.jumpStart > (jumpDuration-2)/2:
            self.v = increment

    def collision(self, blockSet):
        floorFlag = False
        char = self.rect()
        blockRects = []
        for block in blockSet:
            blockRects.append(block.rect())
        # blockList = [block.rect() for block in blockSet]

        indicies = char.collidelistall(blockRects)
        print(indicies)

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

        # fall if you're not mid-jump or on the floor
        if not self.midJump and not floorFlag:
            self.v = increment


class Enemy(Character):
    '''
    Defines the enemies in the pygame
    Plan on using
    '''
    pass


class Player(Character):
    def enemyEncounter(self, enemySet):
        char = self.rect()
        for enemy in enemySet:
            if char.colliderect(enemy.rect()):
                die()


class Block:
    def __init__(self, x, y, width=20, height=50, color=(255,0,0)):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.color = color

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def appear(self, screen):
        pygame.draw.rect(screen, self.color, self.rect())


class View():
    def __init__(self, model, size):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height """
        self.model = model
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        """ Draw the current game state to the screen """
        for i in range(800):
            pygame.draw.line(self.screen,(i/8+40,i/20+20,i/7+70),(i,0),(i,700))
        for block in self.model.blocks:
            pygame.draw.rect(self.screen,pygame.Color(255, 0, 0),pygame.Rect(block.x,block.y,block.w,block.h))
        pygame.draw.rect(self.screen,pygame.Color(0, 255, 0),pygame.Rect(self.model.player.x,self.model.player.y,self.model.player.size,self.model.player.size))
        pygame.display.update()

class KeyboardController():
    """ Handles keyboard input for brick breaker """
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        """ Up and down presses modify the y of the player """
        if event.type != pygame.locals.KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.model.player.y += -10.0
            self.model.update()
        if event.key == pygame.K_DOWN:
            self.model.player.y += 10.0
            self.model.update()



# ==============================================================================
#                                  Setup
# ==============================================================================
# arduinoSerialData = serial.Serial('com11',9600) #com11 can be changed to whatever port arduino is connected to

tock = 0
jumpDuration = 10 # must be even
increment = 5


# ==============================================================================
#                                 Functions
# ==============================================================================
#defines what happens in event of collisions
#calls your classes and pictures and stuff
#appropriately moves things

def update(tock):

    model.update()
    # model.player.jump(tock)
    model.player.x += increment

def calibrate():
    """Calibrate the sensors"""
    print("Please hold your hands at your comfortable lower limit")
    # Do arduino magic
    print("Please hold your hands at your comfortable upper limit")
    # Do arduino magic
    print("Please remove your hands from the sensors")
    # Do arduino magic

def die():
    print("You died! Play again.")
    pygame.quit()
    global alive
    alive = False

# ==============================================================================
#                                  Main
# ==============================================================================
pygame.init()
alive = True

screenx = 800
screeny = 500
size = (screenx,screeny)
pygame.display.set_mode(size)
GameWindow = pygame.display.set_mode((screenx, screeny))
model = Model(size)
view = View(model, size)
model.add_block(5, GameWindow)
model.floorTest()
controller = KeyboardController(model)


while alive:
    view.draw()
    for event in pygame.event.get():
        controller.handle_event(event)
    update(tock)

    if input("What do? ") == 'Die':
        die()

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
