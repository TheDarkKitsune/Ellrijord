# custom_extra_menu.rpy
# Extra menu hub + destination pages.

init -2 python:
    import os
    LOCKED_GALLERY_TILE = "gui/gallery/locked_tile.png"
    LOCKED_GALLERY_TILE_FALLBACK = "gui/window_icon.png"

    def _extra_panel(title, subtitle=""):
        return {"title": title, "subtitle": subtitle}

    def _gallery_items(folder_prefix):
        exts = (".png", ".jpg", ".jpeg", ".webp")
        items = []
        for f in renpy.list_files():
            if not f.startswith(folder_prefix + "/"):
                continue
            if os.path.splitext(f)[1].lower() not in exts:
                continue
            name = os.path.splitext(os.path.basename(f))[0].replace("_", " ")
            items.append({"name": name, "path": f})
        items.sort(key=lambda i: i["name"].lower())
        return items

    def _gallery_with_placeholders(folder_prefix, label_prefix, count=12):
        items = _gallery_items(folder_prefix)
        if items:
            return items
        ph = "gui/mainmenu_bg.png"
        if not renpy.loadable(ph):
            ph = "gui/mainmenu_bg2.png" if renpy.loadable("gui/mainmenu_bg2.png") else "gui/window_icon.png"
        return [{"name": "{} {}".format(label_prefix, i + 1), "path": ph} for i in range(count)]

    def _gallery_items_from_list(paths):
        items = []
        for p in paths:
            if renpy.loadable(p):
                name = os.path.splitext(os.path.basename(p))[0].replace("_", " ")
                items.append({"name": name, "path": p})
        return items


style extra_title is text:
    font "fonts/trotes/Trotes.ttf"
    size 72
    color "#ffffff"
    outlines [(4, "#6b3aa8", 0, 0)]

style extra_subtitle is text:
    font "fonts/trotes/Trotes.ttf"
    size 30
    color "#efe5ff"
    outlines [(3, "#5a3192", 0, 0)]

style extra_card_title is text:
    font "fonts/trotes/Trotes.ttf"
    size 38
    color "#ffffff"
    outlines [(3, "#5a3192", 0, 0)]

style extra_body is text:
    font "fonts/trotes/Trotes.ttf"
    size 28
    color "#f3ecff"
    outlines [(2, "#47286f", 0, 0)]

style extra_tab_button is button:
    background Solid("#2b2140ee")
    hover_background Solid("#6b3aa8ee")
    selected_background Solid("#8f50d6ff")
    xpadding 26
    ypadding 10

style extra_tab_button_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 34
    color "#f3ecff"
    outlines [(2, "#47286f", 0, 0)]

style extra_gallery_card is button:
    background Solid("#2a2140ee")
    hover_background Solid("#3a2e57ee")
    xsize 510
    ysize 280
    xpadding 10
    ypadding 10

style extra_gallery_name is text:
    font "fonts/trotes/Trotes.ttf"
    size 26
    color "#f3ecff"
    outlines [(2, "#47286f", 0, 0)]

style extra_page_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 28
    color "#efe5ff"
    outlines [(2, "#47286f", 0, 0)]

style extra_gallery_thumb is fixed:
    xsize 360
    ysize 215

style extra_gallery_hub_card is button:
    background None
    hover_background None
    xsize 420
    ysize 710
    xpadding 0
    ypadding 0

style extra_gallery_hub_title is text:
    font "fonts/trotes/Trotes.ttf"
    size 32
    color "#2c2c32"
    outlines []


