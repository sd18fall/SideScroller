'''
Model for SideScroller Game
Contains: Model, Character, Player, Enemy, Blocks, and Background classes

'''

import math
import pygame
import random
from calibrate_sonar import SonarController, randomController


# ==============================================================================
#                              Main Model Class
# ==============================================================================
class Model:
    '''The game's model contains all the parts currently tracked as a part of the game.
    Attributes: size, player, blocks, enemies
    Methods: add_block, add_enemy, update, floorTest
    '''
    def __init__(self, size, px=100, py=100):
        self.size = size
        self.player = Player(px, py)    # place a Player character
        self.blocks = []        # list of Block objects
        self.enemies = []       # list of Enemy objects
        self.endGame = False
        self.background = []
        self.start=False
        self.sonar = SonarController(1, 4) # Min and max multiplier given to player jump height and duration
        # self.sonar = randomController()    # for testing purposes, reports random data

    def add_block(self,num_block, screen, end_block = False, first_block = False,  screenx = 800, screeny = 500):
        '''Add a randomly generated set of blocks anywhere onscreen'''
        counter = 0
        if first_block == True:
            self.blocks.append(Block(100, 200))
        if end_block == True:
            for block in self.blocks:
                if block.x > 650:
                    counter +=1
            if counter < 1:
                self.blocks.append(Block((800), random.randint(100,screeny-100)))
                self.blocks.append(Block((800), random.randint(100,screeny-100)))
        if end_block == False and first_block == False:
            for i in range(num_block):
                    self.blocks.append(Block(800/num_block*i,random.randint(100,screeny-100)))

        for i in self.blocks:
            i.appear(screen)

    def add_enemy(self,num_enemy, screen, endemy = False, spawn = 3,  screenx = 800, screeny = 500):
        counter = 0
        if endemy == True and spawn ==3:
            for enemy in self.enemies:
                if enemy.x > 650:
                    counter +=1
            if counter < 1:
                self.enemies.append(Enemy((800), random.randint(0,screeny)))
        if endemy == False:
            for i in range(num_enemy):
                    self.enemies.append(Enemy(random.randint(400,screenx),random.randint(0,screeny)))

        for i in self.enemies:
            i.appear(screen)

    def add_background(self, screen, first_screen = False):
        counter = 0
        if first_screen == True:
            self.background.append(Background(0,0))
        else:
            for back in self.background:
                if back.x >= 0:
                    counter +=1
            if counter<1:
                self.background.append(Background(back.x+800,0))
        for back in self.background:
            back.appear(screen)

    def drawTitle(self, screen):
        showSprite = pygame.image.load('title.png').convert_alpha()
        screen.blit(pygame.transform.scale(showSprite, (800, 500)), (0, 0))

    def checkSwipe(self):
        if self.sonar.data() != None:
            self.start = True
            print (1)


    def update(self, tock, screen, increment):
        #print('**ping-', end="\n")
        sonarH = self.sonar.data()
        #print('**pong', end="\n")
        self.player.update(self.blocks, self.enemies, tock, increment, sonarH)
        for i, block in enumerate(self.blocks):
            if block.x < -150:
                    del self.blocks[i]
            block.update()
        for i, enemy in enumerate(self.enemies):
            if enemy.x < -50:
                    del self.enemies[i]
            enemy.update(self.blocks, increment)
            enemy.shoot(screen,self.player,1)

        for i, back in enumerate(self.background):
            if back.x < -800:
                    del self.background[i]
            back.update()

        self.shouldEnd()

    def appear(self, screen):
        for back in self.background:
            back.appear(screen)
        for block in self.blocks:
            block.appear(screen)
        for enemy in self.enemies:
            enemy.appear(screen)
        self.player.appear(screen)

    def shouldEnd(self):
        if self.player.death == True:
            self.endGame = True

# ==============================================================================
#                                 Characters
# ==============================================================================

