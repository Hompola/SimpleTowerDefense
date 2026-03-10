TURRET_DATA = {
    "archer": {
        "animSheet":'assets/images/turrets/ArcherUnit_75px.png',
        "cursorImage": 'assets/images/turrets/ArcherUnit_75px_cursor.png',
        "buyCost": 100,
        "upgradeCost": 50,
        "maxLevel":4,
        1: {
            # 1
            "range": 90,
            "cooldown": 1500,
            "damage": 3
        },
        2: {
            # 2
            "range": 110,
            "cooldown": 1200,
            "damage": 4
        },
        3: {
            # 3
            "range": 125,
            "cooldown": 1000,
            "damage": 5
        },
        4: {
            # 4
            "range": 150,
            "cooldown": 900,
            "damage": 6
        }},
    "crossbow": {
            "animSheet":'assets/images/turrets/CrossbowUnit75px.png', ####
            "cursorImage":'assets/images/turrets/CrossbowUnit_75px_cursor.png', ####
            "buyCost": 150,
            "upgradeCost": 100,
            "maxLevel":4,
            1: {
                # 1
                "range": 180,
                "cooldown": 3000,
                "damage" : 10
            },
            2: {
                # 2
                "range": 220,
                "cooldown": 2400,
                "damage" : 12
            },
            3: {
                # 3
                "range": 270,
                "cooldown": 2200,
                "damage" : 14
            },
            4: {
                # 4
                "range": 330,
                "cooldown": 2000,
                "damage" : 15
            }},
    "wizard": {
            "animSheet":'assets/images/turrets/WizardUnit_75px.png', ####
            "cursorImage":'assets/images/turrets/WizardUnit_75px_cursor.png', ####
            "buyCost": 150,
            "upgradeCost": 100,
            "maxLevel":4,
            1: {
                # 1
                "range": 110,
                "cooldown": 3000,
                "damage" : 3
            },
            2: {
                # 2
                "range": 130,
                "cooldown": 2400,
                "damage" : 4
            },
            3: {
                # 3
                "range": 150,
                "cooldown": 2200,
                "damage" : 5
            },
            4: {
                # 4
                "range": 180,
                "cooldown": 2000,
                "damage" : 5
            }}
}
