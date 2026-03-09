import pygame as pg
from pygame.math import Vector2
import math
from enemy_data import ENEMY_STATS

class Enemy(pg.sprite.Sprite):
  def __init__(self, waypoints, images, enemyType):
    pg.sprite.Sprite.__init__(self)
    self.enemyType= enemyType
    self.waypoints = waypoints
    #print(enemyType)
    self.pos = self.waypoints[0]
    self.target_waypoint = 1
    self.health= ENEMY_STATS.get(enemyType)["health"]
    self.speed = ENEMY_STATS.get(enemyType)["speed"]
    self.value = ENEMY_STATS.get(enemyType)["value"] ####
    self.angle = 0
    self.original_image = images.get(enemyType)
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos


  def update(self, world): ####
    self.move(world)
    self.rotate()
    self.CheckAlive(world) ####

  def move(self,world):
    #define a target waypoint
    if self.target_waypoint < len(self.waypoints):
      self.target = Vector2(self.waypoints[self.target_waypoint])
      self.movement = self.target - self.pos
    else:
      #enemy has reached the end of the path
      self.kill()
      world.health-=1

    #calculate distance to target
    dist = self.movement.length()
    #check if remaining distance is greater than the enemy speed
    if dist >= self.speed:
      self.pos += self.movement.normalize() * self.speed
    else:
      if dist != 0:
        self.pos += self.movement.normalize() * dist
      self.target_waypoint += 1

  def rotate(self):
    #calculate distance to next waypoint
    dist = self.target - self.pos
    #use distance to calculate angle
    self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
    #rotate image and update rectangle
    if self.enemyType != "elite":
      self.image = pg.transform.rotate(self.original_image, self.angle)
      self.rect = self.image.get_rect()
      self.rect.center = self.pos
    else:
      mirror=False
      if abs(self.angle) > 90: mirror = True
      self.image = pg.transform.flip(self.original_image, mirror, False)
      self.rect = self.image.get_rect()
      self.rect.center = self.pos-(0,35)

  def CheckAlive(self, world):
    if self.health<=0:
      world.money+= self.value ####
      self.kill()

