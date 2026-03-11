import pygame as pg
import json

import turret_data
from enemy import Enemy
from world import World
from turret import Turret
from wizard import Wizard
import constants as c
import assets
import game_handler as g
from button import Button

# initialise pygame
pg.init()
# create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDEBAR_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

# load assets
images = assets.LoadImages()
enemyImages = images["enemies"]
turretImages = images["turrets"]
uiImages = images["ui"]

# Game variables
levelStarted = False
placing_turrets = False
selectedTurret = None
#pre-load turret data at the start
turretData = g.UpdateTurretData("archer")
# create clocks
clock = pg.time.Clock()
lastEnemySpawn = pg.time.get_ticks()

# create world
world = g.SetupWorld(pathFile='levels/custom_level_720.json', mapImage=images["mapImage"])
# create empty groups
enemyGroup = pg.sprite.Group()
turretGroup = pg.sprite.Group()

# create buttons
upgradeButton = Button(image=uiImages["upgradeButtonImage"],
                       x=c.SCREEN_WIDTH + 30, y=90, single_click=True)
furthestTargetButton = Button(image=uiImages["furthestTargetImage"],
                              x=c.SCREEN_WIDTH + 30, y=30, single_click=True)
strongestTargetButton = Button(image=uiImages["strongestTargetImage"],
                               x=c.SCREEN_WIDTH + 90, y=30, single_click=True)
turretButton = Button(image=uiImages["buyTurretImage"],
                      x=c.SCREEN_WIDTH + 30, y=170, single_click=True)
cancelButton = Button(image=uiImages["cancelImage"],
                      x=c.SCREEN_WIDTH+uiImages["buyTurretImage"].get_width() + 40, y=170, single_click=True)
sellButton = Button(image=uiImages["sellImage"],
                    x=c.SCREEN_WIDTH + uiImages["upgradeButtonImage"].get_width() + 40, y=90, single_click=True)
startRoundButton = Button(image=uiImages["startRoundImage"],
                          x=c.SCREEN_WIDTH + 30, y=330, single_click=True)

archerButton = Button(image=turretImages["archerButtonImage"], name="archer",
                      x=c.SCREEN_WIDTH + 30, y=230, single_click=True)
crossbowButton = Button(image=turretImages["crossbowButtonImage"], name="crossbow",
                        x=c.SCREEN_WIDTH + 90, y=230, single_click=True)
wizardButton = Button(image=turretImages["wizardButtonImage"], name="wizard",
                      x=c.SCREEN_WIDTH + 150, y=230, single_click=True)

# game loop
run = True
while run:
    clock.tick(c.FPS)
    screen.fill("grey100")

    # update groups
    enemyGroup.update(world)
    turretGroup.update(enemyGroup)

    # draw level
    world.draw(screen)
    # DrawGrid()
    # draw groups
    enemyGroup.draw(screen)
    for turret in turretGroup:
        turret.draw(screen)

    # button for placing turrets
    turretButton.draw(screen)

    # draw gui
    screen.blit(uiImages["heart"], (0, 0))
    g.DrawText(text=str(world.health),
               screen=screen, style="normal", textColor="grey100",
               x=uiImages["heart"].get_width()*2, y=0)
    screen.blit(uiImages["coin"], (150, 0))
    g.DrawText(text=str(world.money),
               screen=screen, style="normal", textColor="grey100",
               x= 150 + uiImages["coin"].get_width()*2 + len(str(world.money))*5, y=0)

    if levelStarted == False and len(enemyGroup) == 0:
        startRoundButton.draw(screen)
        if startRoundButton.action():
            levelStarted = True
    if levelStarted:
        if pg.time.get_ticks() - lastEnemySpawn > c.SPAWN_COOLDOWN:
            if world.enemiesSpawned < len(world.enemyList):
                enemy_type = world.enemyList[world.enemiesSpawned]
                enemy = Enemy(world.waypoints, enemyImages, enemy_type)
                enemyGroup.add(enemy)
                lastEnemySpawn = pg.time.get_ticks()
                world.enemiesSpawned += 1
            else:
                world.level += 1
                world.money += world.level * 100
                world.ProcessEnemies()
                levelStarted = False
                print("Wave: "+ str(world.level))

    if turretButton.action():
        placing_turrets = True
        if selectedTurret:
            selectedTurret.selected = False
            selectedTurret = None

    # if placing turrets then show the cancel button as well
    if placing_turrets == True:
        g.DisplayButtonWithText(screen=screen, turretButton=archerButton, text="buyCost")
        g.DisplayButtonWithText(screen=screen, turretButton=crossbowButton, text="buyCost")
        g.DisplayButtonWithText(screen=screen, turretButton=wizardButton, text="buyCost")

        cancelButton.draw(screen)

        # show cursor turret
        cursor_rect = turretData["cursorTurretImage"].get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= c.SCREEN_WIDTH:
            screen.blit(turretData["cursorTurretImage"], cursor_rect)
        # button functionality
        if cancelButton.action():
            placing_turrets = False
        if archerButton.action():
            turretData= g.UpdateTurretData("archer")
        if crossbowButton.action():
            turretData= g.UpdateTurretData("crossbow")
        if wizardButton.action():
            turretData= g.UpdateTurretData("wizard")

    if selectedTurret:
        selectedTurret.selected = True

        upgradeButton.name = selectedTurret.turretType
        g.DisplayButtonWithText(turretButton=upgradeButton, screen=screen, text="upgradeCost")

        turretValue = selectedTurret.buyCost + (selectedTurret.upgradeLevel - 1) * selectedTurret.upgradeCost
        g.DisplayButtonWithText(turretButton=sellButton, screen=screen, text="+"+str(turretValue))

        furthestTargetButton.draw(screen)
        strongestTargetButton.draw(screen)

        if upgradeButton.action():
            if selectedTurret.upgradeCost <= world.money:
                upgraded = selectedTurret.Upgrade()
                if upgraded:
                    world.money -= selectedTurret.upgradeCost
        if sellButton.action():  ####
            g.DestroyTurret(world= world, turret=selectedTurret)
            world.money += turretValue
            selectedTurret = None
        if furthestTargetButton.action():
            selectedTurret.ChangeTargeting(targeting="furthest", rangeImageColor="grey100")
        if strongestTargetButton.action():
            selectedTurret.ChangeTargeting(targeting="strongest", rangeImageColor="red")

    # event handler
    for event in pg.event.get():
        try:
            # quit program
            if event.type == pg.QUIT:
                run = False
        except:
            print("scree")
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mousePos = pg.mouse.get_pos()
            # check if mouse is on the game area
            if mousePos[0] < c.SCREEN_WIDTH and mousePos[1] < c.SCREEN_HEIGHT:
                if placing_turrets == True:
                    if world.money >= turretData["turretBuyCost"]:  ####
                        g.CreateTurret(world=world, turretGroup=turretGroup, mouse_pos=mousePos,
                                       turretData=turretData)
                else:
                    selectedTurret = g.SelectTurret(world=world, turretGroup=turretGroup, mouse_pos=mousePos)

    # update display
    pg.display.flip()

pg.quit()
