# custom_preferences.rpy
# Uses:
#   gui/game_menu.png
#   gui/logo.png
#   gui/btn_idle.png
#   gui/btn_hover.png
#   fonts/trotes/Trotes.ttf

init -2 python:
    PREF_TAB_ZOOM = 0.6
    PREF_TAB_W = int(534 * PREF_TAB_ZOOM)
    PREF_TAB_H = int(140 * PREF_TAB_ZOOM)

    PREF_SM_ZOOM = 0.45
    PREF_SM_W = int(534 * PREF_SM_ZOOM)
    PREF_SM_H = int(140 * PREF_SM_ZOOM)

    def _fix_mute_pref_type():
        prefdata = getattr(persistent, "_preferences", None)
        if isinstance(prefdata, dict) and isinstance(prefdata.get("mute"), bool):
            val = prefdata.get("mute")
            prefdata["mute"] = {"music": val, "sound": val, "voice": val}

    _fix_mute_pref_type()

    def set_all_mute(value):
        prefs = renpy.game.preferences
        if hasattr(prefs, "mute"):
            prefs.mute = {"music": value, "sound": value, "voice": value}
        for ch in ("music", "sound", "voice"):
            try:
                renpy.music.set_mute(value, channel=ch)
            except Exception:
                pass

    def is_all_muted():
        prefs = renpy.game.preferences
        m = getattr(prefs, "mute", None)
        if isinstance(m, dict):
            return all(m.get(ch, False) for ch in ("music", "sound", "voice"))
        return bool(m)

    def reset_preferences():
        # Use Ren'Py's built-in reset so all audio/mute flags restore correctly.
        try:
            renpy.reset_preferences()
        except Exception:
            pass
        # Explicitly restore key settings we want to enforce.
        prefs = renpy.game.preferences
        if hasattr(prefs, "fullscreen"):
            prefs.fullscreen = config.default_fullscreen
        if hasattr(prefs, "text_cps"):
            prefs.text_cps = 0
        if hasattr(prefs, "afm_time"):
            prefs.afm_time = 15
        if hasattr(prefs, "music_volume"):
            prefs.music_volume = 1.0
        if hasattr(prefs, "sound_volume"):
            prefs.sound_volume = 1.0
        if hasattr(prefs, "voice_volume"):
            prefs.voice_volume = 1.0
        # Ensure audio channels are unmuted and at full volume immediately.
        set_all_mute(False)
        for ch in ("music", "sound", "voice"):
            try:
                renpy.music.set_volume(1.0, channel=ch)
            except Exception:
                pass
        renpy.restart_interaction()

transform pref_tab_idle:
    zoom PREF_TAB_ZOOM

transform pref_tab_hover:
    zoom PREF_TAB_ZOOM

transform pref_sm_idle:
    zoom PREF_SM_ZOOM

transform pref_sm_hover:
    zoom PREF_SM_ZOOM

transform pref_thumb_fx:
    zoom 0.4
    yoffset 26

style pref_label is text:
    font "fonts/trotes/Trotes.ttf"
    size 28
    color "#f7e9ff"
    outlines [(3, "#6b3aa8", 0, 0)]
    xalign 0.0

style pref_tab_button is button:
    xsize PREF_TAB_W
    ysize PREF_TAB_H
    background At("gui/btn_idle.png", pref_tab_idle)
    hover_background At("gui/btn_hover.png", pref_tab_hover)
    selected_background At("gui/btn_hover.png", pref_tab_hover)
    xalign 0.5
    yalign 0.5

style pref_tab_button_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 26
    color "#ffffff"
    outlines [(4, "#6b3aa8", 0, 0)]
    xalign 0.5
    yalign 0.5

style pref_small_button is button:
    xsize PREF_SM_W
    ysize PREF_SM_H
    background At("gui/btn_idle.png", pref_sm_idle)
    hover_background At("gui/btn_hover.png", pref_sm_hover)
    selected_background At("gui/btn_hover.png", pref_sm_hover)
    xalign 0.5
    yalign 0.5

style pref_small_button_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 22
    color "#ffffff"
    outlines [(3, "#6b3aa8", 0, 0)]
    xalign 0.5
    yalign 0.5

