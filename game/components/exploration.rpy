style ell_world_text is inv_body_text:
    size 23
    outlines [(1, "#000000bb", 0, 0)]

style ell_world_heading is inv_section_title:
    size 30

transform ell_world_hint_pulse:
    alpha 0.55
    linear 0.7 alpha 1.0
    linear 0.7 alpha 0.55
    repeat


screen ell_world_outline(rect):
    $ x, y, w, h = rect
    fixed at ell_world_hint_pulse:
        xpos x
        ypos y
        xysize (w, h)
        add Solid("#ffe69c") xsize w ysize 4
        add Solid("#ffe69c") xpos 0 ypos (h - 4) xsize w ysize 4
        add Solid("#ffe69c") xsize 4 ysize h
        add Solid("#ffe69c") xpos (w - 4) xsize 4 ysize h


screen ell_world_room():
    tag room
    zorder 250
    modal True
    add ell_world_background()
    on "show" action Function(renpy.stop_skipping)
    key "game_menu" action ShowMenu("showmenu")
    if ell_world_tutorial_action_allowed("map"):
        key "K_m" action Return(("map", None))
    if ell_world_tutorial_action_allowed("inventory"):
        key "K_i" action Return(("inventory", None))
    if not ell_world_tutorial_active:
        key "K_w" action Return(("wait", None))
        key "K_h" action Return(("help", None))

    frame:
        xpos 28
        ypos 26
        xsize 470
        ysize 105
        padding (20, 12)
        background "#171323e8"
        vbox:
            text "Day [ell_day]  |  [ell_world_clock()]  |  [ell_time_of_day!c]" style "ell_world_text" color "#ffe3a3"
            text ELL_WORLD_LOCATIONS[ell_world_location]["name"] style "ell_world_heading"

    fixed:
        xpos 520
        ypos 26
        use ui_png_button("Menu", ShowMenu("showmenu"), xsize=190, ysize=76, text_style="ui_btn_text_small", button_id="world_pause")
    fixed:
        xpos 1130
        ypos 26
        use ui_png_button("Map", Return(("map", None)), xsize=190, ysize=76, text_style="ui_btn_text_small", disabled=not ell_world_tutorial_action_allowed("map"), button_id="world_map")
    fixed:
        xpos 1340
        ypos 26
        use ui_png_button("Wait", Return(("wait", None)), xsize=160, ysize=76, text_style="ui_btn_text_small", disabled=ell_world_tutorial_active, button_id="world_wait")
    fixed:
        xpos 1520
        ypos 26
        use ui_png_button("Help", Return(("help", None)), xsize=210, ysize=76, text_style="ui_btn_text_small", disabled=ell_world_tutorial_active, button_id="world_help")

    $ _player_icon = "gui/hud/Player_female_btn.png" if mc_gender == "female" else "gui/hud/Player_male_btn.png"
    imagebutton:
        id "world_inventory"
        xpos 1768
        ypos 16
        xysize (122, 122)
        idle Transform(_player_icon, xysize=(122, 122), fit="contain")
        hover Transform(_player_icon.replace(".png", "_hover.png"), xysize=(122, 122), fit="contain")
        action Return(("inventory", None))
        sensitive ell_world_tutorial_action_allowed("inventory")
        tooltip "Player Hub (I)"

    if ell_world_location == "bedroom":
        # The same room coordinates as the existing Day 1 point-and-click.
        for rect, action_name, target, tip in (
            ((35, 260, 340, 510), "travel", "hallway", "Bedroom door"),
            ((160, 790, 470, 250), "pc", None, "Use your PC"),
            ((620, 330, 270, 270), "look", "dresser", "Dresser"),
            ((1110, 300, 520, 330), "rest", None, "Bed / Rest"),
        ):
            button:
                id ("world_hotspot_" + action_name)
                xpos rect[0]
                ypos rect[1]
                xysize (rect[2], rect[3])
                background None
                hover_background "#ffe69c25"
                action Return((action_name, target))
                sensitive ell_world_tutorial_action_allowed(action_name, target)
                tooltip tip
        if not ell_world_tutorial_active:
            if "picture1" not in set(getattr(persistent, "picture_frames_found", set())):
                button:
                    id "world_collect_picture1"
                    xpos 1570
                    ypos 360
                    xysize (90, 120)
                    background None
                    hover_background "#ffe69c44"
                    action Return(("collect", "picture1"))
                    tooltip "Look at the small frame"
            if "cat_plush_1" not in set(getattr(persistent, "plushies_found", set())):
                button:
                    id "world_collect_cat"
                    xpos 860
                    ypos 400
                    xysize (70, 180)
                    background None
                    hover_background "#ffe69c44"
                    action Return(("collect", "cat_plush_1"))
                    tooltip "Something beside the wardrobe"

    if not ell_world_tutorial_active:
        frame:
            xpos 1510
            ypos 185
            xsize 380
            padding (16, 16)
            background "#171323e8"
            vbox:
                spacing 12
                text "Who's here" style "ell_world_heading"
                $ _occupants = ell_world_occupants()
                if not _occupants:
                    text "A quiet moment." style "ell_world_text" size 20
                else:
                    vpgrid:
                        cols 2
                        spacing 10
                        xsize 348
                        ymaximum 570
                        mousewheel True
                        draggable True
                        for npc in _occupants:
                            button:
                                id ("world_npc_" + npc)
                                xsize 167
                                ysize 123
                                padding (8, 7)
                                background Frame(pref_choice_button_asset(), 20, 20)
                                hover_background Frame(pref_choice_button_asset(True), 20, 20)
                                action Return(("talk", npc))
                                tooltip "Talk to {} - 10 min for a new conversation".format(ELL_WORLD_NPCS[npc]["name"])
                                vbox:
                                    xalign 0.5
                                    add Transform(ELL_WORLD_NPCS[npc]["portrait"], xysize=(67, 68), fit="contain", xalign=0.5)
                                    text ELL_WORLD_NPCS[npc]["name"] style "ell_world_text" size 21 xalign 0.5

    frame:
        xpos 640
        ypos 840
        xsize 820
        padding (18, 14)
        background "#171323e8"
        vbox:
            spacing 10
            text "Around you" style "ell_world_heading" size 25
            grid 3 3:
                spacing 8
                $ _actions = ell_world_room_actions()
                for i in range(9):
                    if i < len(_actions):
                        $ caption, cmd, target = _actions[i]
                        $ _locked = (cmd == "travel" and bool(ell_world_travel_reason(target)))
                        use ui_png_button(caption, Return((cmd, target)), xsize=255, ysize=49, text_style="ell_world_action_text", disabled=(_locked or not ell_world_tutorial_action_allowed(cmd, target)), tooltip=(ell_world_travel_reason(target) if cmd == "travel" else None), button_id="world_action_{}_{}".format(cmd, target))
                    else:
                        null width 255 height 49

    $ _world_tip = GetTooltip()
    if _world_tip:
        frame:
            xpos 28
            ypos 1040
            padding (12, 4)
            background "#171323e8"
            text _world_tip style "ell_world_text" size 18

    if ell_world_tutorial_active:
        use ell_world_tutorial


