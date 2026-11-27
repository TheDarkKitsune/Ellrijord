# Screens share Ellrijord's existing plum, cream and gold minigame skin.
style ell_fishing_small is ell_minigame_body:
    size 20
style ell_fishing_muted is ell_fishing_small:
    color "#bdaaca"
style ell_fishing_vscrollbar is vscrollbar:
    xsize 12
    base_bar "#392f49"
    thumb "#a58ac5"
    unscrollable "hide"

screen ell_fishing_rules():
    hbox:
        spacing 36
        add Transform("gui/hud/portraits/tsuki.png", xysize=(210, 245), fit="contain") yalign 0.5
        vbox:
            spacing 18
            xsize 1040
            text "Mini Tsuki's lakeside lesson" style "ell_minigame_title" size 34
            text "Move your mouse DOWN to lower the hook, and UP to reel it in. The hook stays beneath the end of the dock." style "ell_minigame_body"
            text "Meet a fish with the bait, then lift it ABOVE the waterline. You can carry one fish at a time. Landing a fish keeps your bait!" style "ell_minigame_body"
            text "Start with three bait lives. Catch 30 fish, build a streak for up to x5 score, and scoop up spare bait. Hazards arrive gradually." style "ell_minigame_body"
            text "Boots and pike steal your catch. Crabs and eels cost bait. Branches and weeds slow the line. At night, wisps can reverse your controls." style "ell_fishing_small" color "#e4c575"
            text "A secret of the night: if the deep stirs, keep a Moonfin on your hook and offer it below. Ordinary bait will not tempt the guardian." style "ell_fishing_small" color "#d7c5fa"
            text "Esc / Space pauses. Instructions and exit also freeze the lake. Finished catches are kept when you return early; restarting discards the current session." style "ell_fishing_muted"

screen ell_fishing_tutorial():
    modal True
    zorder 270
    key "game_menu" action Return(True)
    use ell_minigame_shell("A little patience. A little wonder.", "Forest Lake Fishing"):
        fixed:
            ysize 700
            use ell_fishing_rules
        hbox:
            xalign 0.5
            use ell_minigame_button("Let's cast!", Return(True), "play", width=420, button_id="fishing_tutorial_start")

screen ell_fishing_setup():
    modal True
    zorder 250
    default selected_rod = ell_fishing_rod
    key "game_menu" action Return(None)
    add Transform("images/minigames/fishing/backgrounds/" + ell_fishing_period() + ".png", xysize=(1920, 1080))
    frame:
        align (0.5, 0.5)
        xysize (1520, 950)
        padding (48, 30)
        background Frame(ell_minigame_ui("panel"), 36, 36)
        vbox:
            spacing 18
            text "Forest Lake" style "ell_minigame_title" size 52 xalign 0.5
            text "Beneath the waterfall, a quieter kind of adventure." style "ell_fishing_muted" xalign 0.5
            hbox:
                spacing 42
                frame:
                    xysize (660, 610)
                    padding (20, 20)
                    background Frame(ell_minigame_ui("stat"), 32, 32)
                    vbox:
                        spacing 20
                        add Transform("images/minigames/fishing/ui/journal.png", xysize=(205, 170)) xalign 0.5
                        text "[ell_fishing_period()!c] at the lake" style "ell_minigame_title" size 31 xalign 0.5
                        text "30 fish  |  3 bait lives  |  up to x5 score" style "ell_fishing_small" xalign 0.5
                        text "Personal best: {:,}".format(persistent.ell_fishing_best or 0) style "ell_fishing_small" xalign 0.5 color "#e4c575"
                        text "Species discovered: {} / {}".format(len(ell_fishing_journal), len(ELL_FISHING_SPECIES)) style "ell_fishing_small" xalign 0.5
                        text "Catches go to your inventory. If it fills up, the lake keeps the rest safe until you collect them here." style "ell_fishing_muted" text_align 0.5
                        if ell_fishing_pending:
                            use ell_minigame_button("Collect stored fish ({})".format(sum(ell_fishing_pending.values())), Function(ell_fishing_deliver), width=600, button_id="fishing_collect")
                vbox:
                    spacing 8
                    text "Choose your rod" style "ell_minigame_title" size 30
                    for rod_id, rod_spec in ELL_FISHING_RODS.items():
                        $ unlocked = rod_id in ell_fishing_rods
                        use ell_minigame_button(("Selected  -  " if selected_rod == rod_id else "") + rod_spec["name"] + ("" if unlocked else "  /  Locked"), SetScreenVariable("selected_rod", rod_id), width=650, height=58, disabled=not unlocked, button_id="fishing_rod_" + rod_id)
                    text ELL_FISHING_RODS[selected_rod]["description"] style "ell_fishing_small" xmaximum 630
                    text "More rods will become available through future story and shop content." style "ell_fishing_muted" xmaximum 630
            hbox:
                xalign 0.5
                spacing 18
                use ell_minigame_button("Cast a line", [SetVariable("ell_fishing_rod", selected_rod), Return("play")], "play", width=400, button_id="fishing_play")
                use ell_minigame_button("Journal", Show("ell_fishing_journal_screen"), "pairs", width=290, button_id="fishing_journal")
                use ell_minigame_button("Return", Return(None), "exit", width=290, button_id="fishing_return")

