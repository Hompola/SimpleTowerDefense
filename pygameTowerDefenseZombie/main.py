#imports
import select

import pygame as pg
import json
import constants as con
from constants import tileSize, sidebarWidth, screenHeight, screenWidth
from enemy import Enemy
from world import World
from towersOrTroopsOrSoldiers import Tower
from button import Button

##############################################################################################################################################################################################################################################################################################3
#game variables
selectedTower = None
placingTower = False

#initialises pygame and clocks
pg.init()
clock = pg.time.Clock()

#create gaming window
screen = pg.display.set_mode((con.screenWidth + sidebarWidth, con.screenHeight))

pg.display.set_caption("Tower Defense")

#loading images.......
worldImage = pg.image.load("assets/Levels/custom_level_720_v2.png")
enemyImage = pg.image.load("assets/images/enemies/enemy_1.png").convert_alpha()
turretImage = pg.image.load("assets/images/Towers/ArcherUnitv2_75px_cursor.png").convert_alpha()
buttonImage = pg.image.load("assets/images/shop/buyTurret.png").convert_alpha()
cancelImage = pg.image.load("assets/images/shop/cancel.png").convert_alpha()
turretSpreadsheet = pg.image.load('assets/images/Towers/ArcherUnitv2_75px.png').convert_alpha()

#loading path......
with open("assets/levels/custom_path2.json") as file:
    worldData = json.load(file)
    print(worldData)

#loading world.....
#if you know you know
world = World(worldImage, worldData)
world.ExtractData()
world.TileMap()
waypoints = world.waypoints

#setting up group
enemyGroup = pg.sprite.Group()
towerGroup = pg.sprite.Group()

enemy = Enemy(waypoints, enemyImage)
enemyGroup.add(enemy)

#setting up buttons
towerButton = Button(con.screenWidth + sidebarWidth / 2, screenHeight / 2, buttonImage, False)
cancelButton = Button(con.screenWidth + sidebarWidth / 2, screenHeight / 2 - 100, cancelImage, False)


def Grid():
    for col in range(0, int(con.COLS)):
        lineStart = (col * con.tileSize, 0)
        lineEnd = (col * con.tileSize, con.screenHeight)
        pg.draw.line(screen, "navy", lineStart, lineEnd)
    for row in range(0, int(con.ROWS)):
        lineStart = (0, row * con.tileSize)
        lineEnd = (con.screenWidth, row * con.tileSize)
        pg.draw.line(screen, "navy", lineStart, lineEnd)


def CreateTower(mousePos):
    col = int(mousePos[0] / tileSize)
    row = int(mousePos[1] / tileSize)
    if world.tileMap[row][col] == 0:
        spaceIsFree = True
        for tower in towerGroup:
            #print("tower is placed")
            if (row, col) == (tower.row, tower.column):
                spaceIsFree = False
        if spaceIsFree == True:
            #print("run zombie run!")
            # reference to movie forrest gump above
            newTower = Tower(turretSpreadsheet, col, row)
            towerGroup.add(newTower)
            world.tileMap[row][col] = 42


def SelectTower(mousePos):
    col = int(mousePos[0] / tileSize)
    row = int(mousePos[1] / tileSize)
    for tower in towerGroup:
        print(row,col)
        print(tower.row,tower.column)
        if (row, col) == (tower.row, tower.column):
            return tower


run = True
while run:
    clock.tick(con.fps)
    screen.fill("gray50")
    screen.blit(worldImage, (0, 0))
    pg.draw.lines(screen, "crimson", False, waypoints)

    if selectedTower:
        selectedTower.selected = True

    enemyGroup.update()
    towerGroup.update(enemyGroup,screen)
    enemyGroup.draw(screen)
    enemy.move()

    for tower in towerGroup:
        tower.draw(screen)
    Grid()

    towerButton.Draw(screen)

    if towerButton.Pressed:
        #print("hmmm")
        placingTower = True
    if placingTower:
        #print("run zombie run!")
        cancelButton.Draw(screen)
        cursorRect = turretImage.get_rect()
        cursorPos = pg.mouse.get_pos()
        cursorRect.center = cursorPos
        screen.blit(turretImage, cursorRect)
        if cancelButton.Pressed:
            #print("bye bye tower")
            placingTower = False

    #eventListener
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mousePos = pg.mouse.get_pos()
            if mousePos[0] <= screenWidth and mousePos[1]<=screenHeight:
                if placingTower:
                    CreateTower(mousePos)
                else:
                    print("yo ho ho")
                    SelectTower(mousePos)
                    selectedTower = SelectTower(mousePos)
        if event.type == pg.QUIT:
            run = False

    pg.display.flip()

pg.quit()
