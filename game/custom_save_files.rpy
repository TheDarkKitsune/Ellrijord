# custom_save_files.rpy
# Custom save/load layout.

init -2 python:
    SAVE_SLOT_COUNT = 12


style save_title is text:
    font "fonts/trotes/Trotes.ttf"
    size 46
    color "#c9aa83"
    outlines [(1, "#2a1d14", 0, 0)]

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
    size 34
    color "#ddd4c7"
    outlines [(1, "#2a1d14", 0, 0)]

style save_slot_text_selected is save_slot_text:
    color "#f1e7d8"

style save_meta_label is text:
    font "fonts/trotes/Trotes.ttf"
    size 30
    color "#efe5ff"
    outlines [(3, "#5a3192", 0, 0)]

style save_meta_value is text:
    font "fonts/trotes/Trotes.ttf"
    size 28
    color "#f3ecff"
    outlines [(2, "#47286f", 0, 0)]

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
    $ action_label = "OVERWRITE SAVE" if mode == "save" else "LOAD GAME"
    $ can_open = (mode == "save") or FileLoadable(selected_slot)

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)

    add Solid("#120d20bb")

    text title:
        style "save_title"
        xpos 280
        ypos 58

    # Save slots list + scrollbar.
    side "c r":
        xpos 120
        ypos 120
        xysize (760, 760)

        viewport:
            id "save_slots_viewport"
            mousewheel True
            draggable True
            yadjustment slots_yadj
            has vbox
            spacing 14

            for i in range(1, SAVE_SLOT_COUNT + 1):
                $ slot_name = ("Save %d — %s" % (i, FileSaveName(i, empty="Empty"))) if FileLoadable(i) else "Empty Slot"
                button:
                    background None
                    hover_background Solid("#ffffff10")
                    action SetScreenVariable("selected_slot", i)
                    xsize 720
                    ysize 54

                    hbox:
                        spacing 16
                        yalign 0.5
                        text "•" style "save_slot_text"
                        if i == selected_slot:
                            text slot_name style "save_slot_text_selected"
                        else:
                            text slot_name style "save_slot_text"

        use ui_vscrollbar_for("save_slots_viewport")

    # Right preview/details column.
    fixed:
        xpos 910
        ypos 150
        xsize 930
        ysize 760

        frame:
            background Solid("#00000066")
            xsize 880
            ysize 420
            padding (4, 4)

            frame:
                background Solid("#f0f0f0dd")
                xfill True
                yfill True
                padding (6, 6)
                add FileScreenshot(selected_slot) xalign 0.5 yalign 0.5

        fixed:
            xpos 220
            ypos 390
            xsize 440
            ysize 74
            use ui_png_button(
                action_label,
                FileAction(selected_slot),
                xsize=440,
                ysize=74,
                text_style="ui_btn_text_small",
                use_alt=mm_alt,
                disabled=(not can_open)
            )

        text "Save Time" style "save_meta_label":
            xpos 0
            ypos 500
        text FileTime(selected_slot, format="%Y.%m.%d. - %H:%M", empty="--") style "save_meta_value":
            xpos 0
            ypos 548

        text "Play Time" style "save_meta_label":
            xpos 540
            ypos 500
        text "00:00:00" style "save_meta_value":
            xpos 540
            ypos 548

        fixed:
            xpos 0
            ypos 626
            xsize 360
            ysize 58
            use ui_png_button("OVERWRITE SAVE", FileSave(selected_slot), xsize=360, ysize=58, text_style="ui_btn_text_small", use_alt=mm_alt, disabled=(mode != "save"))

        fixed:
            xpos 540
            ypos 626
            xsize 320
            ysize 58
            use ui_png_button("DELETE SAVE", FileDelete(selected_slot), xsize=320, ysize=58, text_style="ui_btn_text_small", use_alt=mm_alt, disabled=(not FileLoadable(selected_slot)))

    hbox:
        xalign 0.5
        yalign 0.95
        spacing 16
        use ui_png_button("BACK", Return(), xsize=260, ysize=56, text_style="ui_btn_text_small", use_alt=mm_alt)
