# Durable progression and the public entry point. Live sessions run in a
# disposable context; saves contain completed results, never swimming entities.
default ell_fishing_journal = {}
default ell_fishing_claimed = set()
default ell_fishing_pending = {}
default ell_fishing_rods = {"wooden"}
default ell_fishing_rod = "wooden"
default ell_fishing_tutorial_seen = False
default persistent.ell_fishing_best = 0

define ell_fishing_first_achievement = Achievement("A Quiet Cast", id="ell_fishing_first", description="Land your first fish at Forest Lake.", unlocked_image="images/minigames/fishing/fish/goldenfin.png")
define ell_fishing_full_achievement = Achievement("Lakekeeper", id="ell_fishing_full", description="Complete a thirty-fish fishing session.", unlocked_image="images/minigames/fishing/ui/journal.png")
define ell_fishing_legend_achievement = Achievement("A Gift of Moonlight", id="ell_fishing_legend", description="Bring the guardian of Forest Lake to the surface.", unlocked_image="images/minigames/fishing/fish/void_leviathan.png", hide_name=True, hide_description=True)

init -2 python:
    import copy as fishing_copy
    import uuid as fishing_uuid
    import datetime as fishing_datetime

    ELL_MINIGAMES["forest_fishing"] = {
        "title": "Forest Lake Fishing", "description": "Cast a line beneath the waterfall. Discover what swims below.",
        "label": "ellrijord_fishing", "unlock_day": 2,
    }

    def ell_fishing_period():
        return "night" if ell_time_of_day == "night" else "twilight" if ell_time_of_day == "evening" else "day"

    def ell_fishing_deliver():
        # Respect the existing stack and slot limits; keep overflow for later.
        pending = dict(ell_fishing_pending)
        if not pending:
            return 0
        inv = fishing_copy.deepcopy(inventory)
        delivered = 0
        for fish_id, count in list(pending.items()):
            added = inv.add_item(fish_id, count, notify=False)
            delivered += added
            if added == count:
                del pending[fish_id]
            else:
                pending[fish_id] -= added
        renpy.store.inventory = inv
        renpy.store.ell_fishing_pending = pending
        return delivered

    def ell_fishing_commit(result):
        if not result or result.get("session_id") in ell_fishing_claimed:
            return False
        s = renpy.store
        s.ell_fishing_claimed = set(ell_fishing_claimed) | {result["session_id"]}
        journal, pending = fishing_copy.deepcopy(ell_fishing_journal), dict(ell_fishing_pending)
        discoveries = []
        for fish_id, count in result["catches"].items():
            if fish_id not in journal:
                journal[fish_id] = {"count": 0, "first_day": ell_day,
                                    "first_discovery": fishing_datetime.date.today().isoformat(), "locations": []}
                discoveries.append(ELL_FISHING_SPECIES[fish_id]["name"])
            journal[fish_id]["count"] += count
            journal[fish_id]["locations"] = sorted(set(journal[fish_id]["locations"]) | {result["location"]})
            pending[fish_id] = pending.get(fish_id, 0) + count
        s.ell_fishing_journal, s.ell_fishing_pending = journal, pending
        delivered = ell_fishing_deliver()
        result["rewards"] = {"inventory": delivered, "stored": sum(ell_fishing_pending.values()), "discoveries": discoveries}
        result["personal_best"] = max(result["score"], persistent.ell_fishing_best or 0)
        result["new_best"] = result["score"] > (persistent.ell_fishing_best or 0)
        persistent.ell_fishing_best = result["personal_best"]
        renpy.save_persistent()
        if result["caught"]:
            ell_fishing_first_achievement.grant()
        if result["caught"] >= ELL_FISHING_CONFIG["target"]:
            ell_fishing_full_achievement.grant()
        if result["legendary"]:
            ell_fishing_legend_achievement.grant()
        return True


label ellrijord_fishing(_fishing_previous_quick=None, _fishing_previous_location=None, _fishing_again=True, _fishing_result=None):
    if not ell_minigame_available("forest_fishing"):
        return
    $ _fishing_previous_quick = quick_menu
    $ _fishing_previous_location = ell_world_location
    $ quick_menu = False
    $ renpy.stop_skipping()
    $ renpy.block_rollback()
    while _fishing_again:
        call screen ell_fishing_setup
        if _return != "play":
            $ _fishing_again = False
        else:
            if not ell_fishing_tutorial_seen:
                call screen ell_fishing_tutorial
                $ ell_fishing_tutorial_seen = True
            $ renpy.block_rollback()
            $ _fishing_result = renpy.call_in_new_context("_ell_fishing_session", ell_fishing_period(), ell_fishing_rod)
            $ _fishing_result["session_id"] = fishing_uuid.uuid4().hex
            $ ell_fishing_commit(_fishing_result)
            $ ell_minigame_last_result = _fishing_result
            $ renpy.block_rollback()
            call screen ell_fishing_results(_fishing_result)
            $ _fishing_again = _return == "again"
    $ ell_world_location = _fishing_previous_location
    $ quick_menu = _fishing_previous_quick
    $ renpy.block_rollback()
    return ell_minigame_last_result


label _ell_fishing_session(_fishing_period, _fishing_equipped):
    # New contexts do not save live state or participate in story rollback.
    # Only this plain result crosses back into the main context.
    window hide
    call screen ell_fishing_play(_fishing_period, _fishing_equipped)
    while _return == "restart":
        call screen ell_fishing_play(_fishing_period, _fishing_equipped)
    return _return
