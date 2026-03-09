import pygame as pg
import constants as c
from enemy_data import ENEMY_SPAWN_DATA
import random

class World():
  def __init__(self, data, map_image):
    self.waypoints = []
    self.tilemap = []
    self.level_data = data
    self.image = map_image
    #Enemy management
    self.level = 0
    self.enemyList = []
    self.enemiesSpawned = 0
    self.enemiesPassed = 0
    #Game mechanics
    self.health=c.HEALTH ####
    self.money=c.MONEY ####

    # create the empty tilemap
    for i in range(c.ROWS):
      self.tilemap.append([0] * c.COLS)

  def Process_data(self):
    #look through data to extract relevant info
    #print(self.level_data)
    for key in self.level_data:
      regions = self.level_data[key]["regions"]
      for region in regions:
        shape = region["shape_attributes"]
        x_coords = shape["all_points_x"]
        y_coords = shape["all_points_y"]
        self.waypoints = list(zip(x_coords, y_coords))
        #print(self.waypoints)

  def ProcessWaypoints(self):
    # convert first point
    start_x = clamp(int(self.waypoints[0][0] // c.TILE_SIZE), 0, c.COLS - 1)
    start_y = clamp(int(self.waypoints[0][1] // c.TILE_SIZE), 0, c.ROWS - 1)

    for (px, py) in self.waypoints:
      end_x = clamp(int(px // c.TILE_SIZE), 0, c.COLS - 1)
      end_y = clamp(int(py // c.TILE_SIZE), 0, c.ROWS - 1)

      # fill horizontal
      while start_x != end_x:
          self.tilemap[start_y][start_x] = 1
          start_x += 1 if start_x < end_x else -1

      # fill vertical
      while start_y != end_y:
          self.tilemap[start_y][start_x] = 1
          start_y += 1 if start_y < end_y else -1

      # mark final tile
      self.tilemap[start_y][start_x] = 1


  def ProcessEnemies(self):
    levelSpawnData=ENEMY_SPAWN_DATA[self.level] #The list of enemies for the level
    for enemyType in levelSpawnData: #Loop through every type in that list (eg.: normal, fast, etc.)
      enemiesToSpawn = levelSpawnData[enemyType] #Load in the correct number of enemies for this type
      for enemy in range(enemiesToSpawn): #repeat until we reach the correct number of them
        self.enemyList.append(enemyType) #Add the correct type of enemy
    random.shuffle(self.enemyList)
    print(self.enemyList)

  def draw(self, surface):
    surface.blit(self.image, (0, 0))


  #def process_waypoints(self, data):
    #iterate through waypoints to extract individual sets of x and y coordinates
    #for point in data:
      #temp_x = point.get("x")
      #temp_y = point.get("y")
      #self.waypoints.append((temp_x, temp_y))


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))