import pygame as pg
from turret import Turret
import math

class Wizard(Turret):
    def pick_target(self, enemy_group):
        highestHealth = 0
        # check distance to each enemy to see if it is in range
        for enemy in enemy_group:
            x_dist = enemy.pos[0] - self.x
            y_dist = enemy.pos[1] - self.y
            dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
            if dist < self.range:
                if enemy.health > 0:
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    # print(self.angle)
                    if abs(self.angle) > 90:
                        self.mirror = True
                    else:
                        self.mirror = False
                    if self.targeting == "furthest":
                        self.target = enemy
                        # print("furthest: "+str(dist))
                    elif self.targeting == "thoughest":
                        if enemy.health > highestHealth:
                            self.target = enemy
                            highestHealth = enemy.health
        if self.target:
            for enemy in enemy_group:
                x_dist = enemy.pos[0] - self.target.pos[0]
                y_dist = enemy.pos[1] - self.target.pos[0]
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    if enemy.health > 0:
                        enemy.health -= self.damage
                        enemy.image.fill((190, 0, 0, 100), special_flags=pg.BLEND_ADD)
            return


