# custom_save_files.rpy
# Custom save/load layout.

init -2 python:
    SAVE_SLOT_COUNT = 12


style save_title is text:
    font "fonts/trotes/Trotes.ttf"
    size 52
    color "#c9aa83"
    outlines [(2, "#2a1d14", 0, 0)]

style save_nav_button is button:
    background None
    hover_background None
    insensitive_background None
    xpadding 10
    ypadding 6

style save_nav_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 54
    color "#c9aa83"
    outlines [(2, "#2a1d14", 0, 0)]
    hover_color "#e4c79f"

style save_slot_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 36
    color "#ececec"
    outlines [(2, "#2a1d14", 0, 0)]

style save_meta_label is text:
    font "fonts/trotes/Trotes.ttf"
    size 46
    color "#c9aa83"
    outlines [(2, "#2a1d14", 0, 0)]

style save_meta_value is text:
    font "fonts/trotes/Trotes.ttf"
    size 38
    color "#ececec"
    outlines [(2, "#2a1d14", 0, 0)]

style save_slot_button is button:
    background None
    hover_background Solid("#ffffff0f")
    xpadding 12
    ypadding 6
    xmargin 0
    ymargin 0

style save_slot_button_text is save_slot_text

style save_vscrollbar is vscrollbar:
    xsize 10
    base_bar Solid("#f2d68d1e")
    thumb Solid("#e5c770ee")


screen save():
    tag menu
    use custom_file_slots("save")


screen load():
    tag menu
    use custom_file_slots("load")


screen custom_file_slots(mode="save"):
    tag menu
    default selected_slot = 1
    default slots_yadj = ui.adjustment()
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))
    $ title = "Save Files" if mode == "save" else "Load Files"
    $ action_label = "Overwrite Save" if mode == "save" else "Load Game"
    $ can_open = (mode == "save") or FileLoadable(selected_slot)

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)

    add Solid("#101019cc")

    # Warm haze/tint.
    add Solid("#d2b58a16") xalign 0.5 yalign 1.0 xsize config.screen_width ysize int(config.screen_height * 0.50)

    # Top-right back.
    fixed:
        xpos 1620
        ypos 34
        use ui_png_button("BACK", Return(), zoom=0.48, text_style="ui_btn_text_small", use_alt=mm_alt)

    # Main title.
    text title style "save_title":
        xpos 640
        ypos 130

    # Slot list and scrollbar.
    side "c r":
        xpos 450
        ypos 220
        xysize (600, 700)

        viewport:
            id "save_slots_viewport"
            mousewheel True
            draggable True
            yadjustment slots_yadj
            has vbox
            spacing 6

            for i in range(1, SAVE_SLOT_COUNT + 1):
                $ slot_name = ("Save %d -- %s" % (i, FileSaveName(i, empty="Empty"))) if FileLoadable(i) else "Empty Slot"
                button:
                    style "save_slot_button"
                    action SetScreenVariable("selected_slot", i)
                    xsize 548
                    ysize 62

                    fixed:
                        xsize 548
                        ysize 62

                        if i == selected_slot:
                            add Transform(
                                Frame("gui/btn_idle.png", 24, 8, 24, 8, tile=False),
                                alpha=0.32,
                                xsize=492,
                                ysize=56
                            ):
                                xpos 0
                                ypos 3

                        hbox:
                            spacing 14
                            xpos 8
                            yalign 0.5
                            text ("*" if i == selected_slot else "-") style "save_slot_text"
                            text slot_name style "save_slot_text"

        vbar value YScrollValue("save_slots_viewport") style "save_vscrollbar"

    # Right preview panel.
    frame:
        background Solid("#00000066")
        xpos 1100
        ypos 260
        xsize 700
        ysize 430
        padding (4, 4)

        frame:
            background Solid("#f0f0f0dd")
            xfill True
            yfill True
            padding (6, 6)
            add FileScreenshot(selected_slot) xalign 0.5 yalign 0.5

    # Action button.
    fixed:
        xpos 1240
        ypos 700
        use ui_png_button(action_label, FileAction(selected_slot), zoom=0.62, text_style="ui_btn_text_small", use_alt=mm_alt, disabled=(not can_open))

    # Details and actions row.
    text "Save Time" style "save_meta_label":
        xpos 1080
        ypos 770
    text FileTime(selected_slot, format="%Y.%m.%d. - %H:%M", empty="--") style "save_meta_value":
        xpos 1080
        ypos 840

    text "Play Time" style "save_meta_label":
        xpos 1580
        ypos 770
    text "00:00:00" style "save_meta_value":
        xpos 1620
        ypos 840

    textbutton "Overwrite Save":
        text_style "save_meta_label"
        action FileSave(selected_slot)
        sensitive (mode == "save")
        xpos 1080
        ypos 925

    textbutton "Delete Save":
        text_style "save_meta_label"
        action FileDelete(selected_slot)
        sensitive FileLoadable(selected_slot)
        xpos 1580
        ypos 925
