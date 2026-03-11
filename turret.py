import pygame as pg
import constants as c
import math
from turret_data import TURRET_DATA

class Turret(pg.sprite.Sprite):
  def __init__(self, sprite_sheet, row, col, turretType):
    pg.sprite.Sprite.__init__(self)
    self.upgradeLevel=1
    self.turretType = turretType
    self.turretTypeData=TURRET_DATA.get(turretType)
    self.buyCost = self.turretTypeData.get("buyCost")
    self.upgradeCost=self.turretTypeData.get("upgradeCost")
    self.maxLevel= self.turretTypeData.get("maxLevel")
    self.range = self.turretTypeData.get(self.upgradeLevel).get("range")
    self.cooldown = self.turretTypeData.get(self.upgradeLevel).get("cooldown")
    self.damage = self.turretTypeData.get(self.upgradeLevel).get("damage") ####
    self.last_shot = pg.time.get_ticks()
    print(self.range, self.cooldown)

    #get tile
    self.tileX = col
    self.tileY = row

    #calculate center coordinates
    self.x = (self.tileX + 0.5) * c.TILE_SIZE
    self.y = (self.tileY + 0.5) * c.TILE_SIZE

    # animation variables
    self.sprite_sheet = sprite_sheet
    self.animation_list = self.load_images()
    self.frame_index = 0
    self.update_time = pg.time.get_ticks()

    # Stetup image update framework
    self.angle = 0
    self.mirror=False
    self.original_image = self.animation_list[self.frame_index] #####
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = (self.x, self.y)

    #Transparent circle
    self.range_image = pg.Surface((self.range * 2, self.range * 2))
    self.range_image.fill((0, 0, 0))
    self.range_image.set_colorkey((0, 0, 0))
    self.rangeImageColor="grey100"
    pg.draw.circle(self.range_image, self.rangeImageColor, (self.range, self.range), self.range)
    self.range_image.set_alpha(100)
    self.range_rect = self.range_image.get_rect()
    self.range_rect.center = self.rect.center
    self.selected=False

    #Enemy interaction
    self.target=None
    self.targeting = "furthest" ####



  def load_images(self):
    # extract images from spritesheet
    size = self.sprite_sheet.get_height()
    animation_list = []
    for i in range(c.ANIMATION_STEPS):
      #print(size, width, i)
      temp_img = self.sprite_sheet.subsurface(i * size, 0, size, size)
      animation_list.append(temp_img)
    return animation_list


  def play_animation(self):
    self.original_image=self.animation_list[self.frame_index] #####
    if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
      self.update_time = pg.time.get_ticks()
      self.frame_index += 1
      #print("frameindex:" + str(self.frame_index) + " out of " +str(len(self.animation_list)))
      # check if the animation has finished and reset to idle
      if self.frame_index >= len(self.animation_list):
        self.frame_index = 0
        # record completed time and clear target so cooldown can begin
        self.last_shot = pg.time.get_ticks()
        self.target = None


  def update(self, enemy_group):
    #shoot or search for new target once turret has cooled down
    if self.target:
      self.play_animation()
    else:
      # search for new target once turret has cooled down
      if pg.time.get_ticks() - self.last_shot > self.cooldown:
        self.pick_target(enemy_group)

  def draw(self, surface):
    self.image = pg.transform.flip(self.original_image, self.mirror, False)
    self.rect = self.image.get_rect()
    self.rect.center = (self.x, self.y)
    surface.blit(self.image, self.rect)
    if self.selected:
      surface.blit(self.range_image, self.range_rect)


  def pick_target(self, enemy_group):
    #find an enemy to target
    x_dist = 0
    y_dist = 0
    highestHealth = 0
    #check distance to each enemy to see if it is in range
    for enemy in enemy_group:
      x_dist = enemy.pos[0] - self.x
      y_dist = enemy.pos[1] - self.y
      dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
      if dist < self.range:
        if enemy.health>0:
          self.angle = math.degrees(math.atan2(-y_dist, x_dist))
          #print(self.angle)
          if abs(self.angle)>90: self.mirror=True
          else: self.mirror=False
          if self.targeting == "furthest": ####
            self.target = enemy
            self.target.health -= self.damage ####
            #print("furthest: "+str(dist))
            return
          elif self.targeting == "strongest": ####
            if enemy.health > highestHealth:
              self.target = enemy
              highestHealth = enemy.health
    if self.target: ####
      #print("thougest"+str(self.target.health))
      self.target.health -= self.damage  ####
      self.target.image.fill((190, 0, 0, 100), special_flags=pg.BLEND_ADD)

  def UpdateRangeImage(self): ####
    self.range_image = pg.Surface((self.range * 2, self.range * 2))
    self.range_image.fill((0, 0, 0))
    self.range_image.set_colorkey((0, 0, 0))
    pg.draw.circle(self.range_image, self.rangeImageColor, (self.range, self.range), self.range)
    self.range_image.set_alpha(100)
    self.range_rect = self.range_image.get_rect()
    self.range_rect.center = self.rect.center


  def Upgrade(self):
    if self.upgradeLevel<self.maxLevel:
      self.upgradeLevel+=1
    else: return

    self.range = self.turretTypeData.get(self.upgradeLevel).get("range")
    self.maxLevel = self.turretTypeData.get("maxLevel")
    self.cooldown = self.turretTypeData.get(self.upgradeLevel).get("cooldown")
    self.UpdateRangeImage()
    print(self.upgradeLevel)
    return self.upgradeLevel
  
  def ChangeTargeting(self, targeting, rangeImageColor):
    self.targeting = targeting
    self.rangeImageColor = rangeImageColor
    self.UpdateRangeImage()