screen extra_menu():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)

    add Solid("#120d20aa")

    text L("extra_menu_title") style "extra_title":
        xalign 0.5
        ypos 46

    # 2x2 hub buttons.
    grid 2 2:
        xalign 0.5
        yalign 0.52
        xspacing 90
        yspacing 70

        use ui_png_button(L("extra_image_gallery"), ShowMenu("extra_image_gallery"), zoom=0.95, text_style="ui_btn_text", use_alt=mm_alt)
        use ui_png_button(L("extra_music_gallery"), ShowMenu("music_room", mr=music_room), zoom=0.95, text_style="ui_btn_text", use_alt=mm_alt)
        use ui_png_button(L("extra_achievements"), ShowMenu("achievement_gallery"), zoom=0.95, text_style="ui_btn_text", use_alt=mm_alt)
        use ui_png_button(L("extra_credits"), ShowMenu("extra_credits"), zoom=0.95, text_style="ui_btn_text", use_alt=mm_alt)

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22
        use ui_png_button(L("extra_return"), ShowMenu("main_menu"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)


screen extra_image_gallery():
    tag menu
    $ char_cfg_items = _gallery_items_from_list(gallery_character_images)
    $ gameplay_cfg_items = _gallery_items_from_list(gallery_gameplay_images)
    $ secret_cfg_items = _gallery_items_from_list(gallery_secret_images)
    $ extra_cfg_items = _gallery_items_from_list(gallery_extra_images)
    $ chars_preview = (char_cfg_items[0]["path"] if char_cfg_items else _gallery_with_placeholders("gui/gallery/characters", "Character", 1)[0]["path"])
    $ gameplay_preview = (gameplay_cfg_items[0]["path"] if gameplay_cfg_items else _gallery_with_placeholders("gui/gallery/gameplay", "Gameplay", 1)[0]["path"])
    $ secret_preview = (secret_cfg_items[0]["path"] if secret_cfg_items else _gallery_with_placeholders("gui/gallery/secret", "Secret", 1)[0]["path"])
    $ extra_preview = (extra_cfg_items[0]["path"] if extra_cfg_items else _gallery_with_placeholders("gui/gallery/extra", "Extra", 1)[0]["path"])

    add Solid("#e8d4dd")

    textbutton "GALLERY  >":
        action NullAction()
        xpos 48
        ypos 40
        background Frame(Solid("#ead8df"), 8, 8)
        xminimum 320
        yminimum 76
        text_size 48
        text_color "#2b2b31"
        text_xalign 0.5
        text_yalign 0.5

    textbutton "<-":
        action ShowMenu("extra_menu")
        xpos 1820
        ypos 40
        xsize 90
        ysize 90
        background Frame(Solid("#000000"), 45, 45)
        text_size 42
        text_color "#ffffff"
        text_xalign 0.5
        text_yalign 0.5

    hbox:
        xalign 0.5
        ypos 220
        spacing 60

        button style "extra_gallery_hub_card" action ShowMenu("extra_image_gallery_grid", initial_tab="characters"):
            fixed:
                xysize (420, 710)
                add Solid("#111111") xysize (420, 710)
                add Solid("#ead8df") xpos 3 ypos 3 xysize (414, 704)
                add chars_preview fit "contain" xpos 6 ypos 6 xysize (408, 698)

        button style "extra_gallery_hub_card" action ShowMenu("extra_image_gallery_grid", initial_tab="gameplay"):
            fixed:
                xysize (420, 710)
                add Solid("#111111") xysize (420, 710)
                add Solid("#ead8df") xpos 3 ypos 3 xysize (414, 704)
                if gameplay_cfg_items:
                    add gameplay_preview fit "contain" xpos 6 ypos 6 xysize (408, 698)
                else:
                    add (LOCKED_GALLERY_TILE if renpy.loadable(LOCKED_GALLERY_TILE) else LOCKED_GALLERY_TILE_FALLBACK) fit "contain" xpos 6 ypos 6 xysize (408, 698)

        button style "extra_gallery_hub_card" action ShowMenu("extra_image_gallery_grid", initial_tab="secret"):
            fixed:
                xysize (420, 710)
                add Solid("#111111") xysize (420, 710)
                add Solid("#ead8df") xpos 3 ypos 3 xysize (414, 704)
                if secret_cfg_items:
                    add secret_preview fit "contain" xpos 6 ypos 6 xysize (408, 698)
                else:
                    add (LOCKED_GALLERY_TILE if renpy.loadable(LOCKED_GALLERY_TILE) else LOCKED_GALLERY_TILE_FALLBACK) fit "contain" xpos 6 ypos 6 xysize (408, 698)

        button style "extra_gallery_hub_card" action ShowMenu("extra_image_gallery_grid", initial_tab="extra"):
            fixed:
                xysize (420, 710)
                add Solid("#111111") xysize (420, 710)
                add Solid("#ead8df") xpos 3 ypos 3 xysize (414, 704)
                if extra_cfg_items:
                    add extra_preview fit "contain" xpos 6 ypos 6 xysize (408, 698)
                else:
                    add (LOCKED_GALLERY_TILE if renpy.loadable(LOCKED_GALLERY_TILE) else LOCKED_GALLERY_TILE_FALLBACK) fit "contain" xpos 6 ypos 6 xysize (408, 698)


screen extra_image_gallery_grid(initial_tab="characters"):
    tag menu
    default ig_tab = initial_tab
    default ig_char_page = 0
    default ig_gameplay_page = 0
    default ig_secret_page = 0
    default ig_extra_page = 0
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))
    $ char_cfg_items = _gallery_items_from_list(gallery_character_images)
    $ gameplay_cfg_items = _gallery_items_from_list(gallery_gameplay_images)
    $ secret_cfg_items = _gallery_items_from_list(gallery_secret_images)
    $ extra_cfg_items = _gallery_items_from_list(gallery_extra_images)
    $ char_items = (char_cfg_items if char_cfg_items else _gallery_with_placeholders("gui/gallery/characters", "Character"))
    $ gameplay_items = (gameplay_cfg_items if gameplay_cfg_items else _gallery_with_placeholders("gui/gallery/gameplay", "Gameplay"))
    $ secret_items = (secret_cfg_items if secret_cfg_items else _gallery_with_placeholders("gui/gallery/secret", "Secret"))
    $ extra_items = (extra_cfg_items if extra_cfg_items else _gallery_with_placeholders("gui/gallery/extra", "Extra"))
    $ items_per_page = 6

    if ig_tab == "characters":
        $ active_items = char_items
        $ active_page = ig_char_page
    elif ig_tab == "gameplay":
        $ active_items = gameplay_items
        $ active_page = ig_gameplay_page
    elif ig_tab == "secret":
        $ active_items = secret_items
        $ active_page = ig_secret_page
    else:
        $ active_items = extra_items
        $ active_page = ig_extra_page

    $ total_pages = max(1, (len(active_items) + items_per_page - 1) // items_per_page)
    $ active_page = min(active_page, total_pages - 1)
    $ page_start = active_page * items_per_page
    $ page_items = active_items[page_start:page_start + items_per_page]
    $ tab_name = ("Character Images" if ig_tab == "characters" else ("Gameplay Images" if ig_tab == "gameplay" else ("Secret Images" if ig_tab == "secret" else "Extra")))

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    add Solid("#120d20bb")

    text L("extra_image_gallery") style "extra_title":
        xalign 0.5
        ypos 70

    frame:
        background Solid("#2b2140dd")
        xalign 0.5
        yalign 0.525
        xsize 1700
        ysize 790
        padding (30, 24)

        vbox:
            spacing 20

            text tab_name style "extra_subtitle":
                xalign 0.5

            vpgrid:
                cols 3
                rows 2
                xspacing 24
                yspacing 22
                xalign 0.5
                yalign 0.5

                for item in page_items:
                    button action NullAction():
                        style "extra_gallery_card"
                        xsize 510
                        ysize 280
                        vbox:
                            spacing 10
                            fixed style "extra_gallery_thumb":
                                add item["path"] fit "contain" xysize (360, 215) xalign 0.5 yalign 0.5
                            text item["name"] style "extra_gallery_name" xalign 0.5

            hbox:
                spacing 20
                xalign 0.5
                textbutton "<" style "extra_tab_button":
                    sensitive active_page > 0
                    action If(
                        ig_tab == "characters",
                        SetScreenVariable("ig_char_page", active_page - 1),
                        If(
                            ig_tab == "gameplay",
                            SetScreenVariable("ig_gameplay_page", active_page - 1),
                            If(
                                ig_tab == "secret",
                                SetScreenVariable("ig_secret_page", active_page - 1),
                                SetScreenVariable("ig_extra_page", active_page - 1)
                            )
                        )
                    )
                text "Page [active_page + 1] / [total_pages]" style "extra_page_text"
                textbutton ">" style "extra_tab_button":
                    sensitive active_page < (total_pages - 1)
                    action If(
                        ig_tab == "characters",
                        SetScreenVariable("ig_char_page", active_page + 1),
                        If(
                            ig_tab == "gameplay",
                            SetScreenVariable("ig_gameplay_page", active_page + 1),
                            If(
                                ig_tab == "secret",
                                SetScreenVariable("ig_secret_page", active_page + 1),
                                SetScreenVariable("ig_extra_page", active_page + 1)
                            )
                        )
                    )

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22
        use ui_png_button(L("pref_button_back"), ShowMenu("extra_image_gallery"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)


screen extra_music_gallery():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    add Solid("#120d20bb")

    text L("extra_music_gallery") style "extra_title":
        xalign 0.5
        ypos 70

    frame:
        background Solid("#2b2140dd")
        xalign 0.5
        yalign 0.52
        xsize 1300
        ysize 560
        padding (40, 30)

        vbox:
            spacing 18
            text L("extra_music_gallery_subtitle") style "extra_subtitle"
            text L("extra_music_gallery_body") style "extra_body"

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22
        use ui_png_button(L("pref_button_back"), ShowMenu("extra_menu"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)


screen extra_achievements():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    add Solid("#120d20bb")

    text L("extra_achievements") style "extra_title":
        xalign 0.5
        ypos 70

    frame:
        background Solid("#2b2140dd")
        xalign 0.5
        yalign 0.52
        xsize 1300
        ysize 560
        padding (40, 30)

        vbox:
            spacing 18
            text L("extra_achievements_subtitle") style "extra_subtitle"
            text L("extra_achievements_body") style "extra_body"

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22
        use ui_png_button(L("pref_button_back"), ShowMenu("extra_menu"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)


screen extra_credits():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    add Solid("#120d20bb")

    text L("extra_credits") style "extra_title":
        xalign 0.5
        ypos 70

    frame:
        background Solid("#2b2140dd")
        xalign 0.5
        yalign 0.52
        xsize 1300
        ysize 560
        padding (40, 30)

        vbox:
            spacing 18
            text L("extra_credits_subtitle") style "extra_subtitle"
            text L("extra_credits_body") style "extra_body"

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22
        use ui_png_button(L("pref_button_back"), ShowMenu("extra_menu"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)
