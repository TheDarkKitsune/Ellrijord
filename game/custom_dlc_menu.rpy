# custom_dlc_menu.rpy
# DLC menu with sidebar tabs and ownership display.

init -2 python:
    DLC_TABS = [
        ("free", "Free DLC"),
        ("paid", "Paid DLC"),
        ("supporter", "Supporter DLC"),
    ]

    DLC_ITEMS = [
        {
            "id": "summer_festival_dlc",
            "name": "Summer Festival DLC",
            "type": "free",
            "desc": "Theme: romance-heavy. Adds 1 extra date per heroine, a fireworks confession variant, and yukata outfits.",
        },
        {
            "id": "spring_festival_story",
            "name": "Spring Festival Story",
            "type": "free",
            "desc": "Festival-themed mini arc with extra dialogue and CG rewards.",
        },
        {
            "id": "halloween_event",
            "name": "Halloween Event",
            "type": "free",
            "desc": "Limited-time side story. One-night anomaly event, costumes, and light comedy.",
        },
        {
            "id": "void_chronicles_expansion",
            "name": "Void Chronicles Expansion",
            "type": "paid",
            "desc": "Major story expansion with new chapters, choices, and endings.",
        },
        {
            "id": "city_nights_pack",
            "name": "City Nights Pack",
            "type": "paid",
            "desc": "Additional late-night city events and character interactions.",
        },
        {
            "id": "lady_ender_route",
            "name": "Lady Ender Route",
            "type": "paid",
            "desc": "Emotional tragedy arc. Enter her memories, see Aurora before corruption,massive lore payoff.",
        },
        {
            "id": "founders_collection",
            "name": "Founder's Collection",
            "type": "supporter",
            "desc": "Supporter-exclusive artbook, soundtrack extras, and title badge.",
        },
        {
            "id": "supporter_route_bundle",
            "name": "Supporter Route Bundle",
            "type": "supporter",
            "desc": "Early access route variants and behind-the-scenes story notes.",
        },
    ]

    def _dlc_items_for(tab_id):
        return [x for x in DLC_ITEMS if x.get("type") == tab_id]

    DLC_OWNERSHIP_ALIASES = {
        "summer_festival_dlc": ["academy_window_pack"],
    }

    def _dlc_owned_set():
        raw = getattr(persistent, "dlc_owned_ids", None)
        if raw is None:
            s = set()
        else:
            try:
                s = set(raw)
            except Exception:
                s = set()
        persistent.dlc_owned_ids = s
        return s

    def dlc_is_owned(dlc_id):
        key = str(dlc_id)
        owned = _dlc_owned_set()
        if key in owned:
            return True
        for alias in DLC_OWNERSHIP_ALIASES.get(key, []):
            if str(alias) in owned:
                return True
        return False

    def dlc_set_owned(dlc_id, owned=True):
        s = _dlc_owned_set()
        key = str(dlc_id)
        if owned:
            s.add(key)
        else:
            s.discard(key)
        persistent.dlc_owned_ids = s
        renpy.save_persistent()


style dlc_header_title is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 66
    color "#f4ebff"
    outlines [(3, "#2b1d42", 0, 0)]
    xalign 0.5
    text_align 0.5

style dlc_tab_button is button:
    background Solid("#2f2448")
    hover_background Solid("#4c2f73")
    selected_background Solid("#6b3aa8")
    xpadding 18
    ypadding 12

style dlc_tab_button_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 30
    color "#f3eaff"
    outlines [(2, "#2b1d42", 0, 0)]
    text_align 0.5
    xalign 0.5

style dlc_card_title is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 34
    color "#f5eeff"
    outlines [(2, "#221634", 0, 0)]

style dlc_card_body is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 22
    color "#e9ddff"
    outlines [(1, "#221634", 0, 0)]
    line_spacing 2

style dlc_status_owned is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 22
    color "#adffcf"
    outlines [(1, "#1d4c32", 0, 0)]

style dlc_status_locked is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 22
    color "#ffc8d0"
    outlines [(1, "#5a202d", 0, 0)]


