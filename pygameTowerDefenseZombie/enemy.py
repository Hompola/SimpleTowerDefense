import pygame as pg
from pygame.math import Vector2
import math


#the sailor went to sea sea sea to see what he could see see see but all that he could he see see see was the bottom of the deep blue sea sea sea
class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.targ = 1  #target waypoint for hoomans not phrogs

        self.speed = 1
        self.angle = 0

        self.originalImage = image
        self.image = pg.transform.rotate(self.originalImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.move()
        self.rotate()

    def move(self):
        #q1234567890-=qwertyuiop[]\asdfghjkl;'zxcvbnm,./!@#$%^&*()_+QWERTYUIOP{}}}}}}|ASDFGHJKL:"ZXCVBNM<>>
        if self.targ < len(self.waypoints):
            self.destiny = Vector2(self.waypoints[self.targ])
            self.movement = self.destiny - self.pos

        else:
            self.kill()

        dist = self.movement.length()

        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed


        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.targ += 1
        return

    def rotate(self):
        dist = self.destiny - self.pos
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        self.image = pg.transform.rotate(self.originalImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