class Character:
    '''
    Defines the basic features of a character in the game.
    Player and Enemy classes will inherit from this.

    Attributes: x, y, v (y-velocity), size, sprite
                jumpStart (a tock time), midJump (boolean)
    Methods: update, appear, rect, collision
    '''

    def __init__(self, x, y, vx = 0, vy = 0, size = 25, sprite = "butter.png", jumpSprite = "butter.png"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

        self.size = size
        self.sprite = sprite
        self.floorSprite = sprite
        self.jumpSprite = jumpSprite
        self.distortx = self.size

        self.jumpStart = None
        self.floor = False

    def rect(self):
        '''Makes a pygame Rect object for the character.
        Must be updated for any new x-y values, and called as charName.rect()'''
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def collision(self, blockSet, increment = 3):
        '''Detect characters colliding with blocks and bump them back appropriately.
        Convert things into rect form and use pygame's collildelistall rect method
            to find all collisions
        For each block that we collided with, check which side of the character
            is within the block's space. Then, move character the opposite direction.
            '''

        self.floor = False
        char = self.rect()
        blockRects = [block.rect() for block in blockSet]

        indicies = char.collidelistall(blockRects)

        for i in indicies:
            thisBlock = blockRects[i]
            #if thisBlock.left >= char.right and char.right <= thisBlock.left: #hit right
            if thisBlock.left >= char.right and char.center < thisBlock.left:
                self.x = thisBlock.left - self.size
                self.vx = 0
            if thisBlock.left >= char.right : #hit left
                self.x = thisBlock.right + self.size
                self.vx = 0
            if thisBlock.bottom >= char.top and char.top >= thisBlock.top: #hit top
                self.jumpStart = None
                self.y = thisBlock.bottom
                self.vy += increment

            if thisBlock.bottom >= char.bottom and char.bottom >= thisBlock.top: #hit floor
                self.y = thisBlock.top - self.size + 1
                self.vy = 0
                self.floor = True
                self.jumpStart = None
                self.sprite = self.floorSprite
                self.distortx = int(self.size * 2.4)

        # If we're not currently jumping, and none of these collisions is a floor, fall.
        if self.jumpStart == None and not self.floor:
            self.vy = increment
            self.sprite = self.jumpSprite
            self.distortx = self.size * 3

class Enemy(Character):
    '''Class for enemy characters, inheriting from the general Character.'''

    def update(self, blockSet, increment=3):
        self.collision(blockSet, increment)
        self.y = self.y + self.vy
        self.x = self.x + self.vx
        self.x -= increment   #shift to follow screen

    def appear(self, screen):
        showSprite = pygame.image.load(self.sprite).convert_alpha()
        screen.blit(pygame.transform.scale(showSprite, (40, 40)), (self.x, self.y-15))

    def shoot(self, screen,  player, difficulty = 1):
        self.projectile = Projectile(self.x,self.y)
        self.projectile.appear(screen)
        self.projectile.update()
        if difficulty == 1:
            pass
        elif difficulty ==2:
            self.projectile.go('left')
        elif difficulty ==3:
            self.projectile.aimed_shot(player, self)

class Projectile(Enemy):
    '''
    Class for projectiles that enemies shoot

    '''
    def appear(self, screen):
        pygame.draw.ellipse(screen, (255,0,0), self.rect())

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

    def vanish(self,  screenx = 800, screeny = 500):
        #Temporary hiding code
        # TODO: this.
        self.x = screenx+10
        self.y = screeny+10
        self.vx = 0
        self.vy = 0

    def collision(self, blockSet):
        '''Converts all walls into rectangles and uses pygame's colliderect rect method to find any collisions. In case of a collision, vanish is called.'''
        char = self.rect()
        for block in blockSet:
            if char.colliderect(block.rect()):
                self.vanish()

class Player(Character):
    '''Class for player, inheriting from general Character.
    New Attributes: death, jumpPower
    New Methods: enemyEncounter, jump'''

    def __init__(self, x, y, vx = 0, vy = 0, size = 25, sprite = "TOAST.png", jumpSprite = "toast_jump.png"):
        '''Initialize player with similar parameters as character
        New variables: jumpPower, death'''
        super().__init__(x, y, vx, vy, size, sprite, jumpSprite)
        self.jumpPower = 1
        self.death = False

    def update(self, blockSet, enemySet, tock, increment, sonarH = None, screenx = 800, screeny = 500):
        '''Updates the character by checking if the player is on screen, jumping, hitting an enemy, or hitting a block'''
        # Jump and move
        self.startJump(tock, sonarH)
        if self.jumpStart != None:
            self.jump(tock, increment)
        self.y = self.y + self.vy
        # Do we need to die or collide
        self.onScreen(screenx, screeny)
        self.enemyEncounter(enemySet)
        self.collision(blockSet, increment)

    def appear(self, screen):
        '''Draws character with given sprite'''
        showSprite = pygame.image.load(self.sprite).convert_alpha()
        screen.blit(pygame.transform.scale(showSprite, (self.distortx, 60)), (self.x, self.y-17))

    def startJump(self, tock, sonarH):
        '''Initializes a jump if a hand is over the sonar'''
        if sonarH is not None and self.floor:   # If the sonar sees a hand and we're on the floor
            self.jumpStart = tock           # make the current tock the start time.
            self.jumpPower = sonarH         # set the power for this jump

    def jump(self, tock, increment = 3):
        '''Makes the character jump for tock amount of time. jumpPower based on sonar readings'''
        if tock - self.jumpStart < 2 + 2*self.jumpPower: #old; jumpDuration/2 = 8:   # Rise for the first half of the jump
            self.vy = -int(self.jumpPower*increment)
        else:     # If we're not rising, stop jumping and reset
            self.jumpStart = None
            self.jumpPower = 1

    def enemyEncounter(self, enemySet):
        '''Converts all characters into rectangles and uses pygame's 'colliderect'
        rect method to find any collisions. In case of a collision, self.death is true.'''
        char = self.rect()
        for enemy in enemySet:
            if char.colliderect(enemy.rect()):
                self.death = True

    def onScreen(self,  screenx = 800, screeny = 500):
        '''Makes sure the character is still on screen'''
        # If you fall off the bottom or left, die.
        # Over-screen top bumps you back on.
        if self.y > screeny or self.x < 0:
            self.death = True
        if self.y < 0:
            self.y = 0


# ==============================================================================
#                                Other Subclasses
# ==============================================================================
class Block():
    '''Class for rectangular blocks for the characters to navigate.
    Attributes: x, y, w (width), h (height), color
    Methods: rect, appear
    '''
    def __init__(self, x, y, width = 150, height = 20, color = (0,0,150), sprite = "plate.png"):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.sprite = sprite
        self.color = color

    def rect(self):
        '''Makes a pygame Rect object to display and test for collisions.'''
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def appear(self, screen):
        '''Makes the block appear at x, y with the given sprite'''
        showSprite = pygame.image.load(self.sprite).convert_alpha()
        screen.blit(pygame.transform.scale(showSprite, (self.w, self.h)), (self.x, self.y))

    def update(self, increment = 3):
        '''Update block x value as screen moves'''
        self.x -= increment

class Background():
        '''
        Class for background of the game. Because it is a sidescroller, the background moves with the gameself.
        Attributes: x, y
        Methods: appear, update
        '''
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def appear(self, screen):
            '''Shows the background on the screen at x, y'''
            showSprite = pygame.image.load('kitchen-min.png').convert_alpha()
            screen.blit(showSprite, (self.x, self.y))
        def update(self, increment = 3):
            '''Updates the x position of the background. Moves at half speed of other game objects'''
            self.x -= increment/3
