# custom_save_files.rpy
# Custom save/load layout.

init -2 python:
    SAVE_SLOT_COUNT = 11

default save_ui_selected_slot = 1
default persistent.save_slot_playtime = {}

init -2 python:
    def _save_playtime_map():
        raw = getattr(persistent, "save_slot_playtime", None)
        if not isinstance(raw, dict):
            raw = {}
        persistent.save_slot_playtime = raw
        return raw

    def _record_slot_playtime(slot):
        m = _save_playtime_map()
        try:
            s = int(slot)
        except Exception:
            return
        m[s] = int(max(0, renpy.get_game_runtime()))
        persistent.save_slot_playtime = m
        renpy.save_persistent()

    def _clear_slot_playtime(slot):
        m = _save_playtime_map()
        try:
            s = int(slot)
        except Exception:
            return
        if s in m:
            del m[s]
            persistent.save_slot_playtime = m
            renpy.save_persistent()

    def _slot_playtime_text(slot):
        m = _save_playtime_map()
        try:
            s = int(slot)
        except Exception:
            return "--:--:--"
        secs = int(m.get(s, 0) or 0)
        h = secs // 3600
        mnt = (secs % 3600) // 60
        sec = secs % 60
        return "{:02d}:{:02d}:{:02d}".format(h, mnt, sec) if secs > 0 else "--:--:--"


style save_title is text:
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
    size 46
    color "#f7e9ff"
    outlines [(3, "#6b3aa8", 0, 0)]

style save_nav_button is button:
    background None
    hover_background None
    insensitive_background None
    xpadding 10
    ypadding 6

style save_nav_text is text:
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
    size 54
    color "#c9aa83"
    outlines [(2, "#2a1d14", 0, 0)]
    hover_color "#e4c79f"

style save_slot_text is text:
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
    size 34
    color "#efe5ff"
    outlines [(2, "#5a3192", 0, 0)]

style save_slot_text_selected is save_slot_text:
    color "#ffffff"
    outlines [(3, "#6b3aa8", 0, 0)]

style save_meta_label is text:
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
    size 30
    color "#efe5ff"
    outlines [(3, "#5a3192", 0, 0)]

style save_meta_value is text:
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
    size 28
    color "#f3ecff"
    outlines [(2, "#47286f", 0, 0)]

style save_slot_button is button:
    background None
    hover_background Solid("#ffffff0f")
    selected_background Solid("#ffffff18")
    selected_hover_background Solid("#ffffff24")
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
    $ selected_slot = int(save_ui_selected_slot) if save_ui_selected_slot else 1
    $ selected_slot = max(1, min(SAVE_SLOT_COUNT, selected_slot))
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))
    $ title = L("save_title_save") if mode == "save" else L("save_title_load")
    $ action_label = L("save_action_overwrite") if mode == "save" else L("save_action_load")
    $ can_open = (mode == "save") or FileLoadable(selected_slot)

    add im.Scale(get_main_menu_bg_path(), config.screen_width, config.screen_height)

    add Solid("#120d20bb")

    text title:
        style "save_title"
        xpos 280
        ypos 58

    # Save slots list (no scrollbar).
    fixed:
        xpos 120
        ypos 150
        xsize 760
        ysize 760

        vbox:
            spacing 14

            for i in range(1, SAVE_SLOT_COUNT + 1):
                $ slot_name = (("{0} {1} - {2}".format(L("save_slot_prefix"), i, FileSaveName(i, empty=L("save_empty_slot")))) if FileLoadable(i) else L("save_empty_slot"))
                button:
                    style "save_slot_button"
                    selected (i == selected_slot)
                    action SetVariable("save_ui_selected_slot", i)
                    xsize 720
                    ysize 54

                    hbox:
                        xpos 14
                        yalign 0.5
                        spacing 16
                        text "*" style ("save_slot_text_selected" if i == selected_slot else "save_slot_text") yalign 0.5
                        if i == selected_slot:
                            text slot_name style "save_slot_text_selected" yalign 0.5
                        else:
                            text slot_name style "save_slot_text" yalign 0.5

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
                fixed:
                    xfill True
                    yfill True
                    clipping True
                    add FileScreenshot(selected_slot) fit "cover" xalign 0.5 yalign 0.5

        fixed:
            xpos 220
            ypos 450
            xsize 440
            ysize 74
            use ui_png_button(
                (L("save_action_load") if mode == "load" else "SAVE GAME"),
                (FileAction(selected_slot) if mode == "load" else [Function(_record_slot_playtime, selected_slot), FileSave(selected_slot)]),
                xsize=440,
                ysize=74,
                text_style="ui_btn_text_small",
                use_alt=mm_alt,
                disabled=((not can_open) if mode == "load" else False)
            )

        text L("save_time_label") style "save_meta_label":
            xpos 0
            ypos 544
        text FileTime(selected_slot, format="%d/%m/%Y - %H:%M", empty="--") style "save_meta_value":
            xpos 0
            ypos 592

        text L("play_time_label") style "save_meta_label":
            xpos 540
            ypos 544
        text _slot_playtime_text(selected_slot) style "save_meta_value":
            xpos 540
            ypos 592

        fixed:
            xpos 0
            ypos 690
            xsize 360
            ysize 58
            use ui_png_button(L("save_action_overwrite"), [Function(_record_slot_playtime, selected_slot), FileSave(selected_slot)], xsize=360, ysize=58, text_style="ui_btn_text_small", use_alt=mm_alt, disabled=(mode != "save"))

        fixed:
            xpos 540
            ypos 690
            xsize 320
            ysize 58
            use ui_png_button(L("save_action_delete"), [Function(_clear_slot_playtime, selected_slot), FileDelete(selected_slot)], xsize=320, ysize=58, text_style="ui_btn_text_small", use_alt=mm_alt, disabled=(not FileLoadable(selected_slot)))

    hbox:
        xalign 0.5
        yalign 0.95
        spacing 16
        use ui_png_button(L("pref_button_back"), Return(), xsize=260, ysize=56, text_style="ui_btn_text_small", use_alt=mm_alt)

