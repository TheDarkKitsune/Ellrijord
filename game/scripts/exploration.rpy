# Shared, saveable exploration state. The clock advances through activities,
# not wall time. Schedules, the PC and room occupants all use this same clock.
default ell_world_minutes = 420
default ell_world_location = "bedroom"
default ell_world_unlocked = set(ELL_WORLD_STARTING_LOCATIONS)
default ell_world_visited = set()
default ell_world_conversations = set()
default ell_world_classes = set()
default ell_world_breakfast_day = 0
default ell_world_bulletin_read = False
default ell_world_notice = ""
default ell_world_tutorial_complete = False
default ell_world_tutorial_active = False
default ell_world_tutorial_step = 0
default day2_opening_seen = False
default day2_hana_dream_discussed = False

init -4 python:
    ELL_WORLD_LOCATIONS = {
        "bedroom": {"name": "Your bedroom", "area": "home", "backgrounds": ("gui/maps/bedroom2.png",), "links": ("hallway",)},
        "hallway": {"name": "Home hallway", "area": "home", "backgrounds": ("scenes/Hallway.png",), "links": ("bedroom", "kitchen")},
        "kitchen": {"name": "Kitchen", "area": "home", "backgrounds": ("scenes/Kitchen_open.png",), "links": ("hallway",)},
        "school_gate": {"name": "School gates", "area": "school", "backgrounds": ("scenes/school_gate.png",), "links": ("school_corridor", "courtyard")},
        "school_corridor": {"name": "School corridor", "area": "school", "backgrounds": ("scenes/school_hallway.png",), "links": ("school_gate", "classroom", "courtyard", "library")},
        "classroom": {"name": "Your classroom", "area": "school", "backgrounds": ("scenes/classroom.png",), "links": ("school_corridor",)},
        "courtyard": {"name": "School courtyard", "area": "school", "backgrounds": ("scenes/school_courtyard.png",), "links": ("school_gate", "school_corridor")},
        "library": {"name": "School library", "area": "school", "backgrounds": ("scenes/school_library.png",), "links": ("school_corridor",)},
        "town_centre": {"name": "Town centre", "area": "town", "backgrounds": ("scenes/town_centre.png",), "links": ()},
        "park": {"name": "Riverside park", "area": "park", "backgrounds": ("scenes/park.png",), "links": ()},
        "forest": {"name": "Forest path", "area": "forest", "backgrounds": ("gui/maps/forest_map.png",), "links": ("forest_lake",)},
        "forest_lake": {"name": "Forest Lake", "area": "forest", "backgrounds": ("images/minigames/fishing/backgrounds/day.png",), "links": ("forest",)},
    }
    ELL_WORLD_STARTING_LOCATIONS = tuple(k for k in ELL_WORLD_LOCATIONS if k not in ("library", "park", "forest", "forest_lake"))
    ELL_WORLD_MAP_DESTINATIONS = (
        ("hallway", "Home", 750, 810),
        ("school_gate", "School", 610, 480),
        ("town_centre", "Town centre", 1370, 560),
        ("park", "Riverside park", 290, 330),
        ("forest", "Forest path", 500, 150),
        ("forest_lake", "Forest Lake", 790, 150),
    )
    ELL_WORLD_NPCS = {
        "hana": {"name": "Hana", "portrait": "gui/hud/portraits/Hana.png"},
        "tsuki": {"name": "Tsuki", "portrait": "gui/hud/portraits/tsuki.png"},
        "aria": {"name": "Aria", "portrait": "gui/hud/portraits/Aria.png"},
        "poko": {"name": "Poko", "portrait": "gui/hud/portraits/Poko.png"},
        "mimi": {"name": "Mimi", "portrait": "gui/hud/portraits/Mimi.png"},
        "kuroe": {"name": "Kuroe", "portrait": "gui/hud/portraits/Kuroe.png"},
        "sakura": {"name": "Sakura", "portrait": "gui/hud/portraits/Sakura.png"},
        "rika": {"name": "Rika", "portrait": "gui/hud/portraits/Rika.png"},
    }
    # Half-open intervals avoid characters appearing in two places at a boundary.
    # Students are unavailable while attending their own classes.
    ELL_WORLD_SCHEDULES = {
        "hana": ((420, 540, "kitchen"), (540, 720, "town_centre"), (720, 840, "kitchen"), (840, 1080, "hallway"), (1080, 1260, "kitchen")),
        "tsuki": ((420, 480, "kitchen"), (480, 510, "school_corridor"), (720, 780, "courtyard"), (900, 1080, "hallway"), (1080, 1260, "kitchen")),
        "aria": ((465, 510, "school_gate"), (720, 780, "courtyard"), (900, 1020, "town_centre")),
        "poko": ((465, 510, "courtyard"), (720, 780, "courtyard"), (900, 1020, "courtyard")),
        "mimi": ((465, 510, "school_corridor"), (720, 780, "courtyard"), (900, 1020, "library")),
        "kuroe": ((465, 510, "school_corridor"), (720, 780, "courtyard"), (900, 1020, "park")),
        "sakura": ((465, 510, "courtyard"), (720, 780, "courtyard"), (900, 1020, "town_centre")),
        "rika": ((465, 510, "school_corridor"), (720, 780, "courtyard"), (900, 1020, "school_corridor")),
    }
    ELL_WORLD_TUTORIAL = (
        ("welcome", "Morning! Mini Tsuki reporting for guide duty. I'll show you the useful buttons, then you can explore for yourself."),
        ("map", "The Map button is up there. Open it! You can travel to unlocked places and see which ones are open right now."),
        ("inventory", "Now open your Player Hub. Your inventory, quests, collectibles and character notes are all in there. Come back when you've had a look!"),
        ("pc", "Your PC is on the desk. Click the desk or the PC button to use it. Check the school bulletin while you're there!"),
        ("time", "Keep an eye on the clock. Looking around and opening menus takes no time. Travelling, chatting and other activities do. People move as the day goes on!"),
        ("door", "Try the bedroom door, or the Hallway button below. Rooms in the same area are free to move between."),
        ("finish", "That's it! Use Map to head out, Wait to pass time, and Help if you need me again. Try breakfast with Mum before school. Off you go!"),
    )
    ELL_QUESTS.update({
        "day2_get_your_bearings": {"title": "Find Your Feet", "giver": "Mini Tsuki", "description": "Learn how to use the map, Player Hub and room interactions.", "target": 1, "kind": "story"},
        "day2_school_day": {"title": "Back to Class", "giver": "School", "description": "Complete a school day by attending both morning and afternoon classes.", "target": 2, "kind": "story"},
    })

    def ell_world_clock():
        return "{:02d}:{:02d}".format(ell_world_minutes // 60, ell_world_minutes % 60)

    def ell_world_sync_time():
        renpy.store.ell_time_of_day = (
            "morning" if ell_world_minutes < 720 else
            "midday" if ell_world_minutes < 780 else
            "afternoon" if ell_world_minutes < 1080 else
            "evening" if ell_world_minutes < 1260 else "night"
        )

    def ell_world_map_art():
        suffix = "night" if ell_world_minutes >= 1260 else "twilight" if ell_world_minutes >= 1080 else "day"
        return "gui/maps/main_map_{}.png".format(suffix)

    def ell_world_background(location=None):
        location = location or ell_world_location
        paths = ELL_WORLD_LOCATIONS[location]["backgrounds"]
        if location == "forest_lake":
            paths = ("images/minigames/fishing/backgrounds/{}.png".format(ell_fishing_period()),)
        if location == "bedroom" and "cat_plush_1" in set(getattr(persistent, "plushies_found", set())):
            paths = ("gui/maps/collectibles_gone.png",) + paths
        if ell_world_minutes >= 1260:
            paths = ("scenes/{}_night.png".format(location),) + paths
        return day1_optional_background(*(paths + (ell_world_map_art(),)))

    def ell_world_open_at(location, minutes):
        area = ELL_WORLD_LOCATIONS[location]["area"]
        if area == "forest":
            return ell_day >= 2 and 420 <= minutes <= 1380
        if area == "school":
            return 450 <= minutes < 1080
        if area in ("town", "park"):
            return 420 <= minutes < 1260
        return area == "home"

    def ell_world_travel_cost(location):
        return 0 if ELL_WORLD_LOCATIONS[location]["area"] == ELL_WORLD_LOCATIONS[ell_world_location]["area"] else 15

    def ell_world_location_unlocked(location):
        return location in ell_world_unlocked or (ell_day >= 2 and location in ("forest", "forest_lake"))

    def ell_world_travel_reason(location):
        if not ell_world_location_unlocked(location):
            return "The forest path is closed." if location == "forest" else "Check the school bulletin on your PC to unlock this place."
        if not ell_world_open_at(location, ell_world_minutes + ell_world_travel_cost(location)):
            area = ELL_WORLD_LOCATIONS[location]["area"]
            return "School is open 07:30-18:00." if area == "school" else "Open 07:00-23:00 from Day 2." if area == "forest" else "Open 07:00-21:00."
        return ""

    def ell_world_advance(minutes):
        s = renpy.store
        s.ell_world_minutes = min(1380, max(420, ell_world_minutes + int(minutes)))
        ell_world_sync_time()
        if not ell_world_open_at(ell_world_location, ell_world_minutes):
            closed_name = ELL_WORLD_LOCATIONS[ell_world_location]["name"]
            s.ell_world_location = "town_centre" if ell_world_minutes < 1260 else "hallway"
            s.ell_world_notice = "{} is closing. I head {}.".format(closed_name, "into town" if ell_world_minutes < 1260 else "home")

    def ell_world_travel(location):
        reason = ell_world_travel_reason(location)
        if reason:
            renpy.store.ell_world_notice = reason
            return False
        cost = ell_world_travel_cost(location)
        renpy.store.ell_world_location = location
        ell_world_advance(cost)
        renpy.store.ell_world_visited = set(ell_world_visited) | {location}
        return True

    def ell_world_npc_location(npc, minutes=None):
        minutes = ell_world_minutes if minutes is None else minutes
        return next((location for start, end, location in ELL_WORLD_SCHEDULES.get(npc, ()) if start <= minutes < end), None)

    def ell_world_occupants(location=None):
        location = location or ell_world_location
        return [npc for npc in ELL_WORLD_NPCS if ell_world_npc_location(npc) == location]

    def ell_world_conversation_key(npc):
        return (ell_day, ell_time_of_day, npc)

    def ell_world_unlock(location):
        renpy.store.ell_world_unlocked = set(ell_world_unlocked) | {location}

    def ell_world_finish_tutorial():
        renpy.store.ell_world_tutorial_active = False
        renpy.store.ell_world_tutorial_complete = True
        renpy.store.ell_world_tutorial_step = 0
        ell_set_quest_progress("day2_get_your_bearings", 1)

    def ell_world_next_period():
        return next((t for t in (450, 480, 510, 720, 780, 900, 1080, 1260, 1380) if t > ell_world_minutes), 1380)

    def ell_world_read_bulletin():
        if ell_world_bulletin_read:
            return False
        renpy.store.ell_world_bulletin_read = True
        ell_world_unlock("library")
        ell_world_unlock("park")
        ell_world_advance(5)
        return True

    def ell_world_attend_class():
        period = "morning" if ell_world_minutes < 720 else "afternoon" if 780 <= ell_world_minutes < 900 else None
        key = (ell_day, period)
        if ell_world_location != "classroom" or period is None or key in ell_world_classes:
            return False
        renpy.store.ell_world_classes = set(ell_world_classes) | {key}
        ell_world_advance((720 if period == "morning" else 900) - ell_world_minutes)
        if "day2_school_day" not in ell_completed_quests:
            ell_set_quest_progress("day2_school_day", sum((ell_day, p) in ell_world_classes for p in ("morning", "afternoon")))
        return True

    def ell_world_new_day():
        s = renpy.store
        s.ell_day += 1
        s.ell_world_minutes = 420
        s.ell_world_location = "bedroom"
        s.ell_world_conversations = set()
        s.ell_world_classes = set()
        if "day2_school_day" in ell_active_quests and "day2_school_day" not in ell_completed_quests:
            ell_set_quest_progress("day2_school_day", 0)
        ell_world_sync_time()

    def ell_world_room_actions():
        actions = []
        if ell_world_location == "forest_lake" and ell_day >= 2:
            actions.extend((("Cast a line", "fishing", None), ("Fishing Journal", "fishing_journal", None)))
        if ell_world_location == "bedroom":
            actions.extend((("PC", "pc", None), ("Dresser", "look", "dresser"), ("Bed / Rest", "rest", None)))
        elif ell_world_location == "kitchen" and ell_world_minutes < 540 and ell_world_breakfast_day != ell_day:
            actions.append(("Breakfast - 15 min", "breakfast", None))
        elif ell_world_location == "classroom":
            period = "morning" if ell_world_minutes < 720 else "afternoon" if 780 <= ell_world_minutes < 900 else None
            if period and (ell_day, period) not in ell_world_classes:
                actions.append(("Attend {} classes".format(period), "class", None))
        actions.append(("Look around", "look", "room"))
        for target in ELL_WORLD_LOCATIONS[ell_world_location]["links"]:
            actions.append((ELL_WORLD_LOCATIONS[target]["name"], "travel", target))
        return actions

    def ell_world_tutorial_action_allowed(action, target=None):
        if not ell_world_tutorial_active:
            return True
        key = ELL_WORLD_TUTORIAL[ell_world_tutorial_step][0]
        return (key == "map" and action == "map") or (key == "inventory" and action == "inventory") or (key == "pc" and action == "pc") or (key == "door" and action == "travel" and target == "hallway")
