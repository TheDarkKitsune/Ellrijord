default ell_active_quests = set()
default ell_completed_quests = set()
default ell_quest_progress = {}

init -5 python:
    ELL_QUESTS = {
        "tsuki_lost_plushies": {
            "title": "Tsuki's Lost Plushies",
            "giver": "Tsuki",
            "description": "Find all 25 of Tsuki's missing plushies scattered around the world.",
            "target": 25,
            "kind": "collection",
        },
        "picture_frames_25": {
            "title": "Picture Frame Collection",
            "giver": "Unknown",
            "description": "Discover all 25 hidden picture frames.",
            "target": 25,
            "kind": "collection",
        },
        "first_day_settle_in": {
            "title": "First Day, First Steps",
            "giver": "System",
            "description": "Make it through your first morning and arrive at school.",
            "target": 1,
            "kind": "story",
        },
        "meet_the_upperclassmen": {
            "title": "Familiar Faces",
            "giver": "System",
            "description": "Reconnect with the Year 3 trio.",
            "target": 1,
            "kind": "story",
        },
        "family_tradition": {
            "title": "Family Tradition",
            "giver": "System",
            "description": "Deal with whatever trouble Rika brings your way.",
            "target": 1,
            "kind": "story",
        },
    }

    def ell_get_quest(quest_id):
        return ELL_QUESTS.get(quest_id, None)

    def ell_accept_quest(quest_id):
        if quest_id not in ELL_QUESTS:
            return False

        active = set(getattr(renpy.store, "ell_active_quests", set()))
        completed = set(getattr(renpy.store, "ell_completed_quests", set()))
        progress = dict(getattr(renpy.store, "ell_quest_progress", {}))

        if quest_id in active or quest_id in completed:
            return False

        active.add(quest_id)
        progress.setdefault(quest_id, 0)

        renpy.store.ell_active_quests = active
        renpy.store.ell_quest_progress = progress
        return True

    def ell_set_quest_progress(quest_id, value):
        if quest_id not in ELL_QUESTS:
            return False

        ell_accept_quest(quest_id)

        active = set(getattr(renpy.store, "ell_active_quests", set()))
        completed = set(getattr(renpy.store, "ell_completed_quests", set()))
        progress = dict(getattr(renpy.store, "ell_quest_progress", {}))

        target = int(ELL_QUESTS[quest_id].get("target", 1))
        progress[quest_id] = max(0, min(int(value), target))

        if progress[quest_id] >= target:
            active.discard(quest_id)
            completed.add(quest_id)

        renpy.store.ell_active_quests = active
        renpy.store.ell_completed_quests = completed
        renpy.store.ell_quest_progress = progress
        return True

    def ell_add_quest_progress(quest_id, amount=1):
        current = dict(getattr(renpy.store, "ell_quest_progress", {})).get(quest_id, 0)
        return ell_set_quest_progress(quest_id, current + amount)

    def ell_sync_collectible_quests():
        plushies_found = len(set(getattr(renpy.store.persistent, "plushies_found", set())))
        picture_frames_found = len(set(getattr(renpy.store.persistent, "picture_frames_found", set())))

        if "tsuki_lost_plushies" in set(getattr(renpy.store, "ell_active_quests", set())) or "tsuki_lost_plushies" in set(getattr(renpy.store, "ell_completed_quests", set())):
            ell_set_quest_progress("tsuki_lost_plushies", plushies_found)

        if "picture_frames_25" in set(getattr(renpy.store, "ell_active_quests", set())) or "picture_frames_25" in set(getattr(renpy.store, "ell_completed_quests", set())):
            ell_set_quest_progress("picture_frames_25", picture_frames_found)
