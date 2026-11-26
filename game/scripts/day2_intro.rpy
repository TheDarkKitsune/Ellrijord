# Day 2 introduces the shared exploration loop. Mini Tsuki is a UI guide;
# her tutorial is separate from the real Tsuki's daily location and dialogue.

label day2_opening:
    $ day1_ensure_characters()
    if not day2_opening_seen:
        $ ell_day = 2
        $ ell_world_minutes = 420
        $ ell_world_location = "bedroom"
        $ ell_world_visited = set(ell_world_visited) | {"bedroom"}
        $ ell_world_sync_time()
        scene expression ell_world_background() with fade
        narrator "Morning light finds its way into my room."
        if mc_gender == "female" and day1_akari_dream_seen:
            narrator "For a moment, I can almost hear that unfinished tune again. Then the ordinary sounds of the house take its place."
            mc "(Maybe I'll ask Mum about the dream when I see her.)"
        else:
            mc "(Right. A little less rushing around today.)"
        narrator "A tiny Tsuki appears at the edge of the screen, looking extremely pleased with herself."
        $ ell_accept_quest("day2_get_your_bearings")
        $ ell_accept_quest("day2_school_day")
        $ ell_world_tutorial_active = not ell_world_tutorial_complete
        $ ell_world_tutorial_step = 0
        $ day2_opening_seen = True
    jump day2_free_roam


label day2_free_roam:
    while True:
        $ renpy.stop_skipping()
        scene expression ell_world_background()
        if ell_world_notice:
            narrator "[ell_world_notice]"
            $ ell_world_notice = ""
        window hide
        call screen ell_world_room
        $ _world_cmd, _world_target = _return

        if _world_cmd == "tutorial_skip":
            $ ell_world_finish_tutorial()
        elif _world_cmd == "tutorial_next":
            if ell_world_tutorial_step == len(ELL_WORLD_TUTORIAL) - 1:
                $ ell_world_finish_tutorial()
            else:
                $ ell_world_tutorial_step += 1
        elif _world_cmd == "map":
            call screen ell_world_map(tutorial=ell_world_tutorial_active)
            $ _destination = _return
            if ell_world_tutorial_active:
                $ ell_world_tutorial_step += 1
            elif _destination in ELL_WORLD_LOCATIONS:
                $ ell_world_travel(_destination)
        elif _world_cmd == "inventory":
            $ _world_quick_menu_before = quick_menu
            $ quick_menu = False
            call screen inventory_menu
            $ quick_menu = _world_quick_menu_before
            if ell_world_tutorial_active:
                $ ell_world_tutorial_step += 1
        elif _world_cmd == "pc":
            call ell_world_use_pc
            if ell_world_tutorial_active:
                $ ell_world_tutorial_step += 1
        elif _world_cmd == "travel":
            $ _travelled = ell_world_travel(_world_target)
            if _travelled and ell_world_tutorial_active:
                $ ell_world_tutorial_step += 1
        elif _world_cmd == "wait":
            call screen ell_world_wait
            if _return in (15, 60, "next"):
                $ ell_world_advance(ell_world_next_period() - ell_world_minutes if _return == "next" else _return)
        elif _world_cmd == "help":
            call screen ell_world_help
            if _return == "replay":
                $ ell_world_tutorial_active = True
                $ ell_world_tutorial_step = 0
        elif _world_cmd == "talk":
            call ell_world_chat(_world_target)
        elif _world_cmd == "look":
            if _world_target == "dresser":
                narrator "My uniform is ready for the day. Everything else is where I left it."
            elif ell_world_location == "bedroom":
                narrator "My own little corner of the house. The desk, the wardrobe, and a few things Tsuki probably hopes I won't notice."
            elif ell_world_location == "classroom":
                narrator "My seat is waiting. Morning lessons finish at noon; afternoon classes run from one until three."
            elif ell_world_location == "library":
                narrator "The library is peaceful. The noticeboard near the entrance is already filling up with new term announcements."
            elif ell_world_location == "park":
                narrator "The reopened path follows the river between the trees. It's an easy place to lose track of the noise of town."
            elif ell_world_location == "kitchen":
                narrator "The kitchen smells faintly of tea. It's the first place I check when I'm looking for Mum in the morning."
            else:
                narrator "I take a moment to look around. Familiar places feel different depending on who's here."
        elif _world_cmd == "breakfast":
            if ell_world_breakfast_day != ell_day and ell_world_minutes < 540:
                narrator "I sit down for breakfast before heading out. A proper start to the day, for once."
                $ ell_world_breakfast_day = ell_day
                $ ell_world_advance(15)
        elif _world_cmd == "class":
            if ell_world_attend_class():
                narrator "I settle into my seat and turn my attention to the lessons."
                narrator "By the time the bell rings, my notebook is considerably less empty."
        elif _world_cmd == "collect":
            call ell_world_collect(_world_target)
        elif _world_cmd == "rest":
            call ell_world_rest


