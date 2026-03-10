import pygame as pg
import json

import turret_data
from world import World
import constants as c
from button import Button

def setupGame():
    #initialise pygame
    pg.init()
    #create clock
    clock = pg.time.Clock()

    #create game window
    screen = pg.display.set_mode((c.SCREEN_WIDTH+c.SIDEBAR_WIDTH, c.SCREEN_HEIGHT))
    pg.display.set_caption("Tower Defence")
    # load json data for level
    with open('levels/custom_level_720.json') as file:
      world_data = json.load(file)

    # create world
    mapImage = pg.image.load('levels/custom_level_720_v2.png').convert_alpha()
    world = World(world_data, mapImage)
    world.Process_data()
    world.ProcessWaypoints()
    world.ProcessEnemies()

# enemies
enemyImages = {
    "normal": pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
    "fast": pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(),
    "tank": pg.image.load('assets/images/enemies/enemy_3.png').convert_alpha(),
    "elite": pg.image.load('assets/images/enemies/Zomboss(Custom).png').convert_alpha()
}

turret_sheet = pg.image.load('assets/images/turrets/ArcherUnit_75px.png').convert_alpha()
cursorTurretImage = pg.image.load('assets/images/turrets/ArcherUnit_75px_cursor.png').convert_alpha()
# shop buttons ####
upgradeButtonImage = pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()
furthestTargetImage = pg.image.load('assets/images/buttons/furthestTarget_button_50px.png').convert_alpha()
thoughestTargetImage = pg.image.load('assets/images/buttons/thoughestTarget_button_50px.png').convert_alpha()

buy_turret_image = pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
archerButtonImage = pg.image.load('assets/images/buttons/archer_button50px.png').convert_alpha()  ####
crossbowButtonImage = pg.image.load('assets/images/buttons/crossbow_button50px.png').convert_alpha()  ####
wizardButtonImage = pg.image.load('assets/images/buttons/wizard_button50px.png').convert_alpha()  ####

startRoundImage = pg.image.load('assets/images/buttons/begin.png').convert_alpha()
# gui
heart = pg.image.load('assets/images/gui/heart.png').convert_alpha()
coin = pg.image.load('assets/images/gui/coin.png').convert_alpha()

# create buttons
upgradeButton = Button(c.SCREEN_WIDTH + 30, 30, upgradeButtonImage, True)
furthestTargetButton = Button(c.SCREEN_WIDTH + 30, 90, furthestTargetImage, True)  ####
thoughestTargetButton = Button(c.SCREEN_WIDTH + 90, 90, thoughestTargetImage, True)  ####
turret_button = Button(c.SCREEN_WIDTH + 30, 170, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + buy_turret_image.get_width() + 40, 170, cancel_image, True)
archerButton = Button(c.SCREEN_WIDTH + 30, 230, archerButtonImage, True)
crossbowButton = Button(c.SCREEN_WIDTH + 90, 230, crossbowButtonImage, True)
wizardButton = Button(c.SCREEN_WIDTH + 150, 230, wizardButtonImage, True)
startRoundButton = Button(c.SCREEN_WIDTH + 30, 330, startRoundImage, True)