screen extra_dlc_menu():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))
    default dlc_tab = "free"
    default show_dlc_dev = False
    $ panel_w = 1640
    $ panel_h = 820
    $ news_bg = "gui/news/new_background.png" if renpy.loadable("gui/news/new_background.png") else "gui/news/news_background.png"
    $ tab_label = dict(DLC_TABS).get(dlc_tab, "DLC")
    $ tab_items = _dlc_items_for(dlc_tab)

    add im.Scale(news_bg, config.screen_width, config.screen_height)

    fixed:
        xalign 0.5
        yalign 0.52
        xsize panel_w
        ysize panel_h

        add Solid("#6b3aa8") xsize panel_w ysize panel_h
        add Solid("#2b2440dd") xpos 6 ypos 6 xsize (panel_w - 12) ysize (panel_h - 12)

        frame:
            background Solid("#4a2f72")
            xpos 28
            ypos 24
            xsize (panel_w - 56)
            ysize 120
            padding (16, 14)

            text "DLC Library":
                style "dlc_header_title"
                xalign 0.5
                yalign 0.5

        textbutton "Dev":
            style "dlc_tab_button"
            text_style "dlc_tab_button_text"
            xpos (panel_w - 180)
            ypos 38
            xsize 120
            ysize 56
            action ToggleScreenVariable("show_dlc_dev")

        frame:
            background Solid("#241d36dd")
            xpos 28
            ypos 162
            xsize 300
            ysize 610
            padding (14, 14)

            vbox:
                spacing 12

                text "Categories":
                    style "news_body"
                    size 28
                    xalign 0.5

                for tab_id, tab_name in DLC_TABS:
                    textbutton tab_name:
                        style "dlc_tab_button"
                        text_style "dlc_tab_button_text"
                        xfill True
                        action SetScreenVariable("dlc_tab", tab_id)
                        selected (dlc_tab == tab_id)

        frame:
            background Solid("#19152add")
            xpos 346
            ypos 162
            xsize (panel_w - 374)
            ysize 610
            padding (18, 14)

            vbox:
                spacing 10

                text "[tab_label]":
                    style "news_title"
                    size 36
                    xalign 0.0

                viewport:
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    xfill True
                    yfill True

                    vbox:
                        spacing 12

                        if tab_items:
                            for item in tab_items:
                                $ item_id = item.get("id", "")
                                $ item_owned = dlc_is_owned(item_id)
                                $ item_action = (
                                    Confirm(
                                        "Play Summer Festival DLC now?",
                                        yes=[Hide("extra_dlc_menu"), Jump("dlc_summer_festival_router")],
                                        no=NullAction()
                                    )
                                    if (item_id == "summer_festival_dlc" and item_owned) else
                                    (Notify("You do not own this DLC.") if (item_id == "summer_festival_dlc" and not item_owned) else NullAction())
                                )

                                button:
                                    background Solid("#3b2d58cc")
                                    hover_background Solid("#4d3a72dd")
                                    xfill True
                                    ysize 130
                                    action item_action
                                    padding (16, 12)

                                    hbox:
                                        spacing 20
                                        xfill True

                                        vbox:
                                            xsize 860
                                            spacing 8
                                            text item.get("name", "DLC") style "dlc_card_title"
                                            text item.get("desc", "") style "dlc_card_body" xfill True

                                        frame:
                                            background Solid("#ffffff18")
                                            xsize 220
                                            ysize 86
                                            padding (12, 10)
                                            xalign 1.0
                                            yalign 0.5

                                            vbox:
                                                spacing 6
                                                xalign 0.5
                                                yalign 0.5

                                                if item_owned:
                                                    text "Owned" style "dlc_status_owned" xalign 0.5
                                                else:
                                                    text "Not Owned" style "dlc_status_locked" xalign 0.5

                                                text "ID: [item_id]" style "news_cloud_text" size 16 xalign 0.5
                        else:
                            text "No DLC entries found for this category." style "dlc_card_body"

        if show_dlc_dev:
            frame:
                background Solid("#120e1fd8")
                xpos 420
                ypos 214
                xsize 1120
                ysize 500
                padding (16, 14)

                vbox:
                    spacing 10

                    text "DLC Ownership Debug":
                        style "news_title"
                        size 34

                    text "Toggle ownership for testing. This writes to persistent.dlc_owned_ids.":
                        style "news_body"
                        size 20

                    viewport:
                        mousewheel True
                        draggable True
                        scrollbars "vertical"
                        xfill True
                        yfill True

                        vbox:
                            spacing 8
                            for item in DLC_ITEMS:
                                hbox:
                                    spacing 14
                                    xfill True

                                    text item.get("name", "DLC") style "dlc_card_body" xsize 700

                                    text ("Owned" if dlc_is_owned(item.get("id", "")) else "Not Owned"):
                                        style ("dlc_status_owned" if dlc_is_owned(item.get("id", "")) else "dlc_status_locked")
                                        xsize 160

                                    use ui_png_button(
                                        ("Revoke" if dlc_is_owned(item.get("id", "")) else "Grant"),
                                        Function(dlc_set_owned, item.get("id", ""), (not dlc_is_owned(item.get("id", "")))),
                                        zoom=0.40,
                                        text_style="ui_btn_text_small",
                                        use_alt=mm_alt
                                    )

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 16
        use ui_png_button(L("pref_button_back"), ShowMenu("extra_menu"), zoom=0.55, text_style="ui_btn_text_small", use_alt=mm_alt)


label dlc_summer_festival_router:
    if renpy.has_label("dlc_summer_festival_start"):
        jump dlc_summer_festival_start

    "Summer Festival DLC script could not be loaded."
    "Try restarting the game once so Ren'Py recompiles new script files."
    jump _main_menu
