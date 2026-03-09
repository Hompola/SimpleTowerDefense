#the fun bits
import pygame.draw

import constants
from constants import tileSize
import pygame as pg
import math


class Tower(pg.sprite.Sprite):
    def __init__(self, spriteSheet, column, row):
        pg.sprite.Sprite.__init__(self)
        #position variables
        self.column = column
        self.row = row
        #calculate center coordinates
        self.x = tileSize * (column + 0.5)
        self.y = tileSize * (row + 0.5)
        #animation Variables
        self.frame = 0
        self.spriteSheet = spriteSheet
        self.animationList = self.LoadImage()
        self.originalImage = self.animationList[self.frame]
        self.image=pg.transform.rotate(self.originalImage,0)
        #self.image=self.originalImage
        #turret bounding rectangle
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        #cool down variables
        self.cooldown = 1000
        self.timeFromLastShot = pg.time.get_ticks()
        self.timeFromLastFrame = pg.time.get_ticks()
        #translusent range circle
        self.range = 90
        self.rangeImage = pg.Surface((self.range * 2, self.range * 2))
        self.rangeImage.fill("black")
        self.rangeImage.set_colorkey("black")
        pg.draw.circle(self.rangeImage, "grey100", (self.range, self.range), self.range)
        self.rangeImage.set_alpha(100)
        self.ranRect = self.rangeImage.get_rect()
        self.ranRect.center = self.rect.center
        self.selected = False
        #target calculation variables
        self.angle=90
        self.mirrored=False
        self.target = None

    def LoadImage(self):
        sideLength = self.spriteSheet.get_height()
        animationList = []
        for frame in range(0, 8):
            tempImg = self.spriteSheet.subsurface(frame * sideLength, 0, sideLength, sideLength)
            animationList.append(tempImg)
        return animationList

    def DancingTurret(self):
        #update ScreenImage
        self.originalImage = self.animationList[self.frame] ####
        if pg.time.get_ticks() - self.timeFromLastFrame > constants.animationDelay:
            self.timeFromLastFrame = pg.time.get_ticks()
            self.frame += 1
            if self.frame == len(self.animationList):
                self.frame = 0
                self.timeFromLastShot = pg.time.get_ticks()
                self.target=None


    def update(self,enemyGroup,screen):
        if self.target:
            self.DancingTurret()
        else: ####
            if pg.time.get_ticks() - self.timeFromLastShot > self.cooldown:
                self.TargetSpotted(enemyGroup, screen)

    def draw(self, surface):
        self.image=pg.transform.flip(self.originalImage,self.mirrored,False)
        self.rect=self.image.get_rect()
        self.rect.center=(self.x,self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.rangeImage, self.ranRect)
            self.selected = False

    def TargetSpotted(self,enemyGroup,screen):
        xDist=0
        yDist=0
        for enemy in enemyGroup:
            xDist=enemy.pos[0]-self.x
            yDist=enemy.pos[1]-self.y
            dist=math.sqrt(xDist**2+yDist**2)
            if dist<self.range:
                self.target=enemy
                #tangent is calculating angle
                self.angle=math.degrees(math.atan2(-yDist, xDist))
                print(self.angle)
                if abs(self.angle)>90:
                    self.mirrored=True ####
                else:
                    self.mirrored=False