style ell_world_action_text is ui_btn_text_small:
    size 18
    kerning 0


screen ell_world_tutorial():
    $ _key, _message = ELL_WORLD_TUTORIAL[ell_world_tutorial_step]
    $ _targets = {"map": (1126, 22, 198, 84), "inventory": (1764, 12, 130, 130), "pc": (160, 790, 470, 250), "time": (24, 22, 478, 113), "door": (35, 260, 340, 510)}
    if _key in _targets:
        $ _rect = _targets[_key]
        use ell_world_outline(_rect)
        text ("^" if _key in ("map", "inventory", "time") else "v") at ell_world_hint_pulse:
            font "DejaVuSans.ttf"
            size 62
            color "#ffe69c"
            xpos (_rect[0] + _rect[2] // 2 - 20)
            ypos (_rect[1] + _rect[3] + 4 if _key in ("map", "inventory", "time") else _rect[1] - 65)

    frame:
        xpos 35
        ypos 475
        xsize 990
        padding (22, 20)
        background "#171323f5"
        hbox:
            spacing 22
            add Transform("gui/hud/portraits/tsuki.png", xysize=(180, 184), fit="contain") at ell_world_hint_pulse
            vbox:
                spacing 12
                xsize 740
                text "Mini Tsuki" style "ell_world_heading" color "#d8c4ff"
                text _message style "ell_world_text" xmaximum 735
                hbox:
                    spacing 16
                    if _key in ("welcome", "time", "finish"):
                        use ui_png_button("Let's go!" if _key == "finish" else "Next", Return(("tutorial_next", None)), xsize=220, ysize=50, text_style="ui_btn_text_small", button_id="world_tutorial_next")
                    use ui_png_button("Skip tutorial", Return(("tutorial_skip", None)), xsize=250, ysize=50, text_style="ui_btn_text_small", button_id="world_tutorial_skip")


screen ell_world_map(tutorial=False):
    modal True
    zorder 250
    tag world_map
    key "game_menu" action Return("cancel")
    add Solid("#171323")
    $ _map_width, _map_height = renpy.image_size(ell_world_map_art())
    $ _map_scale = min(1920.0 / _map_width, 1080.0 / _map_height)
    add im.Scale(ell_world_map_art(), int(_map_width * _map_scale), int(_map_height * _map_scale)) xalign 0.5 yalign 0.5
    frame:
        xpos 28
        ypos 24
        padding (20, 14)
        background "#171323ee"
        vbox:
            text "Midgard" style "inv_title" size 40
            text "Day [ell_day]  |  [ell_world_clock()]" style "ell_world_text"
    for target, caption, x, y in ELL_WORLD_MAP_DESTINATIONS:
        $ _reason = ell_world_travel_reason(target)
        fixed:
            xpos x
            ypos y
            xsize 240
            ysize 112
            use ui_png_button(caption, Return(target), xsize=240, ysize=65, text_style="ui_btn_text_small", disabled=(tutorial or bool(_reason)), button_id="world_destination_" + target)
            text ("Locked" if not ell_world_location_unlocked(target) else "Closed" if _reason else "{} min".format(ell_world_travel_cost(target))):
                style "ell_world_text"
                size 21
                ypos 69
                xalign 0.5
                color "#ffe3a3"
    frame:
        xpos 28
        ypos 952
        xsize 1430
        padding (18, 14)
        background "#171323ee"
        text ("Have a look, then close the map to continue your tutorial." if tutorial else "School: 07:30-18:00. Town and park: 07:00-21:00. Forest Lake: 07:00-23:00, from Day 2.") style "ell_world_text"
    fixed:
        xpos 1585
        ypos 970
        use ui_png_button("Back", Return("cancel"), xsize=270, ysize=65, text_style="ui_btn_text_small", button_id="world_map_back")


screen ell_world_pc(initial_tab="bulletin"):
    modal True
    zorder 250
    tag world_pc
    default pc_tab = initial_tab
    key "game_menu" action Return("cancel")
    add Transform("gui/inventory_system/gui/inventory_bg.png", xysize=(1920, 1080))
    frame:
        xpos 100
        ypos 80
        xsize 1720
        ysize 900
        padding (32, 26)
        background "#171323e8"
        vbox:
            spacing 22
            text "Your PC" style "inv_title"
            hbox:
                spacing 20
                for tab, caption in (("bulletin", "School bulletin"), ("routine", "Daily routines"), ("journal", "Journal")):
                    use ui_png_button(caption, SetScreenVariable("pc_tab", tab), xsize=310, ysize=60, text_style="ui_btn_text_small", button_id="world_pc_tab_" + tab)
                use ui_png_button("Minigames", Return(("minigames", pc_tab)), xsize=310, ysize=60, text_style="ui_btn_text_small", disabled=(ell_day < 2 or ell_world_tutorial_active), button_id="world_pc_minigames")
            if pc_tab == "bulletin":
                text "New term notices" style "ell_world_heading"
                text "The school library is open before and after classes. The riverside park path has reopened following maintenance." style "ell_world_text" xmaximum 1500
                text "Morning classes end at 12:00. Lunch is 12:00-13:00; afternoon classes end at 15:00." style "ell_world_text"
                if not ell_world_bulletin_read:
                    use ui_png_button("Read notice - 5 min", Return("bulletin"), xsize=400, ysize=65, text_style="ui_btn_text_small", button_id="world_pc_read")
                else:
                    text "Read. The library and park are available on your routes." style "ell_world_text" color "#ffe3a3"
            elif pc_tab == "routine":
                text "Your friends' usual day" style "ell_world_heading"
                viewport:
                    xsize 1560
                    ysize 510
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    vbox:
                        spacing 18
                        for npc, slots in ELL_WORLD_SCHEDULES.items():
                            text ELL_WORLD_NPCS[npc]["name"] style "ell_world_heading" size 25
                            for start, end, location in slots:
                                text "{:02d}:{:02d}-{:02d}:{:02d}  {}".format(start // 60, start % 60, end // 60, end % 60, ELL_WORLD_LOCATIONS[location]["name"]) style "ell_world_text" size 20
            else:
                text "A few things to remember" style "ell_world_heading"
                if mc_gender == "female" and day1_akari_dream_seen:
                    text "Sunlight through branches. Someone humming. Hands that didn't look like mine." style "ell_world_text"
                    text ("Mum suggested writing down the details before they fade." if day2_hana_dream_discussed else "Maybe I should ask Mum about that dream when we have a quiet moment.") style "ell_world_text"
                else:
                    text "A new term. Familiar faces. Find a rhythm and make time for the people around me." style "ell_world_text"
                text "Tsuki's lost plushies are still out there. Keep an eye out in the rooms I visit." style "ell_world_text"
    fixed:
        xpos 1500
        ypos 985
        use ui_png_button("Shut down", Return("cancel"), xsize=310, ysize=65, text_style="ui_btn_text_small", button_id="world_pc_close")


screen ell_world_wait():
    modal True
    zorder 250
    key "game_menu" action Return("cancel")
    add ell_world_background()
    add Solid("#00000088")
    frame:
        xalign 0.5
        yalign 0.5
        padding (36, 30)
        background "#171323f5"
        vbox:
            spacing 20
            text "Take a moment" style "ell_world_heading"
            text "It is [ell_world_clock()]. People may move while you wait." style "ell_world_text"
            for caption, value in (("Wait 15 minutes", 15), ("Wait one hour", 60), ("Wait until the next part of the day", "next")):
                use ui_png_button(caption, Return(value), xsize=610, ysize=60, text_style="ui_btn_text_small", disabled=ell_world_minutes >= 1380, button_id="world_wait_" + str(value))
            use ui_png_button("Back", Return("cancel"), xsize=610, ysize=60, text_style="ui_btn_text_small", button_id="world_wait_back")


screen ell_world_help():
    modal True
    zorder 250
    key "game_menu" action Return("cancel")
    add ell_world_background()
    add Solid("#00000088")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1220
        padding (32, 26)
        background "#171323f5"
        vbox:
            spacing 18
            text "Mini Tsuki's reminders" style "ell_world_heading" color "#d8c4ff"
            text "Map (M): travel to unlocked, open places. Different areas take 15 minutes; nearby rooms are free." style "ell_world_text"
            text "Player Hub (I): inventory, quests, collectibles and character notes." style "ell_world_text"
            text "Wait (W): pass time. New conversations take 10 minutes. Menus and looking around take no time." style "ell_world_text"
            text "People follow their own routines. Check your PC to see where they usually go." style "ell_world_text"
            text "Attend classes from your classroom. At home, click the desk, door, dresser, bed or small collectibles." style "ell_world_text"
            text "You can sleep in your bedroom from 21:00. Save and load through the pause menu at any time." style "ell_world_text"
            hbox:
                spacing 18
                if ell_world_location == "bedroom":
                    use ui_png_button("Replay tutorial", Return("replay"), xsize=360, ysize=60, text_style="ui_btn_text_small", button_id="world_replay")
                use ui_png_button("Back", Return("cancel"), xsize=280, ysize=60, text_style="ui_btn_text_small", button_id="world_help_back")
