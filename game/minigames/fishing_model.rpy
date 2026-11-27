# Pure simulation and configuration. No rendering, store writes or wall clock.
# Tests execute this same Python block outside Ren'Py.
init -3 python:
    import math as fishing_math
    import random as fishing_random

    ELL_FISHING_CONFIG = {
        "target": 30, "bait": 3, "max_bait": 5, "hook_x": 760.0,
        "surface": 302.0, "collect_y": 278.0, "min_y": 248.0, "max_y": 965.0,
        "hook_speed": 780.0, "invulnerability": 2.5,
        "legendary_chance": 0.5, "legendary_after": 26,
        "legendary_min_score": 2500, "legendary_duration": 65.0,
        "fish_interval": 1.8, "hazard_interval": 6.5, "bait_interval": 23.0,
    }
    ELL_FISHING_LOCATIONS = {"forest_lake": "Forest Lake"}
    ELL_FISHING_RODS = {
        "wooden": {"name": "Wooden Rod", "description": "A simple, trusty companion.", "speed": 1.0, "resistance": 0.0, "rare": 1.0, "magic": 1.0},
        "reinforced": {"name": "Reinforced Rod", "description": "35% chance to resist a harmful collision.", "speed": 1.0, "resistance": 0.35, "rare": 1.0, "magic": 1.0},
        "silverstream": {"name": "Silverstream Rod", "description": "Moves the hook 25% faster.", "speed": 1.25, "resistance": 0.0, "rare": 1.0, "magic": 1.0},
        "moonlight": {"name": "Moonlight Rod", "description": "Doubles rare fish weights at night.", "speed": 1.05, "resistance": 0.0, "rare": 2.0, "magic": 1.0},
        "foxfire": {"name": "Foxfire Rod", "description": "Doubles magical fish weights.", "speed": 1.05, "resistance": 0.1, "rare": 1.0, "magic": 2.0},
        "yggdrasil": {"name": "Yggdrasil Rod", "description": "An ancient gift: speed, protection and rarer waters.", "speed": 1.3, "resistance": 0.4, "rare": 2.0, "magic": 2.0},
    }

    def ell_fish_spec(name, rarity, weight, speed, depth, size, score, sell, times, description, behaviour="gentle"):
        return dict(name=name, rarity=rarity, weight=weight, speed=speed, depth=depth,
                    size=size, bounds=(size[0] * 0.32, size[1] * 0.30), score=score,
                    sell=sell, times=times, description=description, behaviour=behaviour,
                    locations=("forest_lake",))

    ELL_FISHING_SPECIES = {
        "goldenfin": ell_fish_spec("Goldenfin", "Common", 38, (100, 155), (380, 700), (112, 66), 100, 8, ("day", "twilight", "night"), "A sunny little fish that follows flecks of light through the lake."),
        "silverstream_trout": ell_fish_spec("Silverstream Trout", "Common", 32, (145, 205), (400, 780), (140, 64), 130, 12, ("day", "twilight"), "Quick silver scales flash beneath the waterfall.", "dart"),
        "mossback_carp": ell_fish_spec("Mossback Carp", "Common", 30, (75, 115), (620, 900), (142, 86), 120, 10, ("day", "twilight", "night"), "A patient bottom dweller wearing a coat of moss-green scales."),
        "sunset_koi": ell_fish_spec("Sunset Koi", "Uncommon", 15, (100, 145), (430, 820), (154, 88), 230, 24, ("twilight",), "Amber and rose fins hold the last colours of sunset."),
        "crystal_perch": ell_fish_spec("Crystal Perch", "Uncommon", 12, (120, 170), (500, 900), (128, 82), 260, 28, ("day", "twilight", "night"), "Its translucent fins scatter the light like small crystals.", "magic"),
        "moonfin": ell_fish_spec("Moonfin", "Rare", 11, (100, 150), (420, 810), (144, 86), 450, 55, ("night",), "Moonlight gathers along its crescent fins. Something deep below is listening.", "magic"),
        "foxfire_koi": ell_fish_spec("Foxfire Koi", "Epic", 4, (145, 190), (600, 920), (166, 94), 800, 110, ("night",), "A playful trail of blue flame follows this elusive night swimmer.", "magic"),
        "void_leviathan": ell_fish_spec("Void Leviathan", "Legendary", 0, (85, 85), (650, 840), (450, 210), 6000, 1000, ("special",), "An ancient guardian of the lake's hidden depths. Only a gift of living moonlight draws it near.", "legendary"),
    }
    for _fish_id, _fish_spec in ELL_FISHING_SPECIES.items():
        _fish_spec["id"] = _fish_id
        _fish_spec["art"] = "images/minigames/fishing/fish/" + _fish_id + ".png"
        _fish_spec["silhouette"] = "images/minigames/fishing/silhouettes/" + _fish_id + ".png"

    ELL_FISHING_HAZARDS = {
        "boot": {"name": "Old Boot", "after": 4, "effect": "drop", "size": (100, 100), "speed": 125, "help": "Knocks a hooked fish loose."},
        "branch": {"name": "Floating Branch", "after": 6, "effect": "snare", "size": (190, 68), "speed": 105, "help": "Snags your line for a moment."},
        "crab": {"name": "Crab", "after": 8, "effect": "bait", "size": (112, 86), "speed": 130, "help": "Snips away one bait life."},
        "weeds": {"name": "Water Weeds", "after": 10, "effect": "slow", "size": (100, 155), "speed": 80, "help": "Slows the hook temporarily."},
        "pike": {"name": "Predatory Pike", "after": 14, "effect": "drop", "size": (205, 78), "speed": 210, "help": "Steals the fish on your hook."},
        "eel": {"name": "Electric Eel", "after": 18, "effect": "bait", "size": (200, 75), "speed": 170, "help": "A shock costs one bait life."},
        "wisp": {"name": "Void Wisp", "after": 20, "effect": "reverse", "size": (90, 110), "speed": 115, "help": "Night only: reverses vertical controls briefly."},
    }

    def ell_fishing_swept_hit(ax, ay, bx, by, rx, ry):
        # Segment against a unit ellipse, using relative motion for both bodies.
        ax, ay, bx, by = ax / rx, ay / ry, bx / rx, by / ry
        dx, dy = bx - ax, by - ay
        length = dx * dx + dy * dy
        t = max(0.0, min(1.0, -(ax * dx + ay * dy) / length)) if length else 0.0
        return (ax + t * dx) ** 2 + (ay + t * dy) ** 2 <= 1.0

    class EllFishingModel(object):
        def __init__(self, period="day", rod="wooden", seed=None, config=None):
            self.config = dict(ELL_FISHING_CONFIG)
            if config:
                self.config.update(config)
            self.period = period
            self.rod_id = rod if rod in ELL_FISHING_RODS else "wooden"
            self.rod = ELL_FISHING_RODS[self.rod_id]
            self.rng = fishing_random.Random(seed)
            self.entities = []
            self.effects = []
            self.hook_y = 390.0
            self.mouse_y = self.hook_y
            self.hooked = None
            self.bait = self.config["bait"]
            self.catches = {}
            self.score = self.streak = self.longest_streak = 0
            self.elapsed = self.accumulator = 0.0
            self.invulnerable = self.slow = self.snare = self.reverse = 0.0
            self.fish_clock, self.hazard_clock, self.bait_clock = 0.4, 10.0, 16.0
            self.paused = False
            self.finished = False
            self.reason = ""
            self.encounter = None
            self.encounter_checked = False
            self.encounter_time = 0.0
            self.legend_caught = False
            self.notice = "Move your mouse down to lower the hook."
            self.notice_time = 5.0
            self.events = []

        @property
        def caught(self):
            return sum(self.catches.values())

        @property
        def difficulty(self):
            return min(1.0, self.caught / float(self.config["target"]))

        @property
        def multiplier(self):
            return 1 + min(4, self.streak // 5)

        def tell(self, text, event=None):
            self.notice, self.notice_time = text, 3.5
            if event:
                self.events.append(event)

        def eligible(self):
            return [key for key, spec in ELL_FISHING_SPECIES.items() if self.period in spec["times"] and spec["weight"] > 0]

        def choose_fish(self):
            weighted = []
            for key in self.eligible():
                spec = ELL_FISHING_SPECIES[key]
                weight = spec["weight"]
                if self.period == "night" and spec["rarity"] in ("Rare", "Epic"):
                    weight *= self.rod["rare"]
                if spec["behaviour"] == "magic":
                    weight *= self.rod["magic"]
                weighted.append((key, weight))
            point = self.rng.random() * sum(weight for key, weight in weighted)
            for key, weight in weighted:
                point -= weight
                if point <= 0:
                    return key
            return weighted[-1][0]

        def spawn(self, kind="fish", species=None):
            if kind == "fish":
                species = species or self.choose_fish()
                spec = ELL_FISHING_SPECIES[species]
                width, height = spec["size"]
                depth = self.rng.uniform(*spec["depth"])
                speed = self.rng.uniform(*spec["speed"]) * (1.0 + self.difficulty * 0.35)
            elif kind == "hazard":
                available = [k for k, v in ELL_FISHING_HAZARDS.items() if self.caught >= v["after"] and (k != "wisp" or self.period == "night")]
                if not available:
                    return None
                species = species or self.rng.choice(available)
                spec = ELL_FISHING_HAZARDS[species]
                width, height = spec["size"]
                depth = self.rng.uniform(420, 890)
                speed = spec["speed"] * (1.0 + self.difficulty * 0.25)
            else:
                species, width, height, depth, speed = "bait", 60, 64, self.rng.uniform(450, 820), 115
            direction = self.rng.choice((-1, 1))
            entity = dict(kind=kind, id=species, x=-width if direction == 1 else 1920 + width,
                          y=depth, base_y=depth, direction=direction, speed=speed,
                          width=width, height=height, phase=self.rng.random() * 6.28)
            self.entities.append(entity)
            return entity

        def lose_fish(self):
            self.hooked = None
            self.streak = 0

        def hazard_hit(self, entity):
            if self.invulnerable > 0:
                return
            spec = ELL_FISHING_HAZARDS[entity["id"]]
            if self.rng.random() < self.rod["resistance"]:
                self.invulnerable = 1.0
                self.tell("Your rod held firm!", "resist")
                return
            effect = spec["effect"]
            if effect == "bait":
                self.bait -= 1
                self.lose_fish()
                self.invulnerable = self.config["invulnerability"]
                self.tell(spec["name"] + "! One bait lost.", "hurt")
                if self.bait <= 0:
                    self.finish("no_bait")
            elif effect == "drop":
                if self.hooked:
                    self.lose_fish()
                    self.invulnerable = 0.8
                    self.tell(spec["name"] + "! Your fish slipped away.", "hurt")
            elif effect == "snare":
                self.snare = 0.8
                self.slow = 2.5
                self.tell("The branch snagged your line!", "snag")
            elif effect == "slow":
                self.slow = 3.0
                self.tell("Tangled in weeds. Keep reeling!", "snag")
            else:
                self.reverse = 4.0
                self.tell("Void magic! Controls reversed for four seconds.", "snag")

        def collect(self):
            fish_id = self.hooked
            if not fish_id:
                return
            spec = ELL_FISHING_SPECIES[fish_id]
            self.streak += 1
            self.longest_streak = max(self.longest_streak, self.streak)
            points = spec["score"] * self.multiplier
            self.score += points
            self.catches[fish_id] = self.catches.get(fish_id, 0) + 1
            self.hooked = None
            self.effects.append({"y": self.config["surface"], "age": 0.0, "points": points})
            self.tell("{}  +{}".format(spec["name"], points), "rare" if spec["rarity"] in ("Rare", "Epic", "Legendary") else "catch")
            if fish_id == "void_leviathan":
                self.legend_caught = True
                self.end_encounter()
            self.check_encounter()
            if self.caught >= self.config["target"] and not self.encounter:
                self.finish("target")

        def check_encounter(self):
            if self.encounter_checked or self.period != "night" or self.caught < self.config["legendary_after"]:
                return
            self.encounter_checked = True
            if self.score < self.config["legendary_min_score"] or self.rng.random() >= self.config["legendary_chance"]:
                return
            self.encounter = "omen"
            self.encounter_time = 0.0
            self.entities = []
            self.hazard_clock = 9.0
            self.tell("The deep water stirs... Keep a Moonfin on your hook.", "omen")

        def end_encounter(self):
            self.encounter = None
            self.entities = []
            self.fish_clock = 0.2
            if self.hooked == "void_leviathan":
                self.hooked = None
            if self.caught >= self.config["target"]:
                self.finish("target")

        def finish(self, reason):
            self.finished = True
            self.reason = reason

        def update(self, dt):
            if self.paused or self.finished:
                return
            # Fixed simulation steps make swept collisions and spawn clocks stable.
            self.accumulator += max(0.0, min(0.25, dt))
            step = 1.0 / 120.0
            while self.accumulator + 1e-9 >= step and not self.finished:
                self.accumulator -= step
                self.step(step)

        def step(self, dt):
            self.elapsed += dt
            for name in ("invulnerable", "slow", "snare", "reverse", "notice_time"):
                setattr(self, name, max(0.0, getattr(self, name) - dt))
            for effect in self.effects:
                effect["age"] += dt
            self.effects = [e for e in self.effects if e["age"] < 1.2]
            old_y = self.hook_y
            target = self.mouse_y
            if self.reverse:
                target = self.config["min_y"] + self.config["max_y"] - target
            target = max(self.config["min_y"], min(self.config["max_y"], target))
            speed = self.config["hook_speed"] * self.rod["speed"] * (0.36 if self.slow else 1.0)
            if not self.snare:
                self.hook_y += max(-speed * dt, min(speed * dt, target - self.hook_y))
            if self.hooked and self.hook_y <= self.config["collect_y"]:
                self.collect()
            if self.finished:
                return
            self.fish_clock -= dt
            self.hazard_clock -= dt
            self.bait_clock -= dt
            if self.encounter:
                self.encounter_time += dt
                if self.encounter == "omen" and self.encounter_time >= 4.0:
                    self.encounter = "visible"
                    self.spawn("fish", "void_leviathan")
                    self.tell("Offer a hooked Moonfin to the guardian of the deep.")
                if self.encounter_time >= self.config["legendary_duration"]:
                    self.end_encounter()
                    self.tell("The guardian slips back into the deep.")
                elif self.fish_clock <= 0 and self.hooked != "void_leviathan":
                    if not any(e["id"] == "moonfin" for e in self.entities):
                        self.spawn("fish", "moonfin")
                    self.fish_clock = 4.0
                if self.encounter == "visible" and self.hooked != "void_leviathan" and not any(e["id"] == "void_leviathan" for e in self.entities):
                    self.spawn("fish", "void_leviathan")
            elif self.fish_clock <= 0:
                self.spawn()
                self.fish_clock += self.config["fish_interval"] - self.difficulty * 0.8
            if not self.encounter and self.hazard_clock <= 0:
                if len([e for e in self.entities if e["kind"] == "hazard"]) < 3:
                    self.spawn("hazard")
                self.hazard_clock = self.config["hazard_interval"] - self.difficulty * 2.0
            if self.bait_clock <= 0:
                if self.bait < self.config["max_bait"]:
                    self.spawn("bait")
                self.bait_clock = self.config["bait_interval"]
            remaining = []
            for entity in self.entities:
                old_x, entity_old_y = entity["x"], entity["y"]
                entity["x"] += entity["direction"] * entity["speed"] * dt
                entity["y"] = entity["base_y"] + fishing_math.sin(self.elapsed * 1.8 + entity["phase"]) * 9
                if entity["x"] < -550 or entity["x"] > 2470:
                    continue
                hook_x = self.config["hook_x"]
                if entity["kind"] == "fish":
                    rx, ry = ELL_FISHING_SPECIES[entity["id"]]["bounds"]
                else:
                    rx, ry = entity["width"] * 0.34, entity["height"] * 0.34
                # Attached fish increases the hazard contact area.
                if self.hooked and entity["kind"] == "hazard":
                    rx += 24
                    ry += 18
                hit = self.hook_y > self.config["surface"] + 16 and ell_fishing_swept_hit(
                    hook_x - old_x, old_y - entity_old_y,
                    hook_x - entity["x"], self.hook_y - entity["y"], rx + 12, ry + 12)
                consumed = False
                if hit and entity["kind"] == "fish":
                    fish_id = entity["id"]
                    if fish_id == "void_leviathan":
                        if self.hooked == "moonfin":
                            self.hooked = fish_id
                            consumed = True
                            self.tell("The Leviathan took the Moonfin! Reel it above the water!", "rare")
                        elif not self.hooked and self.notice_time < 1.0:
                            self.tell("Ordinary bait cannot tempt the guardian. Find a Moonfin.")
                    elif self.hooked is None:
                        self.hooked = fish_id
                        consumed = True
                        self.tell("{} hooked! Raise it above the water.".format(ELL_FISHING_SPECIES[fish_id]["name"]), "hook")
                elif hit and entity["kind"] == "bait":
                    self.bait = min(self.config["max_bait"], self.bait + 1)
                    self.tell("Fresh bait!", "bait")
                    consumed = True
                elif hit and entity["kind"] == "hazard" and not self.invulnerable:
                    self.hazard_hit(entity)
                    consumed = True
                if not consumed:
                    remaining.append(entity)
                if self.finished:
                    break
            self.entities = remaining

        def result(self):
            return {"minigame_id": "forest_fishing", "status": "abandoned" if self.reason == "abandoned" else "completed",
                    "reason": self.reason, "period": self.period, "rod": self.rod_id,
                    "location": "forest_lake", "catches": dict(self.catches), "caught": self.caught,
                    "score": self.score, "longest_streak": self.longest_streak,
                    "rare_caught": sum(n for key, n in self.catches.items() if ELL_FISHING_SPECIES[key]["rarity"] in ("Rare", "Epic", "Legendary")),
                    "legendary": self.legend_caught, "elapsed_seconds": int(self.elapsed)}