screen ell_fishing_play(period, rod):
    modal True
    zorder 250
    default lake = EllFishingDisplayable(period, rod)
    default overlay = None
    add lake id "fishing_lake"
    if overlay is None:
        key "game_menu" action [Function(lake.set_pause), SetScreenVariable("overlay", "pause")]
        key "K_SPACE" action [Function(lake.set_pause), SetScreenVariable("overlay", "pause")]
        hbox:
            xpos 1395
            ypos 42
            spacing 10
            use ell_minigame_button("Pause", [Function(lake.set_pause), SetScreenVariable("overlay", "pause")], width=145, height=60, button_id="fishing_pause")
            use ell_minigame_button("Help", [Function(lake.set_pause), SetScreenVariable("overlay", "help")], width=145, height=60, button_id="fishing_help")
            use ell_minigame_button("Exit", [Function(lake.set_pause), SetScreenVariable("overlay", "exit")], width=145, height=60, button_id="fishing_exit")
    else:
        add Solid("#0d1020c9")
        key "game_menu" action [Function(lake.set_pause, False), SetScreenVariable("overlay", None)]
        key "K_SPACE" action [Function(lake.set_pause, False), SetScreenVariable("overlay", None)]
        frame:
            align (0.5, 0.5)
            xysize ((1500, 900) if overlay == "help" else (1010, 670))
            padding (42, 36)
            background Frame(ell_minigame_ui("panel"), 36, 36)
            vbox:
                spacing 25
                if overlay == "help":
                    text "The lake can wait" style "ell_minigame_title" size 40 xalign 0.5
                    use ell_fishing_rules
                elif overlay == "exit":
                    text "Return to shore?" style "ell_minigame_title" size 42 xalign 0.5
                    text "Keep the fish already landed and finish this session. A fish still on the hook will swim free." style "ell_minigame_body" text_align 0.5
                    use ell_minigame_button("Finish and keep catches", Function(lake.leave), "exit", width=900, button_id="fishing_exit_confirm")
                elif overlay == "restart":
                    text "A fresh cast?" style "ell_minigame_title" size 42 xalign 0.5
                    text "Restart with three bait lives. This session's score and catches will be discarded." style "ell_minigame_body" text_align 0.5
                    use ell_minigame_button("Restart session", Return("restart"), "restart", width=900, button_id="fishing_restart_confirm")
                else:
                    text "A moment by the lake" style "ell_minigame_title" size 42 xalign 0.5
                    text "Paused. The water, fish and all effects are resting." style "ell_fishing_muted" xalign 0.5
                    use ell_minigame_button("Instructions", SetScreenVariable("overlay", "help"), "instructions", width=900, button_id="fishing_pause_help")
                    use ell_minigame_button("Start again", SetScreenVariable("overlay", "restart"), "restart", width=900, button_id="fishing_restart")
                    use ell_minigame_button("Return to shore", SetScreenVariable("overlay", "exit"), "exit", width=900, button_id="fishing_pause_exit")
                use ell_minigame_button("Resume fishing", [Function(lake.set_pause, False), SetScreenVariable("overlay", None)], "play", width=900, button_id="fishing_resume")

