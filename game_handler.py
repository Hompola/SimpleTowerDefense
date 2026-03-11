import pygame as pg
import json
import turret_data
from world import World
import constants as c
from turret import Turret
from wizard import Wizard

turrets = turret_data.TURRET_DATA

def SetupWorld(pathFile, mapImage):
    # load json data for level
    with open(pathFile) as file:
        world_data = json.load(file)

    # create world
    world = World(world_data, mapImage)
    world.Process_data()
    world.ProcessWaypoints()
    world.ProcessEnemies()
    return world

def DrawText(screen, text, style, textColor, x, y):
    font = pg.font.SysFont("Consolas", 36)
    if style == "large":
        font = pg.font.SysFont("Consolas", 36, bold=True)
    elif style == "small":
        font = pg.font.SysFont("Consolas", 12, bold=False)

    img = font.render(text, True, textColor)
    screen.blit(img, (x-img.get_width()/2, y))
    return img.get_width()


def DrawGrid(screen):
    for col in range(c.COLS):
        pg.draw.line(screen, "black", (col * c.TILE_SIZE, 0), (col * c.TILE_SIZE, c.SCREEN_HEIGHT))
        pg.draw.line(screen, "black", (0, col * c.TILE_SIZE), (c.SCREEN_HEIGHT, col * c.TILE_SIZE))


def CreateTurret(world, mouse_pos, turretGroup, turretData):
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
            turretType = turretData["turretType"]
            turretSheet = turretData["turretSheet"]
            turretBuyCost = turretData["turretBuyCost"]
            if turretType == "wizard":  ####
                newTurret = Wizard(turretSheet, row, col, turretType)
            else:
                newTurret = Turret(turretSheet, row, col, turretType)
            turretGroup.add(newTurret)
            world.tilemap[row][col] = 2
            world.money -= turretBuyCost

def SelectTurret(world, mouse_pos, turretGroup):
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


def DestroyTurret(world, turret):  ####
    row = turret.tileY
    col = turret.tileX
    turret.kill()
    world.tilemap[row][col] = 0


def LoadTurretData(turretType):
    turretSheet_loc = turret_data.TURRET_DATA.get(turretType).get("animSheet")
    cursorTurretImage_loc = turret_data.TURRET_DATA.get(turretType).get("cursorImage")
    turretSheet = pg.image.load(turretSheet_loc).convert_alpha()
    cursorTurretImage = pg.image.load(cursorTurretImage_loc).convert_alpha()
    turretBuyCost = turret_data.TURRET_DATA.get(turretType).get("buyCost")
    return turretSheet, cursorTurretImage, turretBuyCost

def UpdateTurretData(turretType):
    turretSheet, cursorTurretImage, turretBuyCost = LoadTurretData(turretType)
    turretData={
                "turretType":turretType,
                "turretSheet": turretSheet,
                "cursorTurretImage": cursorTurretImage,
                "turretBuyCost": turretBuyCost}
    return turretData
def DisplayButtonWithText(screen, turretButton, text):
    turretButton.draw(screen)
    if turretButton.name!=None:
        turretText = str(turrets[turretButton.name][text])
    else:
        turretText = text
    DrawText(text=turretText,
             screen=screen, style="small", textColor="grey0",
             x=turretButton.posX+turretButton.image.get_width()/2,
             y=turretButton.posY+turretButton.image.get_height()+10)
