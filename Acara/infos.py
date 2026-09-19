


buildings = {
        "ground": {"sprite_info": (0, 0, 1, 1), "cost": {}},
        "pump": {"sprite_info": (1, 0, 1, 1), "delay": 5, "cost": {"ore": 100, "iron": 10}, "consumes": {"energy": 1}, "produces": {"water": 1}},
        "farm": {"sprite_info": (2, 0, 2, 1), "delay": 20, "cost": {"ore": 300, "iron": 10}, "consumes": {"water": 2, "energy": 1, "people": 2}, "produces": {"food": 10}},
        "treatment": {"sprite_info": (3, 0, 3, 2), "delay": 5, "cost": {"ore": 600, "iron": 50}, "consumes": {"sewage": 50, "energy": 4, "people": 2}, "produces": {"water": 50}},
        "tent": {"sprite_info": (5, 0, 1, 1), "delay": 1, "cost": {"ore": 100, "iron": 10}, "consumes": {"energy": 1, "sewage": -0.05, "food": 0.05, "water": 0.05}, "produces": {"people": 4}},
        "solar": {"sprite_info": (6, 0, 1, 1), "delay": 1, "cost": {"ore": 20, "iron": 20, "silicon": 50}, "produces": {"energy": 20}},
        "miner": {"sprite_info": (7, 0, 1, 1), "delay": 30, "cost": {"ore": 50, "iron": 50}, "consumes": {"energy": 2, "people": 2}, "produces": {"ore": 50}},
        "bin": {"sprite_info": (8, 0, 1, 1), "delay": 1, "cost": {"ore": 50, "iron": 50}, "storage": {"food": 1000}},
        "tank": {"sprite_info": (9, 0, 1, 1), "delay": 1, "cost": {"ore": 50, "iron": 100}, "storage": {"water": 1000}},
        "resources": {"sprite_info": (10 , 0, 3, 3), "delay": 1, "cost": {"ore": 200, "iron": 100}, "storage": {"ore": 1000, "iron": 1000, "gold": 1000, "silicon": 1000, "uranium": 1000, "diamond": 1000, "chip": 1000, "rocket": 100}},
        "sewage": {"sprite_info": (13 , 0, 1, 1), "delay": 1, "cost": {"ore": 50, "iron": 50}, "storage": {"sewage": 1000}}
    }

resources = {
    "people": (0),
    "water": (1),
    "food": (2),
    "energy": (3),
    "ore": (4),
    "iron": (5),
    "mushroom": (6),
    "coal": (7),
    "sewage": (8),
    "steel": (9),
    "gold": (10), 
    "silicon": (11),
    "hydrogen": (12), 
    "uranium": (13), 
    "diamond": (14), 
    "nuclear": (15), 
    "chip": (16), 
    "rocket": (17), 
    }

resources_flux = set(["energy", "people"])