style pref_bar is slider:
    xsize 560
    ysize 80
    base_bar Frame("gui/slider/horizontal_idle_bar.png", gui.slider_borders, tile=gui.slider_tile)
    hover_base_bar Frame("gui/slider/horizontal_hover_bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb At("gui/slider/horizontal_idle_thumb.png", pref_thumb_fx)
    hover_thumb At("gui/slider/horizontal_idle_thumb.png", pref_thumb_fx)

screen pref_tab_button(label, value, current_tab=None):
    textbutton label:
        style "pref_tab_button"
        action SetScreenVariable("pref_tab", value)
        selected current_tab == value

screen pref_small_button(label, action, selected=False):
    textbutton label:
        style "pref_small_button"
        action action
        selected selected

screen preferences():

    tag menu

    default pref_tab = "audio"
    default pref_remapper = pad_remap.ControllerRemap()
    default pref_yadj = ui.adjustment()

    add "gui/game_menu.png"

    # Title/logo
    add Transform("gui/logo.png", zoom=0.40):
        xalign 0.5
        yalign 0.0
        yoffset -40

    # Top tabs
    hbox:
        xpos 240
        ypos 120
        spacing 16
        use pref_tab_button("DISPLAY", "display", pref_tab)
        use pref_tab_button("AUDIO", "audio", pref_tab)
        use pref_tab_button("CONTROLS", "controls", pref_tab)
        use pref_tab_button("ACCESS", "access", pref_tab)

    # Content panel
    fixed:
        xpos 240
        ypos 210
        xsize 1560
        ysize 700

        add Solid("#6b3aa8") xsize 1560 ysize 700
        add Solid("#1b1b26cc") xpos 6 ypos 6 xsize 1548 ysize 688

        frame:
            background None
            xpos 6
            ypos 6
            xsize 1548
            ysize 688
            padding (30, 24)

            if pref_tab == "audio":
                vbox:
                    spacing 26

                    hbox:
                        spacing 18
                        text "MUTE ALL" style "pref_label"
                        use pref_small_button("MUTED", Function(set_all_mute, True), selected=is_all_muted())
                        use pref_small_button("NOT MUTED", Function(set_all_mute, False), selected=not is_all_muted())

                    if config.has_music:
                        vbox:
                            spacing 8
                            text "MUSIC VOLUME" style "pref_label"
                            bar value Preference("music volume") style "pref_bar"

                    if config.has_sound:
                        vbox:
                            spacing 8
                            text "SFX VOLUME" style "pref_label"
                            bar value Preference("sound volume") style "pref_bar"

                    if config.has_voice:
                        vbox:
                            spacing 8
                            text "VOICE VOLUME" style "pref_label"
                            bar value Preference("voice volume") style "pref_bar"

            elif pref_tab == "display":
                fixed:
                    xsize 1480
                    ysize 640

                    $ left_x = 80
                    $ on_x = 620
                    $ off_x = 860
                    $ min_x = 620
                    $ slider_x = 700
                    $ max_x = 1280

                    $ row_y = 30
                    text "DISPLAY" style "pref_label":
                        xpos left_x
                        ypos row_y
                    fixed:
                        xpos on_x
                        ypos (row_y - 8)
                        use pref_small_button("WINDOW", Preference("display", "window"), selected=not preferences.fullscreen)
                    fixed:
                        xpos off_x
                        ypos (row_y - 8)
                        use pref_small_button("FULLSCREEN", Preference("display", "fullscreen"), selected=preferences.fullscreen)

                    $ row_y = 150
                    text "SKIP UNSEEN TEXT" style "pref_label":
                        xpos left_x
                        ypos row_y
                    fixed:
                        xpos on_x
                        ypos (row_y - 8)
                        use pref_small_button("ON", SetField(preferences, "skip_unseen", True), selected=preferences.skip_unseen)
                    fixed:
                        xpos off_x
                        ypos (row_y - 8)
                        use pref_small_button("OFF", SetField(preferences, "skip_unseen", False), selected=not preferences.skip_unseen)

                    $ row_y = 270
                    text "SKIP AFTER CHOICES" style "pref_label":
                        xpos left_x
                        ypos row_y
                    fixed:
                        xpos on_x
                        ypos (row_y - 8)
                        use pref_small_button("ON", SetField(preferences, "skip_after_choices", True), selected=preferences.skip_after_choices)
                    fixed:
                        xpos off_x
                        ypos (row_y - 8)
                        use pref_small_button("OFF", SetField(preferences, "skip_after_choices", False), selected=not preferences.skip_after_choices)

                    $ row_y = 410
                    text "TEXT SPEED" style "pref_label":
                        xpos left_x
                        ypos row_y
                    text "MIN" style "pref_label":
                        xpos min_x
                        ypos row_y
                    bar value Preference("text speed") style "pref_bar":
                        xpos slider_x
                        ypos (row_y - 8)
                    text "MAX" style "pref_label":
                        xpos max_x
                        ypos row_y

                    $ row_y = 540
                    text "AUTO-FORWARD DELAY" style "pref_label":
                        xpos left_x
                        ypos row_y
                    text "MIN" style "pref_label":
                        xpos min_x
                        ypos row_y
                    bar value Preference("auto-forward time") style "pref_bar":
                        xpos slider_x
                        ypos (row_y - 8)
                    text "MAX" style "pref_label":
                        xpos max_x
                        ypos row_y

                    # (Transitions toggle omitted here to match the reference layout.)

            elif pref_tab == "access":
                vbox:
                    spacing 22
                    text "SKIP MODE" style "pref_label"

                    bar value FieldValue(preferences, "skip_unseen", range=1) style "pref_bar"
                    hbox:
                        xfill True
                        text "SEEN" style "pref_label"
                        text "ALL" style "pref_label" xalign 1.0

                    null height 10

                    text "SKIP AFTER CHOICES" style "pref_label"
                    use pref_small_button("ON", SetField(preferences, "skip_after_choices", True), selected=preferences.skip_after_choices)
                    use pref_small_button("OFF", SetField(preferences, "skip_after_choices", False), selected=not preferences.skip_after_choices)

                    text "SKIP TRANSITIONS" style "pref_label"
                    use pref_small_button("ON", SetField(preferences, "transitions", True), selected=preferences.transitions)
                    use pref_small_button("OFF", SetField(preferences, "transitions", False), selected=not preferences.transitions)

            elif pref_tab == "controls":
                vbox:
                    spacing 14

                    hbox:
                        spacing 18
                        use pref_small_button("CALIBRATE GAMEPAD BUTTONS", GamepadCalibrate())
                        use pref_small_button("CHANGE ICON SET", CycleControllerLayout())

                    side "c r":
                        controller_viewport:
                            xysize (980, 520)
                            mousewheel True
                            draggable True
                            shortcuts True
                            id "pref_controls_viewport"
                            yadjustment pref_yadj
                            has vbox
                            spacing 14

                            for title, act, p in pad_remap.REMAPPABLE_EVENTS:
                                hbox:
                                    spacing 16
                                    fixed:
                                        xsize 230
                                        ysize 68
                                        text title style "pref_label" xalign 0.0 yalign 0.5
                                    $ pad_images = pad_remap.get_images(act, pref_remapper.get_current_bindings())
                                    grid 3 1:
                                        spacing 12
                                        for i, img in enumerate(pad_images):
                                            imagebutton:
                                                xysize (68, 68)
                                                background "#2a2836"
                                                idle Transform(img[0], xysize=(68, 68))
                                                hover_foreground "#f003"
                                                action [Function(pref_remapper.remove_button, img[1], act),
                                                    If((act not in pad_remap.REQUIRED_EVENTS
                                                            or len(pad_images) > 1), None,
                                                    Function(renpy.call_in_new_context,
                                                        "listen_for_remap", title, act, pref_yadj,
                                                        pref_remapper))]
                                        for i in range(3 - len(pad_images)):
                                            textbutton _("+"):
                                                yalign 0.5 xysize (68, 68)
                                                text_align (0.5, 0.5)
                                                background "#2a2836"
                                                hover_background "#ff8335"
                                                action Function(renpy.call_in_new_context,
                                                    "listen_for_remap", title, act, pref_yadj,
                                                    pref_remapper)
                        vbar value YScrollValue("pref_controls_viewport") keyboard_focus False

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22

        use pref_small_button("MAIN MENU", MainMenu())
        if main_menu:
            use pref_small_button("BACK", ShowMenu("main_menu"))
        else:
            use pref_small_button("BACK", Return())
        use pref_small_button("DEFAULT", Function(reset_preferences))