label ell_world_use_pc(_pc_tab="bulletin"):
    while True:
        call screen ell_world_pc(getattr(renpy.store, "_pc_tab", "bulletin"))
        if isinstance(_return, tuple) and _return[0] == "minigames":
            $ _pc_tab = _return[1]
            call ell_minigames from ell_world_pc_minigames
        elif _return != "bulletin":
            return
        elif ell_world_read_bulletin():
            narrator "I read through the school notices. The library is open for the new term, and the riverside path is finally clear again."
            call screen day1_game_ui_popup(title="NEW ROUTES AVAILABLE", subtitle="Library and Riverside Park", body="You can reach the library through the school corridor and the park from your map.")


label ell_world_chat(npc):
    if ell_world_npc_location(npc) != ell_world_location:
        narrator "They must have moved on. I'll try another time."
        return
    $ _conversation_key = ell_world_conversation_key(npc)
    if _conversation_key in ell_world_conversations:
        narrator "We exchange another quick hello before getting back to what we were doing."
        return

    if npc == "hana":
        hana "There you are. Finding your feet today?"
        mc "Trying to. It feels good having a little time to myself."
        if mc_gender == "female" and day1_akari_dream_seen and not day2_hana_dream_discussed:
            mc "Mum... I dreamed about those branches again. But this time the hands I could see didn't look like mine."
            hana "Were you looking down at them?"
            mc "I think so. Someone behind me was calling for their mum, but I woke up before I could turn around."
            hana "Write down what you can remember while it's still clear. We can look at it together."
            mc "You don't think it's strange?"
            hana "I'm glad you told me. Let's take one piece at a time."
            $ day2_hana_dream_discussed = True
        elif ell_time_of_day == "morning":
            hana "Have something to eat before school. And check the notices if you're making plans for later."
        else:
            hana "Just let me know if you'll be late home."
    elif npc == "tsuki":
        tsuki "Aha! My extremely reliable plushie assistant!"
        mc "You could at least say hello first."
        tsuki "Hello, extremely reliable plushie assistant. Better?"
        tsuki "Keep checking the little corners of your room. I'm sure I left something near the wardrobe..."
    elif npc == "aria":
        if ell_time_of_day == "morning":
            aria "Morning treating you a little more kindly today?"
        else:
            aria "It's nice having a moment to catch up."
        mc "I'm getting used to the new routine."
        aria "Good. Make a little room in it for your friends too."
    elif npc == "poko":
        poko "There you are! I was beginning to think you'd found a secret route around me."
        mc "Would you really let me live that down?"
        poko "Absolutely not. That's why you should come say hello."
    elif npc == "mimi":
        mimi "I've been looking through the new library notices."
        mc "Already planning the whole term?"
        mimi "Only the sensible parts. Someone has to leave room for Poko's plans."
    elif npc == "kuroe":
        kuroe "The old-world display has some interesting gaps."
        mc "Gaps?"
        kuroe "Different accounts of the same places. I want to compare them before jumping to conclusions."
        mc "Let me know what you find."
    elif npc == "sakura":
        sakura "It's nice seeing everyone settle back in."
        mc "Even with all the new timetables?"
        sakura "We'll figure them out. Lunch in the courtyard is a good place to start."
    elif npc == "rika":
        rika "You found me!"
        mc "You say that as if you weren't standing in the middle of the corridor."
        rika "I make it easy because I'm thoughtful."
        mc "Is that what we're calling it now?"

    $ ell_world_conversations = set(ell_world_conversations) | {_conversation_key}
    $ ell_world_advance(10)
    return


label ell_world_collect(collectible):
    if collectible == "picture1" and "picture1" not in set(getattr(persistent, "picture_frames_found", set())):
        $ day1_unlock_picture_frame("picture1", "secrets/Picture Frames/picture1.png")
        call screen day1_secret_discovered_popup("secrets/Picture Frames/picture1.png", "You've discovered a secret.")
    elif collectible == "cat_plush_1" and "cat_plush_1" not in set(getattr(persistent, "plushies_found", set())):
        narrator "A small cat plush is tucked away beside the wardrobe. Tsuki was right."
        $ day1_unlock_plushie("cat_plush_1", "secrets/plushies/kittycat_plush.png")
        call screen day1_game_ui_popup(title="PLUSHIE FOUND", subtitle="Tsuki's Cat Plush", body="One more of Tsuki's lost plushies is safely accounted for.")
    return


label ell_world_rest:
    menu:
        "Rest for half an hour.":
            narrator "I take a short break before getting on with the day."
            $ ell_world_advance(30)
        "Sleep until morning." if ell_world_minutes >= 1260:
            scene black with fade
            narrator "I put the day behind me and settle down to sleep."
            $ ell_world_new_day()
            scene expression ell_world_background() with fade
            narrator "Another morning. Another chance to find my own way through the day."
        "Get up again.":
            pass
    return
