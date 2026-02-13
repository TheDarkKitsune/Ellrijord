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
    PREF_TABS = ["display", "audio", "controls", "access"]

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
        rect = get_best_rect_at_pos(mx, my)
        if rect is None:
            rect = get_focus_rect()
        if rect is None:
            rect = get_rect_at_pos(mx, my)
        if rect is None:
            rect = (mx, my, 0, 0)
        store.pref_tooltip_rect = rect

    def clear_pref_tooltip():
        store.pref_tooltip = None
        store.pref_tooltip_rect = None

    def pref_L(key):
        if key is None:
            return ""
        txt = L(key)
        if txt != key:
            return txt
        # Fallbacks for common UI keys if localization map isn't loaded yet.
        return {
            "pref_tab_display": "DISPLAY",
            "pref_tab_audio": "AUDIO",
            "pref_tab_controls": "CONTROLS",
            "pref_tab_access": "ACCESS",
            "pref_button_main_menu": "MAIN MENU",
            "pref_button_back": "BACK",
            "pref_button_default": "DEFAULT",
        }.get(key, key)

    def next_pref_tab(current, step):
        try:
            idx = PREF_TABS.index(current)
        except Exception:
            idx = 0
        return PREF_TABS[(idx + step) % len(PREF_TABS)]

style pref_label is text:
    font "fonts/trotes/Trotes.ttf"
    size 20
    color "#f7e9ff"
    outlines [(3, "#6b3aa8", 0, 0)]
    xalign 0.0

style pref_setting_label is pref_label

style pref_setting_btn_text is ui_btn_text_small:
    size 20

style pref_bar is ui_slider_bar

default pref_tooltip = None
default pref_tooltip_rect = None

screen pref_tab_button(label_key, value, current_tab=None, tooltip_key=None, use_alt=None):
    $ label = pref_L(label_key)
    $ tooltip = pref_L(tooltip_key) if tooltip_key else label
    $ _use_alt = bool(getattr(persistent, "mm_alt", False)) if use_alt is None else use_alt
    use ui_png_button(
        label,
        SetScreenVariable("pref_tab", value),
        zoom=PREF_TAB_ZOOM,
        text_style="ui_btn_text_tab",
        use_alt=_use_alt,
        selected=current_tab == value,
        hovered_action=Function(set_pref_tooltip, tooltip),
        unhovered_action=Function(clear_pref_tooltip)
    )

screen pref_small_button(label_key, action, selected=False, tooltip_key=None, use_alt=None, text_style="pref_setting_btn_text", button_id=None, xsize=None, ysize=None):
    $ label = pref_L(label_key)
    $ tooltip = pref_L(tooltip_key) if tooltip_key else label
    $ _use_alt = bool(getattr(persistent, "mm_alt", False)) if use_alt is None else use_alt
    use ui_png_button(
        label,
        action,
        zoom=PREF_SM_ZOOM,
        xsize=xsize,
        ysize=ysize,
        text_style=text_style,
        use_alt=_use_alt,
        button_id=button_id,
        selected=selected,
        hovered_action=Function(set_pref_tooltip, tooltip),
        unhovered_action=Function(clear_pref_tooltip)
    )

screen pref_tiny_button(label, action, selected=False, tooltip=None, use_alt=None, text_style="pref_setting_btn_text", button_id=None, xsize=None, ysize=None):
    $ _use_alt = bool(getattr(persistent, "mm_alt", False)) if use_alt is None else use_alt
    $ _label = pref_L(label)
    use ui_png_button(
        _label,
        action,
        zoom=PREF_TINY_ZOOM,
        xsize=xsize,
        ysize=ysize,
        text_style=text_style,
        use_alt=_use_alt,
        button_id=button_id,
        selected=selected,
        hovered_action=Function(set_pref_tooltip, tooltip) if tooltip else None,
        unhovered_action=Function(clear_pref_tooltip) if tooltip else None
    )

screen pref_icon_button(img, action, tooltip_key=None, button_id=None):
    $ tooltip = pref_L(tooltip_key) if tooltip_key else None
    use ui_rect_icon_button(
        img,
        action,
        button_id=button_id,
        size=68,
        bg="#2a2836",
        hover_overlay="#f003",
        hovered_action=Function(set_pref_tooltip, tooltip),
        unhovered_action=Function(clear_pref_tooltip)
    )

screen pref_add_binding_button(action, tooltip_key=None, button_id=None):
    $ tooltip = pref_L(tooltip_key) if tooltip_key else None
    use ui_rect_text_button(
        pref_L("pref_button_add_binding"),
        action,
        button_id=button_id,
        width=68,
        height=68,
        bg="#2a2836",
        hover_bg="#ff8335",
        text_style="pref_setting_btn_text",
        hovered_action=Function(set_pref_tooltip, tooltip),
        unhovered_action=Function(clear_pref_tooltip)
    )

screen preferences():

    tag menu

    default pref_tab = "display"
    default pref_remapper = pad_remap.ControllerRemap()
    default pref_yadj = ui.adjustment()
    default pref_access_yadj = ui.adjustment()

    # Safe tab switching without relying on button ids.
    key pad_config.get_event("page_left") action SetScreenVariable("pref_tab", next_pref_tab(pref_tab, -1))
    key pad_config.get_event("page_right") action SetScreenVariable("pref_tab", next_pref_tab(pref_tab, 1))
    key "K_q" action SetScreenVariable("pref_tab", next_pref_tab(pref_tab, -1))
    key "K_e" action SetScreenVariable("pref_tab", next_pref_tab(pref_tab, 1))

    add Transform("gui/game_menu.png", xsize=config.screen_width, ysize=config.screen_height)

    # Top tabs
    hbox:
        xpos 120
        ypos 120
        spacing 16
        use pref_tab_button("pref_tab_display", "display", pref_tab, "pref_tip_tab_display")
        use pref_tab_button("pref_tab_audio", "audio", pref_tab, "pref_tip_tab_audio")
        use pref_tab_button("pref_tab_controls", "controls", pref_tab, "pref_tip_tab_controls")
        use pref_tab_button("pref_tab_access", "access", pref_tab, "pref_tip_tab_access")

    # Content area (no panel background, matching save/load style).
    fixed:
        xpos 120
        ypos 210
        xsize 1560
        ysize 700

        frame:
            background None
            xpos 6
            ypos 6
            xsize 1548
            ysize 688
            padding (30, 24)

            if pref_tab == "audio":
                use preferences_tab_audio()
            elif pref_tab == "display":
                use preferences_tab_display()
            elif pref_tab == "access":
                use preferences_tab_access(pref_access_yadj)
            elif pref_tab == "controls":
                use preferences_tab_controls(pref_remapper, pref_yadj)

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22

        use pref_small_button("pref_button_main_menu", MainMenu(), tooltip_key="pref_tip_main_menu", text_style="ui_btn_text_small")
        if main_menu:
            use pref_small_button("pref_button_back", ShowMenu("main_menu"), tooltip_key="pref_tip_back", text_style="ui_btn_text_small")
        else:
            use pref_small_button("pref_button_back", Return(), tooltip_key="pref_tip_back", text_style="ui_btn_text_small")
        use pref_small_button("pref_button_default", Function(reset_preferences), tooltip_key="pref_tip_default", text_style="ui_btn_text_small")

    use ui_tooltip_from_rect(store.pref_tooltip, store.pref_tooltip_rect)
