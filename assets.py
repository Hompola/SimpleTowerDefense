import pygame as pg
from button import Button
import constants as c

def LoadImages():
    images = {}
    images["mapImage"] = pg.image.load('levels/custom_level_720_v2.png').convert_alpha()

    images["enemies"] = {
        "normal": pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
        "fast": pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(),
        "tank": pg.image.load('assets/images/enemies/enemy_3.png').convert_alpha(),
        "elite": pg.image.load('assets/images/enemies/Zomboss(Custom).png').convert_alpha()
    }

    images["ui"] = {
        "upgradeButtonImage": pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha(),
        "furthestTargetImage" : pg.image.load('assets/images/buttons/furthestTarget_button_50px.png').convert_alpha(),
        "strongestTargetImage" : pg.image.load('assets/images/buttons/strongestTarget_button_50px.png').convert_alpha(),
        "buyTurretImage" : pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha(),
        "cancelImage" : pg.image.load('assets/images/buttons/cancel.png').convert_alpha(),
        "sellImage" : pg.image.load('assets/images/buttons/sell_50px.png').convert_alpha(),
        "heart" : pg.image.load('assets/images/gui/heart.png').convert_alpha(),
        "coin" : pg.image.load('assets/images/gui/coin.png').convert_alpha(),
        "startRoundImage" : pg.image.load('assets/images/buttons/begin.png').convert_alpha()
    }

    images["turrets"] = {
        "archerButtonImage" : pg.image.load('assets/images/buttons/archer_button50px.png').convert_alpha(),
        "crossbowButtonImage" : pg.image.load('assets/images/buttons/crossbow_button50px.png').convert_alpha(),
        "wizardButtonImage" : pg.image.load('assets/images/buttons/wizard_button50px.png').convert_alpha()
    }
    return images