screen ell_fishing_results(result):
    modal True
    zorder 250
    key "game_menu" action Return("return")
    use ell_minigame_shell("A basket of stories", "Target reached!" if result["reason"] == "target" else "Out of bait. The lake will be here tomorrow." if result["reason"] == "no_bait" else "Back on the shore. Your landed catches are safe."):
        hbox:
            spacing 38
            ysize 700
            vbox:
                xsize 700
                spacing 18
                text "{:,} points".format(result["score"]) style "ell_minigame_title" size 56 color "#e4c575"
                text "Fish landed: {}".format(result["caught"]) style "ell_minigame_body"
                text "Longest streak: {}".format(result["longest_streak"]) style "ell_minigame_body"
                text "Rare / epic / legendary: {}".format(result["rare_caught"]) style "ell_minigame_body"
                text "Personal best: {:,}{}".format(result["personal_best"], "  -  NEW BEST!" if result.get("new_best") else "") style "ell_minigame_body" color "#e4c575"
                text "Rewards" style "ell_minigame_title" size 30
                text "{} fish added to inventory".format(result["rewards"]["inventory"]) style "ell_fishing_small"
                text "{} fish stored safely at the lake".format(result["rewards"]["stored"]) style "ell_fishing_small"
                if result["rewards"]["discoveries"]:
                    text "New discoveries: " + ", ".join(result["rewards"]["discoveries"]) style "ell_fishing_small" xmaximum 680
                text "Fish are kept as ingredients. Selling and rod purchases can use future shops." style "ell_fishing_muted" xmaximum 650
            viewport:
                style_prefix "ell_fishing"
                mousewheel True
                draggable True
                scrollbars "vertical"
                xysize (890, 670)
                vbox:
                    spacing 8
                    for fish_id, count in result["catches"].items():
                        hbox:
                            spacing 24
                            add Transform(ELL_FISHING_SPECIES[fish_id]["art"], xysize=(180, 100), fit="contain")
                            vbox:
                                yalign 0.5
                                text ELL_FISHING_SPECIES[fish_id]["name"] style "ell_minigame_body"
                                text "{}  |  caught {}".format(ELL_FISHING_SPECIES[fish_id]["rarity"], count) style "ell_fishing_muted"
                    if not result["catches"]:
                        text "Every angler starts with a quiet cast. Try meeting a fish a little deeper next time." style "ell_fishing_muted" xmaximum 650
        hbox:
            xalign 0.5
            spacing 24
            use ell_minigame_button("Play again", Return("again"), "play", width=350, button_id="fishing_again")
            use ell_minigame_button("Journal", Show("ell_fishing_journal_screen"), "pairs", width=350, button_id="fishing_results_journal")
            use ell_minigame_button("Return", Return("return"), "exit", width=350, button_id="fishing_results_return")

screen ell_fishing_journal_screen():
    modal True
    zorder 290
    default selected = "goldenfin"
    key "game_menu" action Hide("ell_fishing_journal_screen")
    use ell_minigame_shell("The Lakekeeper's Journal", "{} of {} species discovered".format(len(ell_fishing_journal), len(ELL_FISHING_SPECIES))):
        hbox:
            spacing 42
            ysize 700
            vbox:
                spacing 10
                for fish_id, spec in ELL_FISHING_SPECIES.items():
                    use ell_minigame_button(spec["name"] if fish_id in ell_fishing_journal else "Undiscovered species", SetScreenVariable("selected", fish_id), width=490, height=65, button_id="fishing_entry_" + fish_id)
            vbox:
                xsize 1080
                spacing 14
                $ spec = ELL_FISHING_SPECIES[selected]
                $ entry = ell_fishing_journal.get(selected)
                add Transform(spec["art"] if entry else spec["silhouette"], xysize=(760, 290), fit="contain") xalign 0.5
                if entry:
                    text spec["name"] style "ell_minigame_title" size 39 xalign 0.5
                    text spec["rarity"] style "ell_minigame_body" color "#e4c575" xalign 0.5
                    text spec["description"] style "ell_minigame_body" text_align 0.5
                    text "Total caught: {}  |  First discovery: Day {} ({})".format(entry["count"], entry["first_day"], entry["first_discovery"]) style "ell_fishing_small"
                    text "Waters: " + ", ".join(ELL_FISHING_LOCATIONS[k] for k in spec["locations"]) style "ell_fishing_small"
                    text "Availability: " + ", ".join(t.title() for t in spec["times"]) style "ell_fishing_small"
                else:
                    text "An unwritten page" style "ell_minigame_title" size 39 xalign 0.5
                    text "Land this fish to reveal its name, habits and story." style "ell_fishing_muted" xalign 0.5
        hbox:
            xalign 0.5
            use ell_minigame_button("Close journal", Hide("ell_fishing_journal_screen"), "exit", width=450, button_id="fishing_journal_close")
