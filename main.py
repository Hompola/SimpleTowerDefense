import pygame as pg
import json

import turret_data
from enemy import Enemy
from world import World
from turret import Turret
from wizard import Wizard
import constants as c
from button import Button

# initialise pygame
pg.init()

# Game variables
placing_turrets = False
selected_turret = None
placingTypeOfTurret = "archer"
turretBuyCost = turret_data.TURRET_DATA.get("archer").get("buyCost")

lastEnemySpawn = pg.time.get_ticks()
levelStarted = False

# create clock
clock = pg.time.Clock()

# create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDEBAR_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

# load images

# map
mapImage = pg.image.load('levels/custom_level_720_v2.png').convert_alpha()
# enemies
enemyImages = {
    "normal": pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
    "fast": pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(),
    "tank": pg.image.load('assets/images/enemies/enemy_3.png').convert_alpha(),
    "elite": pg.image.load('assets/images/enemies/Zomboss(Custom).png').convert_alpha()
}

turretSheet = pg.image.load('assets/images/turrets/ArcherUnit_75px.png').convert_alpha()
cursorTurretImage = pg.image.load('assets/images/turrets/ArcherUnit_75px_cursor.png').convert_alpha()
# shop buttons ####
upgradeButtonImage = pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()
furthestTargetImage = pg.image.load('assets/images/buttons/furthestTarget_button_50px.png').convert_alpha()
thoughestTargetImage = pg.image.load('assets/images/buttons/thoughestTarget_button_50px.png').convert_alpha()

buyTurretImage = pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancelImage = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
sellImage = pg.image.load('assets/images/buttons/sell_50px.png').convert_alpha()  ####
archerButtonImage = pg.image.load('assets/images/buttons/archer_button50px.png').convert_alpha()
crossbowButtonImage = pg.image.load('assets/images/buttons/crossbow_button50px.png').convert_alpha()
wizardButtonImage = pg.image.load('assets/images/buttons/wizard_button50px.png').convert_alpha()  ####

startRoundImage = pg.image.load('assets/images/buttons/begin.png').convert_alpha()
# gui
heart = pg.image.load('assets/images/gui/heart.png').convert_alpha()
coin = pg.image.load('assets/images/gui/coin.png').convert_alpha()

# create buttons
upgradeButton = Button(c.SCREEN_WIDTH + 30, 30, upgradeButtonImage, True)
furthestTargetButton = Button(c.SCREEN_WIDTH + 30, 90, furthestTargetImage, True)
thoughestTargetButton = Button(c.SCREEN_WIDTH + 90, 90, thoughestTargetImage, True)
turretButton = Button(c.SCREEN_WIDTH + 30, 170, buyTurretImage, True)
cancelButton = Button(c.SCREEN_WIDTH + buyTurretImage.get_width() + 40, 170, cancelImage, True)
sellButton = Button(c.SCREEN_WIDTH + buyTurretImage.get_width() + 40, 170, sellImage, True)  ####
archerButton = Button(c.SCREEN_WIDTH + 30, 230, archerButtonImage, True)
crossbowButton = Button(c.SCREEN_WIDTH + 90, 230, crossbowButtonImage, True)
wizardButton = Button(c.SCREEN_WIDTH + 150, 230, wizardButtonImage, True)  ####
startRoundButton = Button(c.SCREEN_WIDTH + 30, 330, startRoundImage, True)

# load json data for level
with open('levels/custom_level_720.json') as file:
    world_data = json.load(file)

# create world
world = World(world_data, mapImage)
world.Process_data()
world.ProcessWaypoints()
world.ProcessEnemies()

# create empty groups
enemyGroup = pg.sprite.Group()
turretGroup = pg.sprite.Group()


def DrawText(text, style, textColor, x, y):
    font = pg.font.SysFont("Consolas", 36)
    if style == "large":
        font = pg.font.SysFont("Consolas", 36, bold=True)
    elif style == "small":
        font = pg.font.SysFont("Consolas", 12, bold=False)

    img = font.render(text, True, textColor)
    screen.blit(img, (x, y))
    return img.get_width()


def DrawGrid():
    for col in range(c.COLS):
        pg.draw.line(screen, "black", (col * c.TILE_SIZE, 0), (col * c.TILE_SIZE, c.SCREEN_HEIGHT))
        pg.draw.line(screen, "black", (0, col * c.TILE_SIZE), (c.SCREEN_HEIGHT, col * c.TILE_SIZE))


