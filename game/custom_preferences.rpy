# custom_preferences.rpy
# Uses:
#   gui/game_menu.png
#   gui/logo.png
#   gui/btn_idle.png
#   gui/btn_hover.png
#   fonts/trotes/Trotes.ttf

init -2 python:
    PREF_TAB_ZOOM = 0.6

    PREF_SM_ZOOM = 0.45
    PREF_TINY_ZOOM = 0.32

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

    def set_pref_tooltip(text):
        store.pref_tooltip = text
        mx, my = renpy.get_mouse_pos()
        rect = get_rect_at_pos(mx, my)
        if rect is None:
            rect = (mx, my, 0, 0)
        store.pref_tooltip_rect = rect

    def clear_pref_tooltip():
        store.pref_tooltip = None
        store.pref_tooltip_rect = None

transform pref_thumb_fx:
    zoom 0.4
    yoffset 26

style pref_label is text:
    font "fonts/trotes/Trotes.ttf"
    size 28
    color "#f7e9ff"
    outlines [(3, "#6b3aa8", 0, 0)]
    xalign 0.0

style pref_bar is slider:
    xsize 560
    ysize 80
    base_bar Frame("gui/slider/horizontal_idle_bar.png", gui.slider_borders, tile=gui.slider_tile)
    hover_base_bar Frame("gui/slider/horizontal_hover_bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb At("gui/slider/horizontal_idle_thumb.png", pref_thumb_fx)
    hover_thumb At("gui/slider/horizontal_idle_thumb.png", pref_thumb_fx)

default pref_tooltip = None
default pref_tooltip_rect = None

screen pref_tab_button(label_key, value, current_tab=None, tooltip_key=None):
    $ label = L(label_key)
    $ tooltip = L(tooltip_key) if tooltip_key else label
    use ui_png_button(
        label,
        SetScreenVariable("pref_tab", value),
        zoom=PREF_TAB_ZOOM,
        text_style="ui_btn_text_tab",
        selected=current_tab == value,
        hovered_action=Function(set_pref_tooltip, tooltip),
        unhovered_action=Function(clear_pref_tooltip)
    )

screen pref_small_button(label_key, action, selected=False, tooltip_key=None):
    $ label = L(label_key)
    $ tooltip = L(tooltip_key) if tooltip_key else label
    use ui_png_button(
        label,
        action,
        zoom=PREF_SM_ZOOM,
        text_style="ui_btn_text_small",
        selected=selected,
        hovered_action=Function(set_pref_tooltip, tooltip),
        unhovered_action=Function(clear_pref_tooltip)
    )

screen pref_tiny_button(label, action, selected=False, tooltip=None):
    use ui_png_button(
        label,
        action,
        zoom=PREF_TINY_ZOOM,
        text_style="ui_btn_text_small",
        selected=selected,
        hovered_action=Function(set_pref_tooltip, tooltip) if tooltip else None,
        unhovered_action=Function(clear_pref_tooltip) if tooltip else None
    )

screen pref_icon_button(img, action, tooltip_key=None):
    $ tooltip = L(tooltip_key) if tooltip_key else None
    imagebutton:
        xysize (68, 68)
        background "#2a2836"
        idle Transform(img, xysize=(68, 68))
        hover_foreground "#f003"
        action action
        hovered Function(set_pref_tooltip, tooltip)

screen pref_add_binding_button(action, tooltip_key=None):
    $ tooltip = L(tooltip_key) if tooltip_key else None
    textbutton L("pref_button_add_binding"):
        yalign 0.5 xysize (68, 68)
        text_align (0.5, 0.5)
        background "#2a2836"
        hover_background "#ff8335"
        action action
        hovered Function(set_pref_tooltip, tooltip)

screen preferences():

    tag menu

    default pref_tab = "audio"
    default pref_remapper = pad_remap.ControllerRemap()
    default pref_yadj = ui.adjustment()
    default pref_access_yadj = ui.adjustment()

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
        use pref_tab_button("pref_tab_display", "display", pref_tab, "pref_tip_tab_display")
        use pref_tab_button("pref_tab_audio", "audio", pref_tab, "pref_tip_tab_audio")
        use pref_tab_button("pref_tab_controls", "controls", pref_tab, "pref_tip_tab_controls")
        use pref_tab_button("pref_tab_access", "access", pref_tab, "pref_tip_tab_access")

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
                        text L("pref_label_mute_all") style "pref_label"
                        use pref_small_button("pref_button_muted", Function(set_all_mute, True), selected=is_all_muted(), tooltip_key="pref_tip_muted")
                        use pref_small_button("pref_button_not_muted", Function(set_all_mute, False), selected=not is_all_muted(), tooltip_key="pref_tip_not_muted")

                    if config.has_music:
                        vbox:
                            spacing 8
                            text L("pref_label_music_volume") style "pref_label"
                            bar value Preference("music volume") style "pref_bar"

                    if config.has_sound:
                        vbox:
                            spacing 8
                            text L("pref_label_sfx_volume") style "pref_label"
                            bar value Preference("sound volume") style "pref_bar"

                    if config.has_voice:
                        vbox:
                            spacing 8
                            text L("pref_label_voice_volume") style "pref_label"
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
                    text L("pref_label_display") style "pref_label":
                        xpos left_x
                        ypos row_y
                    fixed:
                        xpos on_x
                        ypos (row_y - 8)
                        use pref_small_button("pref_button_window", Preference("display", "window"), selected=not preferences.fullscreen, tooltip_key="pref_tip_window")
                    fixed:
                        xpos off_x
                        ypos (row_y - 8)
                        use pref_small_button("pref_button_fullscreen", Preference("display", "fullscreen"), selected=preferences.fullscreen, tooltip_key="pref_tip_fullscreen")

                    $ row_y = 150
                    text L("pref_label_skip_unseen") style "pref_label":
                        xpos left_x
                        ypos row_y
                    fixed:
                        xpos on_x
                        ypos (row_y - 8)
                        use pref_small_button("pref_button_on", SetField(preferences, "skip_unseen", True), selected=preferences.skip_unseen, tooltip_key="pref_tip_skip_unseen_on")
                    fixed:
                        xpos off_x
                        ypos (row_y - 8)
                        use pref_small_button("pref_button_off", SetField(preferences, "skip_unseen", False), selected=not preferences.skip_unseen, tooltip_key="pref_tip_skip_unseen_off")

                    $ row_y = 270
                    text L("pref_label_skip_after_choices") style "pref_label":
                        xpos left_x
                        ypos row_y
                    fixed:
                        xpos on_x
                        ypos (row_y - 8)
                        use pref_small_button("pref_button_on", SetField(preferences, "skip_after_choices", True), selected=preferences.skip_after_choices, tooltip_key="pref_tip_skip_after_choices_on")
                    fixed:
                        xpos off_x
                        ypos (row_y - 8)
                        use pref_small_button("pref_button_off", SetField(preferences, "skip_after_choices", False), selected=not preferences.skip_after_choices, tooltip_key="pref_tip_skip_after_choices_off")

                    $ row_y = 410
                    text L("pref_label_text_speed") style "pref_label":
                        xpos left_x
                        ypos row_y
                    text L("pref_label_min") style "pref_label":
                        xpos min_x
                        ypos row_y
                    bar value Preference("text speed") style "pref_bar":
                        xpos slider_x
                        ypos (row_y - 8)
                    text L("pref_label_max") style "pref_label":
                        xpos max_x
                        ypos row_y

                    $ row_y = 540
                    text L("pref_label_auto_forward") style "pref_label":
                        xpos left_x
                        ypos row_y
                    text L("pref_label_min") style "pref_label":
                        xpos min_x
                        ypos row_y
                    bar value Preference("auto-forward time") style "pref_bar":
                        xpos slider_x
                        ypos (row_y - 8)
                    text L("pref_label_max") style "pref_label":
                        xpos max_x
                        ypos row_y

                    # (Transitions toggle omitted here to match the reference layout.)

            elif pref_tab == "access":
                $ left_x = 60
                $ on_x = 650
                $ off_x = 980
                $ min_x = 650
                $ slider_x = 730
                $ max_x = 1280

                side "c r":
                    viewport:
                        id "pref_access_vp"
                        xysize (1480, 640)
                        mousewheel True
                        draggable True
                        yadjustment pref_access_yadj
                        has vbox
                        spacing 36

                        fixed:
                            xsize 1480
                            ysize 90
                            text "FONT OVERRIDE" style "pref_label":
                                xpos left_x
                                ypos 10
                            fixed:
                                xpos on_x
                                ypos 0
                                use pref_small_button("DEFAULT", Preference("font transform", None), selected=(getattr(preferences, "font_transform", None) is None))
                            fixed:
                                xpos off_x
                                ypos 0
                                use pref_small_button("DEJAVU SANS", Preference("font transform", "dejavusans"), selected=(getattr(preferences, "font_transform", None) == "dejavusans"))

                        fixed:
                            xsize 1480
                            ysize 80
                            fixed:
                                xpos on_x
                                ypos 0
                                use pref_small_button("OPENDYSLEXIC", Preference("font transform", "opendyslexic"), selected=(getattr(preferences, "font_transform", None) == "opendyslexic"))

                        fixed:
                            xsize 1480
                            ysize 90
                            text "TEXT SIZE SCALING" style "pref_label":
                                xpos left_x
                                ypos 10
                            text "MIN" style "pref_label":
                                xpos min_x
                                ypos 10
                            bar value Preference("font size") style "pref_bar":
                                xpos slider_x
                                ypos 0
                            text "MAX" style "pref_label":
                                xpos max_x
                                ypos 10

                        fixed:
                            xsize 1480
                            ysize 90
                            text "LINE SPACE SCALING" style "pref_label":
                                xpos left_x
                                ypos 10
                            text "MIN" style "pref_label":
                                xpos min_x
                                ypos 10
                            bar value Preference("font line spacing") style "pref_bar":
                                xpos slider_x
                                ypos 0
                            text "MAX" style "pref_label":
                                xpos max_x
                                ypos 10

                        fixed:
                            xsize 1480
                            ysize 90
                            text "HIGH CONTRAST TEXT" style "pref_label":
                                xpos left_x
                                ypos 10
                            fixed:
                                xpos on_x
                                ypos 0
                                use pref_small_button("ON", Preference("high contrast text", "enable"), selected=getattr(preferences, "high_contrast_text", False))
                            fixed:
                                xpos off_x
                                ypos 0
                                use pref_small_button("OFF", Preference("high contrast text", "disable"), selected=not getattr(preferences, "high_contrast_text", False))

                        fixed:
                            xsize 1480
                            ysize 90
                            text "SELF-VOICING" style "pref_label":
                                xpos left_x
                                ypos 10
                            fixed:
                                xpos on_x
                                ypos 0
                                use pref_small_button("TEXT-TO-SPEECH", Preference("self voicing", "enable"), selected=getattr(preferences, "self_voicing", False))
                            fixed:
                                xpos off_x
                                ypos 0
                                use pref_small_button("CLIPBOARD", Preference("clipboard voicing", "enable"), selected=getattr(preferences, "clipboard_voicing", False))

                        fixed:
                            xsize 1480
                            ysize 90
                            text "DEBUG" style "pref_label":
                                xpos left_x
                                ypos 10
                            fixed:
                                xpos on_x
                                ypos 0
                                use pref_small_button("ON", Preference("debug voicing", "enable"), selected=getattr(preferences, "debug_voicing", False))
                            fixed:
                                xpos off_x
                                ypos 0
                                use pref_small_button("OFF", Preference("debug voicing", "disable"), selected=not getattr(preferences, "debug_voicing", False))

                        fixed:
                            xsize 1480
                            ysize 90
                            text "VOICE VOLUME" style "pref_label":
                                xpos left_x
                                ypos 10
                            text "MIN" style "pref_label":
                                xpos min_x
                                ypos 10
                            bar value Preference("voice volume") style "pref_bar":
                                xpos slider_x
                                ypos 0
                            text "MAX" style "pref_label":
                                xpos max_x
                                ypos 10

                        fixed:
                            xsize 1480
                            ysize 90
                            text "SELF-VOICING VOLUME DROP" style "pref_label":
                                xpos left_x
                                ypos 10
                            text "MIN" style "pref_label":
                                xpos min_x
                                ypos 10
                            bar value Preference("self voicing volume drop") style "pref_bar":
                                xpos slider_x
                                ypos 0
                            text "MAX" style "pref_label":
                                xpos max_x
                                ypos 10

                    vbar value YScrollValue("pref_access_vp") keyboard_focus False

            elif pref_tab == "controls":
                vbox:
                    spacing 14

                    hbox:
                        spacing 18
                        use pref_small_button("pref_button_calibrate_gamepad", GamepadCalibrate(), tooltip_key="pref_tip_calibrate_gamepad")
                        use pref_small_button("pref_button_change_icon_set", CycleControllerLayout(), tooltip_key="pref_tip_change_icon_set")

                    side "c r":
                        controller_viewport:
                            xysize (1440, 520)
                            mousewheel True
                            draggable True
                            shortcuts True
                            id "pref_controls_viewport"
                            yadjustment pref_yadj
                            has vbox
                            spacing 26

                            fixed:
                                xsize 1360
                                ysize 70
                                text "HOLD TO SKIP" style "pref_label":
                                    xpos 0
                                    ypos 8
                                fixed:
                                    xpos 560
                                    ypos 0
                                    use pref_tiny_button("ON", SetField(persistent, "hold_to_skip", True), selected=persistent.hold_to_skip, tooltip="Hold button to keep skipping")
                                fixed:
                                    xpos 770
                                    ypos 0
                                    use pref_tiny_button("OFF", SetField(persistent, "hold_to_skip", False), selected=not persistent.hold_to_skip, tooltip="Tap to toggle skipping")

                            fixed:
                                xsize 1360
                                ysize 70
                                text "LEFT STICK X-AXIS" style "pref_label":
                                    xpos 0
                                    ypos 8
                                fixed:
                                    xpos 560
                                    ypos 0
                                    use pref_tiny_button("NORMAL", SetStickInversion("left", "x", False), selected=not persistent.left_stick_invert_x, tooltip="Normal left stick x-axis")
                                fixed:
                                    xpos 770
                                    ypos 0
                                    use pref_tiny_button("INVERTED", SetStickInversion("left", "x", True), selected=persistent.left_stick_invert_x, tooltip="Invert left stick x-axis")

                            fixed:
                                xsize 1360
                                ysize 70
                                text "LEFT STICK Y-AXIS" style "pref_label":
                                    xpos 0
                                    ypos 8
                                fixed:
                                    xpos 560
                                    ypos 0
                                    use pref_tiny_button("NORMAL", SetStickInversion("left", "y", False), selected=not persistent.left_stick_invert_y, tooltip="Normal left stick y-axis")
                                fixed:
                                    xpos 770
                                    ypos 0
                                    use pref_tiny_button("INVERTED", SetStickInversion("left", "y", True), selected=persistent.left_stick_invert_y, tooltip="Invert left stick y-axis")

                            fixed:
                                xsize 1360
                                ysize 82
                                text "LEFT STICK DEAD ZONE" style "pref_label":
                                    xpos 0
                                    ypos 12
                                text "MIN" style "pref_label":
                                    xpos 560
                                    ypos 12
                                bar value StickDeadzoneAdjustment("left") style "pref_bar":
                                    xpos 640
                                    ypos 0
                                text "MAX" style "pref_label":
                                    xpos 1210
                                    ypos 12

                            fixed:
                                xsize 1360
                                ysize 82
                                text "LEFT STICK SENSITIVITY" style "pref_label":
                                    xpos 0
                                    ypos 12
                                text "LOW" style "pref_label":
                                    xpos 560
                                    ypos 12
                                bar value StickSensitivityAdjustment("left") style "pref_bar":
                                    xpos 640
                                    ypos 0
                                text "HIGH" style "pref_label":
                                    xpos 1210
                                    ypos 12

                            fixed:
                                xsize 1360
                                ysize 70
                                text "RIGHT STICK X-AXIS" style "pref_label":
                                    xpos 0
                                    ypos 8
                                fixed:
                                    xpos 560
                                    ypos 0
                                    use pref_tiny_button("NORMAL", SetStickInversion("right", "x", False), selected=not persistent.right_stick_invert_x, tooltip="Normal right stick x-axis")
                                fixed:
                                    xpos 770
                                    ypos 0
                                    use pref_tiny_button("INVERTED", SetStickInversion("right", "x", True), selected=persistent.right_stick_invert_x, tooltip="Invert right stick x-axis")

                            fixed:
                                xsize 1360
                                ysize 70
                                text "RIGHT STICK Y-AXIS" style "pref_label":
                                    xpos 0
                                    ypos 8
                                fixed:
                                    xpos 560
                                    ypos 0
                                    use pref_tiny_button("NORMAL", SetStickInversion("right", "y", False), selected=not persistent.right_stick_invert_y, tooltip="Normal right stick y-axis")
                                fixed:
                                    xpos 770
                                    ypos 0
                                    use pref_tiny_button("INVERTED", SetStickInversion("right", "y", True), selected=persistent.right_stick_invert_y, tooltip="Invert right stick y-axis")

                            fixed:
                                xsize 1360
                                ysize 82
                                text "RIGHT STICK DEAD ZONE" style "pref_label":
                                    xpos 0
                                    ypos 12
                                text "MIN" style "pref_label":
                                    xpos 560
                                    ypos 12
                                bar value StickDeadzoneAdjustment("right") style "pref_bar":
                                    xpos 640
                                    ypos 0
                                text "MAX" style "pref_label":
                                    xpos 1210
                                    ypos 12

                            fixed:
                                xsize 1360
                                ysize 82
                                text "RIGHT STICK SENSITIVITY" style "pref_label":
                                    xpos 0
                                    ypos 12
                                text "LOW" style "pref_label":
                                    xpos 560
                                    ypos 12
                                bar value StickSensitivityAdjustment("right") style "pref_bar":
                                    xpos 640
                                    ypos 0
                                text "HIGH" style "pref_label":
                                    xpos 1210
                                    ypos 12

                            null height 12

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
                                            use pref_icon_button(
                                                img[0],
                                                [Function(pref_remapper.remove_button, img[1], act),
                                                    If((act not in pad_remap.REQUIRED_EVENTS
                                                            or len(pad_images) > 1), None,
                                                        Function(renpy.call_in_new_context,
                                                            "listen_for_remap", title, act, pref_yadj,
                                                            pref_remapper))],
                                                tooltip_key="pref_tip_remove_binding"
                                            )
                                        for i in range(3 - len(pad_images)):
                                            use pref_add_binding_button(
                                                Function(renpy.call_in_new_context,
                                                    "listen_for_remap", title, act, pref_yadj,
                                                    pref_remapper),
                                                tooltip_key="pref_tip_add_binding"
                                            )
                        vbar value YScrollValue("pref_controls_viewport") keyboard_focus False

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22

        use pref_small_button("pref_button_main_menu", MainMenu(), tooltip_key="pref_tip_main_menu")
        if main_menu:
            use pref_small_button("pref_button_back", ShowMenu("main_menu"), tooltip_key="pref_tip_back")
        else:
            use pref_small_button("pref_button_back", Return(), tooltip_key="pref_tip_back")
        use pref_small_button("pref_button_default", Function(reset_preferences), tooltip_key="pref_tip_default")

    use ui_tooltip_from_rect(store.pref_tooltip, store.pref_tooltip_rect)
