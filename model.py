'''

Model for SideScroller Game

'''

import math
import pygame
import random
class Model:
    """The game's model contains all the parts currently tracked as a part of the game.
    Attributes: size, player, blocks, enemies
    Methods: add_block, add_enemy, update, floorTest
    """
    def __init__(self, size, px=100, py=100):
        self.size = size
        self.player = Player(px, py)    # place a Player character
        self.blocks = []        # list of Block objects
        self.enemies = []       # list of Enemy objects
        self.endgame = False
        self.background = []
        self.sonar = SonarController()    # will request port number and calibration

    def add_block(self,num_block, screen, end_block = False,  screenx = 800, screeny = 500):
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
                    self.enemies.append(Enemy(random.randint(0,screenx),random.randint(0,screeny)))

        for i in self.enemies:
            i.appear(screen)

    def add_background(self, screen, first_screen = False):
        counter = 0
        if first_screen == True:
            self.background.append(Background(0,0))
        for back in self.background:
            if back.x >= 0:
                counter +=1
        if counter<1:
            self.background.append(Background(800,0))
        for back in self.background:
            back.appear(screen)

    def update(self, tock, screen):
        #sonarH = self.sonar.data()
        sonarH = 2
        self.player.update(self.blocks, self.enemies, tock, sonarH)
        for block in self.blocks:
            block.update()
        for enemy in self.enemies:
            enemy.update(self.blocks, tock)
            enemy.shoot(screen,self.player,2)
        for back in self.background:
            back.update()
        self.endGame()



    def appear(self, screen):
        for back in self.background:
            back.appear(screen)
        for block in self.blocks:
            block.appear(screen)
        for enemy in self.enemies:
            enemy.appear(screen)
        self.player.appear(screen)
    def endGame(self):
        if self.player.death == True:
            self.endgame = True
    def floorTest(self, screenx = 800, screeny = 500):
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
    def __init__(self, x, y, vx = 0, vy = 0, size = 25, sprite = None ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.sprite = 'TOAST.png'
        self.distortx = 25
        self.death = False
        self.jumpStart = None # when did the jump start (in tocks)

    def update(self, blockSet, tock, increment=3):
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

    def jump(self, tock, sonarH = 2, increment = 5, jumpDuration = 16):

        if self.jumpStart is None:
            # If we haven't started jumping already, make the current tock the start time.
            self.jumpStart = tock
        if tock - self.jumpStart < (jumpDuration)/2:
            # Rise for the first half of the jump
            self.vy = -(2*increment)
        else:
            # If we're not rising, stop 'jumping'. Falling is taken care of elsewhere.
            self.jumpStart = None


    def collision(self, blockSet, increment = 5):
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
            if thisBlock.left >= char.right and char.right <= thisBlock.left:
                #and char.right+10 <= thisBlock.centerx:
                #print('hit right')
                self.x = thisBlock.left - self.size
                self.vx = 0
            #if thisBlock.left <= char.left+12 and char.left+12 <= thisBlock.left:
                #and char.left-10 >= thisBlock.centerx:
                #print('hit left')
            #    self.x = thisBlock.right
            #    self.vx = 0
            if thisBlock.bottom >= char.top and char.top >= thisBlock.top:
                #print('hit top')
                self.jumpStart = None
                self.y = thisBlock.bottom
                self.vy += increment

            if thisBlock.bottom >= char.bottom and char.bottom >= thisBlock.top:
                #print('hit floor')
                self.y = thisBlock.top - self.size +1
                self.vy = 0
                floorFlag = True
                # self.floor = True
                self.jumpStart = None
                self.sprite = "TOAST.png"
                self.distortx = 40

        # If none of these collisions is a floor, and we're not currently jumping, fall.
        if self.jumpStart == None and not floorFlag:#self.floor:
            self.vy = increment
            self.sprite = "toast_jump.png"
            self.distortx = 55

class Enemy(Character):
    """Class for enemy characters, inheriting from the general Character."""
    def appear(self, screen):
        #draw the sprite at x, y
        #pygame.draw.rect(screen, (255,0,0), self.rect())
        #pygame.image.load('butter.png')
        butter = pygame.image.load("butter.png").convert_alpha()

        screen.blit(pygame.transform.scale(butter, (40, 40)), (self.x, self.y-15))
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
    '''Class for projectiles that enemies shoot'''
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
    def appear(self, screen):
        #draw the sprite at x, y
        #pygame.draw.rect(screen, (0,255,0), self.rect())
        butter = pygame.image.load(self.sprite).convert_alpha()

        screen.blit(pygame.transform.scale(butter, (self.distortx, 40)), (self.x, self.y-17))
    def enemyEncounter(self, enemySet):
        """Converts all characters into rectangles and uses pygame's 'colliderect'
        rect method to find any collisions. In case of a collision, self.death is true."""
        char = self.rect()
        for enemy in enemySet:
            if char.colliderect(enemy.rect()):
                self.death = True

    def onScreen(self,  screenx = 800, screeny = 500):
        if self.y > screeny or self.y < 0 or self.x < 0:
            # If you go offscreen up, down, or left, die.
            self.death = True

    def update(self, blockSet, enemySet, tock, sonarH=2, screenx = 800, screeny = 500):
        self.onScreen(screenx, screeny)
        if self.jumpStart != None:
            self.jump(tock)
        self.y = self.y + self.vy
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

    def appear(self, screen):
        pygame.draw.rect(screen, self.color, self.rect())

    def update(self, increment=3):
        self.x-=increment

class Background():
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def appear(self, screen):
            kitchen = pygame.image.load('kitchen.png').convert_alpha()
            screen.blit(pygame.transform.scale(kitchen, (800, 500)), (self.x, self.y))
        def update(self, increment=3):
            self.x-=increment
