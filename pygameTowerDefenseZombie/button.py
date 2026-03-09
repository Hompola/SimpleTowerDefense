
import pygame as pg




class Button:
    def __init__(self, x, y, image, singleClick):
        self.clicked=False
        self.x = x
        self.y = y
        self.image = image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.singleClick = singleClick

    def Draw(self, screen):
        screen.blit(self.image,self.rect)

    @property
    def Pressed(self):
        buttonPressed=False
        pos=pg.mouse.get_pos()

        if self.rect.collidepoint(pos):
            #print("nuke is launching if you press!")
            if pg.mouse.get_pressed()[0] and self.clicked==False:
                #print("nuke is launching in ten seconds")
                buttonPressed=True
                if self.singleClick:
                    self.clicked=True
                    #print("yay")
        if pg.mouse.get_pressed()[0]:
            self.clicked=False
        return buttonPressed