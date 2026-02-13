# custom_extra_menu.rpy
# Extra menu hub + destination pages.

init -2 python:
    def _extra_panel(title, subtitle=""):
        return {"title": title, "subtitle": subtitle}


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


screen extra_menu():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)

    add Solid("#120d20aa")

    text "EXTRA MENU" style "extra_title":
        xalign 0.5
        ypos 46

    # 2x2 hub buttons.
    grid 2 2:
        xalign 0.5
        yalign 0.52
        xspacing 90
        yspacing 70

        use ui_png_button("IMAGE GALLERY", ShowMenu("extra_image_gallery"), zoom=0.95, text_style="ui_btn_text", use_alt=mm_alt)
        use ui_png_button("MUSIC GALLERY", ShowMenu("music_room", mr=music_room), zoom=0.95, text_style="ui_btn_text", use_alt=mm_alt)
        use ui_png_button("ACHIEVEMENTS", ShowMenu("extra_achievements"), zoom=0.95, text_style="ui_btn_text", use_alt=mm_alt)
        use ui_png_button("CREDITS", ShowMenu("extra_credits"), zoom=0.95, text_style="ui_btn_text", use_alt=mm_alt)

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22
        use ui_png_button("RETURN", ShowMenu("main_menu"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)


screen extra_image_gallery():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    add Solid("#120d20bb")

    text "IMAGE GALLERY" style "extra_title":
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
            text "Gallery page is ready." style "extra_subtitle"
            text "Add your gallery unlocks/content here.\nIf you already have a gallery screen, you can route this button to it." style "extra_body"

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22
        use ui_png_button("BACK", ShowMenu("extra_menu"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)


screen extra_music_gallery():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    add Solid("#120d20bb")

    text "MUSIC GALLERY" style "extra_title":
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
            text "Music gallery page is ready." style "extra_subtitle"
            text "Hook this page into your music room / jukebox entries." style "extra_body"

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22
        use ui_png_button("BACK", ShowMenu("extra_menu"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)


screen extra_achievements():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    add Solid("#120d20bb")

    text "ACHIEVEMENTS" style "extra_title":
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
            text "Achievements page is ready." style "extra_subtitle"
            text "Display unlocked achievements and progress here." style "extra_body"

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22
        use ui_png_button("BACK", ShowMenu("extra_menu"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)


screen extra_credits():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    add Solid("#120d20bb")

    text "CREDITS" style "extra_title":
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
            text "Credits page is ready." style "extra_subtitle"
            text "Project and contributor credits can go here." style "extra_body"

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22
        use ui_png_button("BACK", ShowMenu("extra_menu"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)