def CreateTurret(mouse_pos, turretType):
    col = int(mouse_pos[0] // c.TILE_SIZE)
    row = int(mouse_pos[1] // c.TILE_SIZE)
    if row < 0 or row >= len(world.tilemap):
        return
    if col < 0 or col >= len(world.tilemap[0]):
        return
    # check if that tile is grass
    if world.tilemap[row][col] == 0:
        # check that there isn't already a turret there
        space_is_free = True
        for turret in turretGroup:
            if (row, col) == (turret.tileY, turret.tileX):
                space_is_free = False
        # if it is a free space then create turret
        if space_is_free == True:
            if turretType == "wizard":  ####
                newTurret = Wizard(turretSheet, row, col, turretType)
            else:
                newTurret = Turret(turretSheet, row, col, turretType)
            turretGroup.add(newTurret)
            world.tilemap[row][col] = 2
            world.money -= turretBuyCost
            """print(row,col)
      for i in world.tilemap:
        print(i)
      print("\n")"""


def selectTurret(mouse_pos):
    selected = None
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    if 0 <= mouse_tile_y < len(world.tilemap) and 0 <= mouse_tile_x < len(world.tilemap[0]):
        for turret in turretGroup:
            turret.selected = False
            if (mouse_tile_x, mouse_tile_y) == (turret.tileX, turret.tileY):
                turret.selected = True
                selected = turret
    return selected


def DestroyTurret(turret):  ####
    row = turret.tileY
    col = turret.tileX
    turret.kill()
    world.tilemap[row][col] = 0


def LoadTurretData(turretType):
    global turretClass
    global turretSheet
    global cursorTurretImage
    turretSheet_loc = turret_data.TURRET_DATA.get(turretType).get("animSheet")
    cursorTurretImage_loc = turret_data.TURRET_DATA.get(turretType).get("cursorImage")
    turretSheet = pg.image.load(turretSheet_loc).convert_alpha()
    cursorTurretImage = pg.image.load(cursorTurretImage_loc).convert_alpha()
    turretBuyCost = turret_data.TURRET_DATA.get(turretType).get("buyCost")
    return turretSheet, cursorTurretImage, turretBuyCost


# game loop
run = True
while run:
    clock.tick(c.FPS)

    screen.fill("grey100")

    # draw level
    world.draw(screen)
    # DrawGrid()

    # update groups
    enemyGroup.update(world)
    turretGroup.update(enemyGroup)

    # draw groups
    enemyGroup.draw(screen)
    for turret in turretGroup:
        turret.draw(screen)

    # draw buttons
    # button for placing turrets
    turretButton.draw(screen)

    # draw gui
    screen.blit(heart, (0, 0))
    DrawText(str(world.health), "normal", "grey100", heart.get_width(), 0)
    screen.blit(coin, (150, 0))
    DrawText(str(world.money), "normal", "grey100", 150 + coin.get_width(), 0)

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
                print(world.level)

    if turretButton.action():
        placing_turrets = True
        if selected_turret:  ####
            selected_turret.selected = False
            selected_turret = None
    # if placing turrets then show the cancel button as well
    if placing_turrets == True:
        archerButton.draw(screen)
        archerCost = turret_data.TURRET_DATA.get("archer").get("buyCost")
        DrawText(str(archerCost), "small", "grey0", c.SCREEN_WIDTH + 30 + 12, 290)
        crossbowButton.draw(screen)
        crossbowCost = turret_data.TURRET_DATA.get("crossbow").get("buyCost")
        DrawText(str(crossbowCost), "small", "grey0", c.SCREEN_WIDTH + 90 + 12, 290)
        wizardButton.draw(screen)  ####
        wizardCost = turret_data.TURRET_DATA.get("wizard").get("buyCost")  ####
        DrawText(str(wizardCost), "small", "grey0", c.SCREEN_WIDTH + 150 + 12, 290)  ####
        cancelButton.draw(screen)
        # show cursor turret
        cursor_rect = cursorTurretImage.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= c.SCREEN_WIDTH:
            screen.blit(cursorTurretImage, cursor_rect)
        if cancelButton.action():
            placing_turrets = False
        if archerButton.action():  ####
            LoadTurretData("archer")
            placingTypeOfTurret = "archer"
        if crossbowButton.action():  ####
            LoadTurretData("crossbow")
            placingTypeOfTurret = "crossbow"
        if wizardButton.action():  ####
            LoadTurretData("wizard")
            placingTypeOfTurret = "wizard"

    if selected_turret:
        selected_turret.selected = True
        upgradeButton.draw(screen)
        upgradeCost = turret_data.TURRET_DATA.get(selected_turret.turretType).get("upgradeCost")
        DrawText(str(upgradeCost), "small", "grey0", c.SCREEN_WIDTH + upgradeButtonImage.get_width() + 30, 30)
        sellButton.draw(screen)
        BuyCost = turret_data.TURRET_DATA.get(selected_turret.turretType).get("buyCost")
        turretValue = BuyCost + (selected_turret.upgradeLevel - 1) * upgradeCost
        DrawText("+" + str(turretValue), "small", "grey0", c.SCREEN_WIDTH + buyTurretImage.get_width() + 40, 230)
        furthestTargetButton.draw(screen)
        thoughestTargetButton.draw(screen)
        if upgradeButton.action():
            if selected_turret.upgradeCost <= world.money:
                upgraded = selected_turret.Upgrade()
                if upgraded:
                    world.money -= selected_turret.upgradeCost
                    DrawText("+" + str(turretValue), "small", "grey0", c.SCREEN_WIDTH + buyTurretImage.get_width() + 40,
                             230)
        if furthestTargetButton.action():
            selected_turret.targeting = "furthest"
            selected_turret.UpdateRangeImage("grey100")
        if thoughestTargetButton.action():
            selected_turret.targeting = "thoughest"
            selected_turret.UpdateRangeImage("red")
        if sellButton.action():  ####
            DestroyTurret(selected_turret)
            world.money += turretValue
            selected_turret = None

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
                    if world.money >= turretBuyCost:  ####
                        CreateTurret(mousePos, placingTypeOfTurret)
                else:
                    selected_turret = selectTurret(mousePos)

    # update display
    pg.display.flip()

pg.quit()