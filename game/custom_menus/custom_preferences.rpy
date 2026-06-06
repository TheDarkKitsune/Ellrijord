# custom_preferences.rpy

init -2 python:
    PREF_TABS = ["display", "audio", "controls", "access", "visuals"]
    PREF_TAB_COLORS = {
        "display": {
            "accent": "#d8b24f",
            "accent_soft": "#d8b24f22",
            "selected_bg": "#d5b1c6",
            "selected_text": "#5b3c18",
            "sidebar_bg": "#110f2198",
            "main_bg": "#14122696",
            "header_bg": "#191532bc",
            "panel_bg": "#17142fc8",
            "well_bg": "#0b10236e",
        },
        "audio": {
            "accent": "#b79cff",
            "accent_soft": "#b79cff22",
            "selected_bg": "#d9d0ff",
            "selected_text": "#3a275c",
            "sidebar_bg": "#120f239a",
            "main_bg": "#15122898",
            "header_bg": "#1a1536be",
            "panel_bg": "#1a1534ca",
            "well_bg": "#0b102570",
        },
        "controls": {
            "accent": "#63a8ff",
            "accent_soft": "#63a8ff22",
            "selected_bg": "#cfe3ff",
            "selected_text": "#173a66",
            "sidebar_bg": "#0f17279c",
            "main_bg": "#101a2b98",
            "header_bg": "#142341c0",
            "panel_bg": "#142341ca",
            "well_bg": "#09122174",
        },
        "access": {
            "accent": "#7ddbcf",
            "accent_soft": "#7ddbcf22",
            "selected_bg": "#c5efe9",
            "selected_text": "#164c49",
            "sidebar_bg": "#0d1827b0",
            "main_bg": "#101a2ab6",
            "header_bg": "#13273bd0",
            "panel_bg": "#0f1d31e0",
            "well_bg": "#081322b6",
        },
        "visuals": {
            "accent": "#d8b24f",
            "accent_soft": "#d8b24f22",
            "selected_bg": "#d8cff4",
            "selected_text": "#4a355f",
            "sidebar_bg": "#141024a6",
            "main_bg": "#17142ab0",
            "header_bg": "#1d1735cc",
            "panel_bg": "#191531d2",
            "well_bg": "#0c1024b4",
        },
    }

    VISUAL_PREF_DEFAULTS = {
        "pref_ui_opacity": 0.80,
        "pref_textbox_opacity": 0.80,
        "pref_menu_background_dim": 0.60,
        "pref_highlight_intensity": 0.70,
        "pref_particle_effects": True,
        "pref_screen_effects": True,
        "pref_scene_transitions": True,
        "pref_menu_animations": True,
        "pref_transition_speed": 0.55,
        "pref_cursor_style": "classic",
        "pref_dialogue_window_style": "classic",
        "pref_theme_accent": "violet",
        "pref_button_glow": "medium",
        "pref_panel_border_style": "ornate",
        "pref_selected_highlight_style": "glow",
        "pref_confirm_prompts": True,
        "pref_remember_last_tab": True,
        "pref_last_settings_tab": "display",
    }

    def water_lemon_font_transform(f):
        p_otf = "fonts/water_lemon/Water Lemon.otf"
        p_ttf = "fonts/water_lemon/Water Lemon.ttf"
        if renpy.loadable(p_otf):
            return p_otf
        if renpy.loadable(p_ttf):
            return p_ttf
        return f

    def cinzel_font_transform(f):
        p_otf = "fonts/cinzel/Cinzel-Bold.otf"
        return p_otf if renpy.loadable(p_otf) else f

    config.font_transforms["cinzel"] = cinzel_font_transform
    config.font_transforms["water_lemon"] = water_lemon_font_transform

    def _fix_mute_pref_type():
        prefdata = getattr(persistent, "_preferences", None)
        if isinstance(prefdata, dict) and isinstance(prefdata.get("mute"), bool):
            val = prefdata.get("mute")
            prefdata["mute"] = {"music": val, "sound": val, "voice": val}

    _fix_mute_pref_type()

    def ensure_visual_pref_defaults():
        changed = False
        for field, value in VISUAL_PREF_DEFAULTS.items():
            if (not hasattr(persistent, field)) or (getattr(persistent, field, None) is None):
                setattr(persistent, field, value)
                changed = True
        if changed:
            try:
                renpy.save_persistent()
            except Exception:
                pass

    def _pref_clamp(value, low=0.0, high=1.0):
        if value is None:
            value = low
        return max(low, min(high, float(value)))

    def pref_visual_value(field, default=None):
        ensure_visual_pref_defaults()
        if default is None:
            default = VISUAL_PREF_DEFAULTS.get(field)
        value = getattr(persistent, field, default)
        if value is None:
            value = default
        return value

    def pref_set_visual_value(field, value):
        setattr(persistent, field, value)
        apply_visual_preferences()

    def _pref_parse_hex(color):
        color = (color or "#000000").lstrip("#")
        if len(color) == 3:
            color = "".join(ch * 2 for ch in color) + "ff"
        elif len(color) == 4:
            color = "".join(ch * 2 for ch in color)
        elif len(color) == 6:
            color += "ff"
        elif len(color) != 8:
            color = "000000ff"
        return tuple(int(color[i:i + 2], 16) for i in range(0, 8, 2))

    def pref_color_alpha(color, factor=1.0):
        r, g, b, a = _pref_parse_hex(color)
        a = int(_pref_clamp((a / 255.0) * factor) * 255)
        return "#{:02x}{:02x}{:02x}{:02x}".format(r, g, b, a)

    def pref_surface_color(base_color, role="panel"):
        ui_opacity = _pref_clamp(pref_visual_value("pref_ui_opacity", 0.80))
        role_factor = {
            "sidebar": ui_opacity * 0.92,
            "main": ui_opacity * 0.88,
            "header": min(1.0, ui_opacity * 0.98),
            "panel": min(1.0, ui_opacity * 1.04),
            "well": min(1.0, ui_opacity * 1.16),
        }.get(role, ui_opacity)
        return pref_color_alpha(base_color, role_factor)

    def pref_selected_fill(base_color):
        intensity = 0.34 + (_pref_clamp(pref_visual_value("pref_highlight_intensity", 0.70)) * 0.66)
        return pref_color_alpha(base_color, intensity)

    def pref_background_dim_alpha():
        return 0.08 + (_pref_clamp(pref_visual_value("pref_menu_background_dim", 0.60)) * 0.22)

    def pref_background_glow_alpha():
        if not pref_visual_value("pref_screen_effects", True):
            return 0.0
        return 0.03 + (_pref_clamp(pref_visual_value("pref_menu_background_dim", 0.60)) * 0.08)

    def pref_visual_percent(field):
        return "{}%".format(int(round(_pref_clamp(pref_visual_value(field, 0.0)) * 100.0)))

    def pref_visual_bool(field):
        return bool(pref_visual_value(field, False))

    def pref_cursor_style_key():
        current = str(pref_visual_value("pref_cursor_style", "arrow") or "arrow").lower()
        return {
            "classic": "arrow",
            "glow": "feather",
            "star": "star",
            "ring": "moon",
            "petal": "paw",
            "arrow": "arrow",
            "feather": "feather",
            "paw": "paw",
            "moon": "moon",
            "crystal": "crystal",
        }.get(current, "arrow")

    def pref_visual_cursor_symbol():
        return {
            "arrow": ">",
            "feather": "/",
            "star": "+",
            "paw": "o",
            "moon": ")",
            "crystal": "#",
        }.get(pref_cursor_style_key(), ">")

    def pref_visual_cursor_label():
        return {
            "arrow": "Arrow",
            "star": "Star",
            "feather": "Feather",
            "paw": "Paw",
            "moon": "Moon",
            "crystal": "Crystal",
        }.get(pref_cursor_style_key(), "Arrow")

    def pref_mouse_cursor_name():
        return "feather" if pref_cursor_style_key() == "feather" else None

    def pref_visual_window_style_label():
        return {
            "classic": "Classic",
            "soft": "Soft",
            "bright": "Bright",
            "fantasy": "Fantasy Frame",
            "minimal": "Minimal",
        }.get(pref_visual_value("pref_dialogue_window_style", "classic"), "Classic")

    def pref_theme_accent_key():
        current = str(pref_visual_value("pref_theme_accent", "violet") or "violet").lower()
        return current if current in ("gold", "violet", "blue", "mint", "rose") else "violet"

    def pref_theme_accent_label():
        return {
            "gold": "Gold",
            "violet": "Violet",
            "blue": "Blue",
            "mint": "Mint",
            "rose": "Rose",
        }.get(pref_theme_accent_key(), "Violet")

    def pref_theme_palette():
        key = pref_theme_accent_key()
        return {
            "gold": {"accent": "#d8b24f", "selected_bg": "#e2d39b", "selected_text": "#4e3912"},
            "violet": {"accent": "#d39bd2", "selected_bg": "#d8cff4", "selected_text": "#4a355f"},
            "blue": {"accent": "#88b8ff", "selected_bg": "#d4e3ff", "selected_text": "#27446b"},
            "mint": {"accent": "#8edcca", "selected_bg": "#d1f1e8", "selected_text": "#1f544e"},
            "rose": {"accent": "#df9ab2", "selected_bg": "#f0d3dd", "selected_text": "#673348"},
        }.get(key, {"accent": "#d39bd2", "selected_bg": "#d8cff4", "selected_text": "#4a355f"})

    def pref_button_glow_key():
        current = str(pref_visual_value("pref_button_glow", "medium") or "medium").lower()
        return current if current in ("low", "medium", "high") else "medium"

    def pref_button_glow_label():
        return pref_button_glow_key().title()

    def pref_button_glow_alpha():
        return {
            "low": 0.18,
            "medium": 0.30,
            "high": 0.44,
        }.get(pref_button_glow_key(), 0.30)

    def pref_panel_border_style_key():
        current = str(pref_visual_value("pref_panel_border_style", "ornate") or "ornate").lower().replace(" ", "_")
        mapping = {
            "nothing": "nothing",
            "none": "nothing",
            "simple": "simple",
            "ornate": "ornate",
            "soft_glow": "soft_glow",
            "softglow": "soft_glow",
        }
        return mapping.get(current, "ornate")

    def pref_panel_border_style_label():
        return {
            "nothing": "Nothing",
            "simple": "Simple",
            "ornate": "Ornate",
            "soft_glow": "Soft Glow",
        }.get(pref_panel_border_style_key(), "Ornate")

    def pref_selected_highlight_style_key():
        current = str(pref_visual_value("pref_selected_highlight_style", "glow") or "glow").lower()
        return current if current in ("fill", "outline", "glow") else "glow"

    def pref_selected_highlight_style_label():
        return pref_selected_highlight_style_key().title()

    def pref_dialogue_window_background(style_name=None, alpha=None, width=1526, height=251):
        style_name = style_name or pref_visual_value("pref_dialogue_window_style", "classic")
        alpha = _pref_clamp(pref_visual_value("pref_textbox_opacity", 0.80) if alpha is None else alpha)
        base = Transform("gui/hud/msgbox_720p.png", size=(width, height), xalign=0.5, yalign=0.0, alpha=alpha)

        if style_name == "soft":
            return Fixed(
                base,
                Transform(Solid("#f3e6ff18"), xsize=width, ysize=height),
                xsize=width,
                ysize=height,
            )
        if style_name == "bright":
            return Fixed(
                base,
                Transform(Solid("#f2edf833"), xsize=width, ysize=height),
                Transform(Solid("#d8b24f66"), xsize=width, ysize=3, ypos=3),
                xsize=width,
                ysize=height,
            )
        if style_name == "fantasy":
            return Fixed(
                Transform("gui/hud/msgbox_720p.png", size=(width, height), xalign=0.5, yalign=0.0, alpha=max(0.48, alpha * 0.78)),
                Transform(Solid("#2414347a"), xsize=width, ysize=height),
                Transform(Solid("#e0b5ff88"), xsize=width, ysize=2, ypos=2),
                Transform(Solid("#e0b5ff55"), xsize=width, ysize=2, ypos=(height - 4)),
                xsize=width,
                ysize=height,
            )
        if style_name == "minimal":
            return Fixed(
                Transform("gui/hud/msgbox_720p.png", size=(width, height), xalign=0.5, yalign=0.0, alpha=max(0.42, alpha * 0.72)),
                Transform(Solid("#0d112488"), xsize=width, ysize=height),
                Transform(Solid("#c7d8ff55"), xsize=width, ysize=2, ypos=0),
                xsize=width,
                ysize=height,
            )
        return base

    def pref_dialogue_namebox_background(style_name=None, alpha=None, width=380, height=78):
        style_name = style_name or pref_visual_value("pref_dialogue_window_style", "classic")
        alpha = _pref_clamp(pref_visual_value("pref_textbox_opacity", 0.80) if alpha is None else alpha)
        base = Transform("gui/hud/msgbox_name_header_720p.png", size=(width, height), alpha=alpha)

        if style_name == "soft":
            return Fixed(
                base,
                Transform(Solid("#f3e6ff18"), xsize=width, ysize=height),
                xsize=width,
                ysize=height,
            )
        if style_name == "bright":
            return Fixed(
                base,
                Transform(Solid("#f2edf833"), xsize=width, ysize=height),
                Transform(Solid("#d8b24f66"), xsize=width, ysize=3, ypos=2),
                xsize=width,
                ysize=height,
            )
        if style_name == "fantasy":
            return Fixed(
                Transform("gui/hud/msgbox_name_header_720p.png", size=(width, height), alpha=max(0.48, alpha * 0.78)),
                Transform(Solid("#2414347a"), xsize=width, ysize=height),
                Transform(Solid("#e0b5ff88"), xsize=width, ysize=2, ypos=1),
                xsize=width,
                ysize=height,
            )
        if style_name == "minimal":
            return Fixed(
                Transform("gui/hud/msgbox_name_header_720p.png", size=(width, height), alpha=max(0.42, alpha * 0.72)),
                Transform(Solid("#0d112488"), xsize=width, ysize=height),
                Transform(Solid("#c7d8ff55"), xsize=width, ysize=2, ypos=0),
                xsize=width,
                ysize=height,
            )
        return base

    def pref_transition_duration():
        if not pref_visual_value("pref_scene_transitions", True):
            return 0.0
        if not pref_visual_value("pref_menu_animations", True):
            return 0.0
        speed = _pref_clamp(pref_visual_value("pref_transition_speed", 0.55))
        return speed * 0.65

    def pref_transition_mode():
        speed = _pref_clamp(pref_visual_value("pref_transition_speed", 0.55))
        if speed <= 0.08:
            return "instant"
        if speed <= 0.38:
            return "fast"
        if speed <= 0.68:
            return "normal"
        return "slow"

    def pref_transition_mode_label():
        return {
            "instant": "Instant",
            "fast": "Fast",
            "normal": "Normal",
            "slow": "Slow",
        }.get(pref_transition_mode(), "Normal")

    def set_pref_transition_mode(mode):
        mapping = {
            "instant": 0.0,
            "fast": 0.25,
            "normal": 0.55,
            "slow": 0.85,
        }
        pref_set_visual_value("pref_transition_speed", mapping.get(mode, 0.55))

    def remember_pref_tab(tab):
        if pref_visual_bool("pref_remember_last_tab"):
            persistent.pref_last_settings_tab = tab

    def initial_pref_tab():
        ensure_visual_pref_defaults()
        if pref_visual_bool("pref_remember_last_tab"):
            tab = getattr(persistent, "pref_last_settings_tab", "display")
            if tab in PREF_TABS:
                return tab
        return "display"

    def apply_visual_preferences():
        ensure_visual_pref_defaults()
        duration = pref_transition_duration()
        transition = None if duration <= 0.01 else Dissolve(duration)
        config.window_show_transition = transition
        config.window_hide_transition = transition
        renpy.store.default_mouse = pref_mouse_cursor_name()

    ensure_visual_pref_defaults()
    config.mouse_displayable = MouseDisplayable(None).add("feather", "gui/button/test.png", 2, 3)
    apply_visual_preferences()

    class PersistentFloatAdjustment(BarValue):
        def __init__(self, field, default=0.0, step=0.01, changed=None):
            self.field = field
            self.default = float(default)
            self.step = step
            self._changed = changed
            super(PersistentFloatAdjustment, self).__init__()

        def get_adjustment(self):
            return ui.adjustment(
                value=_pref_clamp(pref_visual_value(self.field, self.default)),
                range=1.0,
                step=self.step,
                adjustable=True,
                changed=self.set_value,
            )

        def set_value(self, value):
            pref_set_visual_value(self.field, _pref_clamp(value))
            if self._changed is not None:
                self._changed()

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
        def _cfg(name, fallback):
            try:
                return getattr(config, name)
            except Exception:
                return fallback

        try:
            renpy.reset_preferences()
        except Exception:
            pass

        default_pref_values = (
            ("text speed", _cfg("default_text_cps", 0)),
            ("auto-forward time", _cfg("default_afm_time", 15)),
            ("music volume", 1.0),
            ("sound volume", 1.0),
            ("voice volume", 1.0),
            ("font size", _cfg("default_font_size", 1.0)),
            ("font line spacing", _cfg("default_font_line_spacing", 1.0)),
            ("self voicing volume drop", _cfg("default_self_voicing_volume_drop", 0.0)),
        )
        for pref_name, pref_value in default_pref_values:
            try:
                renpy.store.Preference(pref_name, pref_value)()
            except Exception:
                pass

        prefs = renpy.game.preferences
        if hasattr(prefs, "fullscreen"):
            prefs.fullscreen = config.default_fullscreen
        if hasattr(prefs, "skip_unseen"):
            prefs.skip_unseen = False
        if hasattr(prefs, "skip_after_choices"):
            prefs.skip_after_choices = False
        if hasattr(prefs, "text_cps"):
            prefs.text_cps = _cfg("default_text_cps", 0)
        if hasattr(prefs, "afm_time"):
            prefs.afm_time = _cfg("default_afm_time", 15)
        if hasattr(prefs, "font_transform"):
            prefs.font_transform = None
        if hasattr(prefs, "high_contrast_text"):
            prefs.high_contrast_text = False
        if hasattr(prefs, "self_voicing"):
            prefs.self_voicing = False
        if hasattr(prefs, "clipboard_voicing"):
            prefs.clipboard_voicing = False
        if hasattr(prefs, "debug_voicing"):
            prefs.debug_voicing = False
        if hasattr(prefs, "music_volume"):
            prefs.music_volume = 1.0
        if hasattr(prefs, "sound_volume"):
            prefs.sound_volume = 1.0
        if hasattr(prefs, "voice_volume"):
            prefs.voice_volume = 1.0
        if hasattr(prefs, "font_size"):
            prefs.font_size = _cfg("default_font_size", 1.0)
        if hasattr(prefs, "font_line_spacing"):
            prefs.font_line_spacing = _cfg("default_font_line_spacing", 1.0)
        if hasattr(prefs, "self_voicing_volume_drop"):
            prefs.self_voicing_volume_drop = _cfg("default_self_voicing_volume_drop", 0.0)

        set_all_mute(False)
        for ch in ("music", "sound", "voice"):
            try:
                renpy.music.set_volume(1.0, channel=ch)
            except Exception:
                pass

        for field, value in (
            ("hold_to_skip", False),
            ("left_stick_invert_x", False),
            ("left_stick_invert_y", False),
            ("right_stick_invert_x", False),
            ("right_stick_invert_y", False),
            ("left_stick_sensitivity", 1.0),
            ("right_stick_sensitivity", 1.0),
            ("controller_layout", "generic"),
        ):
            if hasattr(persistent, field):
                setattr(persistent, field, value)

        for field in (
            "left_stick_dead_zone",
            "right_stick_dead_zone",
            "left_stick_max",
            "right_stick_max",
            "controller_guid_to_type",
        ):
            if hasattr(persistent, field):
                setattr(persistent, field, dict())

        for field, value in VISUAL_PREF_DEFAULTS.items():
            setattr(persistent, field, value)

        try:
            if hasattr(renpy.store, "reset_to_default"):
                renpy.store.reset_to_default(None)
        except Exception:
            pass

        apply_visual_preferences()

        try:
            renpy.style.rebuild()
        except Exception:
            pass

        renpy.save_persistent()
        renpy.restart_interaction()

    def pref_L(key):
        if key is None:
            return ""
        txt = L(key)
        if txt != key:
            return txt
        return {
            "pref_tab_display": "DISPLAY",
            "pref_tab_audio": "AUDIO",
            "pref_tab_controls": "CONTROLS",
            "pref_tab_access": "ACCESS",
            "pref_tab_visuals": "INTERFACE",
            "pref_button_main_menu": "MAIN MENU",
            "pref_button_back": "BACK",
            "pref_button_default": "DEFAULT",
        }.get(key, key)

    def pref_bool_text(value):
        return pref_L("pref_button_on") if value else pref_L("pref_button_off")

    def pref_font_label():
        mapping = {
            None: pref_L("pref_button_default_font"),
            "dejavusans": pref_L("pref_button_dejavu_sans"),
            "cinzel": pref_L("pref_button_cinzel"),
            "opendyslexic": pref_L("pref_button_opendyslexic"),
            "water_lemon": pref_L("pref_button_water_lemon"),
        }
        current = getattr(renpy.game.preferences, "font_transform", None)
        return mapping.get(current, str(current).upper())

    def pref_tab_heading(current):
        return {
            "display": "Display",
            "audio": "Audio",
            "controls": "Controls",
            "access": "Accessibility",
            "visuals": "Interface",
        }.get(current, "Display")

    def pref_tab_subtitle(current):
        return {
            "display": "Screen mode, skip rules, and text pacing.",
            "audio": "Volume balance and mute controls.",
            "controls": "Gamepad calibration, bindings, and stick tuning.",
            "access": "Readable text, contrast, and self-voicing.",
            "visuals": "Customize the look and feel of the game interface.",
        }.get(current, "Screen mode, skip rules, and text pacing.")

    def pref_tab_colors(current):
        return PREF_TAB_COLORS.get(current, PREF_TAB_COLORS["display"])

    def pref_sidebar_rows(current):
        prefs = renpy.game.preferences

        if current == "display":
            return [
                ("Mode", "Fullscreen" if getattr(prefs, "fullscreen", False) else "Window"),
                ("Skip Unseen", pref_bool_text(getattr(prefs, "skip_unseen", False))),
                ("Language", get_ui_lang_label(get_ui_lang())),
            ]

        if current == "audio":
            muted_label = pref_L("pref_button_muted")
            music_value = muted_label if is_all_muted() else "{}%".format(int(getattr(prefs, "music_volume", 1.0) * 100))
            sfx_value = muted_label if is_all_muted() else "{}%".format(int(getattr(prefs, "sound_volume", 1.0) * 100))
            voice_value = muted_label if is_all_muted() else "{}%".format(int(getattr(prefs, "voice_volume", 1.0) * 100))
            return [
                ("Mute All", pref_bool_text(is_all_muted())),
                ("Music", music_value),
                ("SFX", sfx_value),
                ("Voice", voice_value),
            ]

        if current == "controls":
            return [
                ("Hold To Skip", pref_bool_text(getattr(persistent, "hold_to_skip", False))),
                ("Layout", str(getattr(persistent, "controller_layout", "generic")).replace("_", " ").title()),
                ("Left Y Invert", pref_bool_text(getattr(persistent, "left_stick_invert_y", False))),
            ]

        if current == "visuals":
            return [
                ("Accent", pref_theme_accent_label()),
                ("Glow", pref_button_glow_label()),
                ("Border", pref_panel_border_style_label()),
                ("Cursor", pref_visual_cursor_label()),
            ]

        return [
            ("Font", pref_font_label()),
            ("Contrast", pref_bool_text(getattr(prefs, "high_contrast_text", False))),
            ("Self-Voicing", pref_bool_text(getattr(prefs, "self_voicing", False))),
        ]

    def next_pref_tab(current, step):
        try:
            idx = PREF_TABS.index(current)
        except Exception:
            idx = 0
        return PREF_TABS[(idx + step) % len(PREF_TABS)]

    def pref_sidebar_icon():
        for candidate in ("gui/logos/settings.png", "gui/window_icon.png"):
            if renpy.loadable(candidate):
                return candidate
        return None

    def pref_preview_cps():
        cps = float(getattr(renpy.game.preferences, "text_cps", 0) or 0)
        if cps <= 0:
            return 28.0
        return min(max(cps, 14.0), 72.0)

    def pref_preview_char_delay():
        return 1.0 / pref_preview_cps()

    def pref_preview_hold_delay():
        afm = float(getattr(renpy.game.preferences, "afm_time", 15) or 15)
        return max(0.9, min(2.2, afm / 8.0))

    def pref_preview_cycle_delay(line):
        line_len = max(1, len(line or ""))
        return (line_len * pref_preview_char_delay()) + pref_preview_hold_delay()

    def pref_preview_text_dd(st, at, line, style="pref_body_text", size=20, color=None):
        line = line or ""
        if not pref_visual_value("pref_menu_animations", True):
            text_kwargs = {"style": style}
            if size is not None:
                text_kwargs["size"] = size
            if color is not None:
                text_kwargs["color"] = color
            return Text(line, **text_kwargs), None

        char_delay = pref_preview_char_delay()
        type_duration = max(char_delay, len(line) * char_delay)
        hold_duration = pref_preview_hold_delay()
        cycle_duration = type_duration + hold_duration
        phase = (st % cycle_duration) if cycle_duration > 0.0 else 0.0

        if phase >= type_duration:
            char_count = len(line)
        else:
            char_count = max(1, min(len(line), int(phase / char_delay) + 1))

        shown = line[:char_count]
        cursor_on = (phase < type_duration) or (int((phase - type_duration) / 0.28) % 2 == 0)
        if cursor_on:
            shown += " " + pref_visual_cursor_symbol()

        text_kwargs = {"style": style}
        if size is not None:
            text_kwargs["size"] = size
        if color is not None:
            text_kwargs["color"] = color

        return Text(shown, **text_kwargs), min(0.05, char_delay)

    def pref_preview_displayable(line, style="pref_body_text", size=20, color=None):
        return DynamicDisplayable(pref_preview_text_dd, line, style, size, color)

    def pref_audio_percent(pref_attr):
        return "{}%".format(int(getattr(renpy.game.preferences, pref_attr, 1.0) * 100))

style pref_shell_frame:
    background "#09101e82"
    xpadding 28
    ypadding 28

style pref_sidebar_frame:
    background "#14122696"
    xpadding 18
    ypadding 18

style pref_main_frame:
    background "#14122692"
    xpadding 0
    ypadding 0

style pref_sidebar_button:
    background "#00000000"
    hover_background "#ffffff10"
    xfill True
    ypadding 14
    xpadding 18

style pref_sidebar_button_text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 25
    color "#eef3ff"
    hover_color "#ffffff"
    selected_color "#1b2431"

style pref_screen_title is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 50
    color "#f6f1e7"

style pref_screen_subtitle is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 20
    color "#d6deef"

style pref_section_title is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 30
    color "#fcf7ee"

style pref_body_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 22
    color "#edf3ff"

style pref_muted_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 18
    color "#b9c5d8"

style pref_label_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 16
    color "#95a4bc"

style pref_sidebar_value_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 19
    color "#edf3ff"

style pref_setting_label is pref_body_text:
    size 20

style pref_setting_btn_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 18
    color "#d8d1ea"
    hover_color "#ffffff"
    selected_color "#1b2431"
    xalign 0.5
    yalign 0.5

style pref_choice_button:
    background "#00000048"
    hover_background "#00000062"
    ypadding 12
    xpadding 18

style pref_square_button:
    background "#00000048"
    hover_background "#00000062"
    xpadding 0
    ypadding 0

style pref_panel_frame:
    background "#17142fc8"
    xpadding 18
    ypadding 14

style pref_bar is ui_slider_bar_fill


screen pref_small_button(label_key, action, selected=False, tooltip_key=None, use_alt=None, text_style="pref_setting_btn_text", button_id=None, xsize=None, ysize=None, accent=None, selected_bg=None, selected_text=None):
    $ label = pref_L(label_key)
    $ _accent = accent if accent is not None else PREF_TAB_COLORS["display"]["accent"]
    $ _selected_bg = selected_bg if selected_bg is not None else PREF_TAB_COLORS["display"]["selected_bg"]
    $ _selected_text = selected_text if selected_text is not None else PREF_TAB_COLORS["display"]["selected_text"]
    $ _selected_fill = pref_selected_fill(_selected_bg)
    $ _xsize = 190 if xsize is None else xsize
    $ _ysize = 52 if ysize is None else ysize

    textbutton label:
        style "pref_choice_button"
        text_style text_style
        action action
        selected selected
        xsize _xsize
        ysize _ysize
        text_xalign 0.5
        text_yalign 0.5
        text_xmaximum (_xsize - 20)
        text_hover_color _accent
        text_selected_color _selected_text
        selected_background _selected_fill
        if button_id is not None:
            id button_id


screen pref_tiny_button(label, action, selected=False, tooltip=None, use_alt=None, text_style="pref_setting_btn_text", button_id=None, xsize=None, ysize=None, accent=None, selected_bg=None, selected_text=None):
    $ _label = pref_L(label)
    use pref_small_button(_label, action, selected=selected, text_style=text_style, button_id=button_id, xsize=xsize, ysize=ysize, accent=accent, selected_bg=selected_bg, selected_text=selected_text)


screen pref_icon_button(img, action, tooltip_key=None, button_id=None):
    button:
        style "pref_square_button"
        xsize 68
        ysize 68
        action action
        if button_id is not None:
            id button_id

        fixed:
            xsize 68
            ysize 68
            add Solid("#ffffff08") xpos 2 ypos 2 xsize 64 ysize 64
            add Solid("#d8b24f") xpos 0 ypos 0 xsize 68 ysize 2
            add Transform(img, fit="contain", xsize=48, ysize=48, xalign=0.5, yalign=0.5)


screen pref_add_binding_button(action, tooltip_key=None, button_id=None):
    button:
        style "pref_square_button"
        xsize 68
        ysize 68
        action action
        if button_id is not None:
            id button_id

        fixed:
            xsize 68
            ysize 68
            add Solid("#ffffff08") xpos 2 ypos 2 xsize 64 ysize 64
            add Solid("#d8b24f") xpos 0 ypos 0 xsize 68 ysize 2
            text pref_L("pref_button_add_binding") style "pref_setting_btn_text" xsize 68 ysize 68 xalign 0.5 yalign 0.5 text_align 0.5


screen pref_hub_panel(title, subtitle=None, xsize=400, ysize=200, accent="#d8b24f", background="#241d4358"):
    frame:
        style "pref_panel_frame"
        background pref_surface_color(background, "panel")
        xsize xsize
        ysize ysize

        vbox:
            spacing 6
            text title style "pref_section_title" color accent
            if subtitle:
                text subtitle style "pref_label_text"
            add Solid(accent + "66") xsize (xsize - 36) ysize 2
            transclude


screen pref_hub_slider_row(label_key, value, tooltip_key=None, variant="default", style_name="pref_bar", label_width=250, slider_width=360, dimmed=False):
    $ _row_alpha = 0.48 if dimmed else 1.0

    hbox:
        at Transform(alpha=_row_alpha)
        spacing 12

        fixed:
            xsize label_width
            ysize 64
            text pref_L(label_key) style "pref_setting_label" yalign 0.5

        fixed:
            xsize 42
            ysize 64
            text pref_L("pref_label_min") style "pref_label_text" xalign 1.0 yalign 0.5

        fixed:
            xsize slider_width
            ysize 64
            use ui_slider(value, style_name=style_name, variant=variant, xpos=0, ypos=16, xsize=slider_width, ysize=32)

        fixed:
            xsize 42
            ysize 64
            text pref_L("pref_label_max") style "pref_label_text" xalign 0.0 yalign 0.5


transform pref_particle_float_a:
    xpos 220
    ypos 820
    alpha 0.0
    linear 0.8 alpha 0.35
    linear 12.0 xpos 420 ypos 180 alpha 0.18
    linear 1.2 alpha 0.0
    repeat

transform pref_particle_float_b:
    xpos 980
    ypos 900
    alpha 0.0
    linear 1.4 alpha 0.28
    linear 14.0 xpos 1180 ypos 260 alpha 0.12
    linear 1.2 alpha 0.0
    repeat

transform pref_particle_float_c:
    xpos 1540
    ypos 760
    alpha 0.0
    linear 1.0 alpha 0.30
    linear 11.0 xpos 1360 ypos 210 alpha 0.14
    linear 1.0 alpha 0.0
    repeat

screen pref_particles_overlay():
    if pref_visual_bool("pref_particle_effects") and pref_visual_bool("pref_menu_animations"):
        add Solid("#c7dcff88") at pref_particle_float_a xsize 6 ysize 6
        add Solid("#f1ddff78") at pref_particle_float_b xsize 5 ysize 5
        add Solid("#a6f5ff70") at pref_particle_float_c xsize 4 ysize 4


screen preferences():

    tag menu
    on "hide" action Function(renpy.restart_interaction)

    default pref_tab = initial_pref_tab()
    default pref_remapper = pad_remap.ControllerRemap()
    default pref_yadj = ui.adjustment()
    default pref_access_yadj = ui.adjustment()

    key pad_config.get_event("page_left") action [SetScreenVariable("pref_tab", next_pref_tab(pref_tab, -1)), Function(remember_pref_tab, next_pref_tab(pref_tab, -1))]
    key pad_config.get_event("page_right") action [SetScreenVariable("pref_tab", next_pref_tab(pref_tab, 1)), Function(remember_pref_tab, next_pref_tab(pref_tab, 1))]
    key "K_q" action [SetScreenVariable("pref_tab", next_pref_tab(pref_tab, -1)), Function(remember_pref_tab, next_pref_tab(pref_tab, -1))]
    key "K_e" action [SetScreenVariable("pref_tab", next_pref_tab(pref_tab, 1)), Function(remember_pref_tab, next_pref_tab(pref_tab, 1))]

    $ tab_colors = pref_tab_colors(pref_tab)
    $ pref_heading = pref_tab_heading(pref_tab)
    $ pref_subtitle = pref_tab_subtitle(pref_tab)
    $ sidebar_rows = pref_sidebar_rows(pref_tab)
    $ sidebar_icon = pref_sidebar_icon()
    $ pref_is_visuals = (pref_tab == "visuals")
    $ pref_shell_bg = "#00000000" if pref_is_visuals else "#09101e82"
    $ pref_sidebar_bg = "#101427dc" if pref_is_visuals else pref_surface_color(tab_colors["sidebar_bg"], "sidebar")
    $ pref_main_bg = "#11152cb0" if pref_is_visuals else pref_surface_color(tab_colors["main_bg"], "main")
    $ pref_header_bg = "#00000000" if pref_is_visuals else pref_surface_color(tab_colors["header_bg"], "header")
    $ pref_sidebar_w = 280 if pref_is_visuals else 300
    $ pref_sidebar_h = 760 if pref_is_visuals else 896
    $ pref_sidebar_spacing = 10 if pref_is_visuals else 14

    add Transform("gui/inventory_system/gui/inventory_bg.png", xsize=config.screen_width, ysize=config.screen_height)
    add Solid(pref_color_alpha("#020617", pref_background_dim_alpha()))
    if pref_visual_bool("pref_screen_effects"):
        add Solid(pref_color_alpha("#8f6dff", pref_background_glow_alpha()))
    use pref_particles_overlay

    frame:
        style "pref_shell_frame"
        background pref_shell_bg
        xpos 74
        ypos 64
        xsize 1772
        ysize 952

        hbox:
            spacing 22

            frame:
                style "pref_sidebar_frame"
                background pref_sidebar_bg
                xsize pref_sidebar_w
                ysize pref_sidebar_h

                vbox:
                    spacing pref_sidebar_spacing

                    hbox:
                        spacing 14
                        if sidebar_icon:
                            add Transform(sidebar_icon, xsize=110, ysize=110)
                        else:
                            add Solid("#ffffff10") xsize 110 ysize 110
                        vbox:
                            spacing 2
                            text "CONFIG" style "pref_section_title"
                            text "Game settings and system options." style "pref_label_text"

                    null height 8

                    for tab in PREF_TABS:
                        $ sidebar_tab_colors = pref_tab_colors(tab)
                        textbutton pref_L("pref_tab_" + tab):
                            style "pref_sidebar_button"
                            text_style "pref_sidebar_button_text"
                            action [SetScreenVariable("pref_tab", tab), Function(remember_pref_tab, tab)]
                            selected (pref_tab == tab)
                            selected_background pref_selected_fill(sidebar_tab_colors["selected_bg"])
                            text_selected_color sidebar_tab_colors["selected_text"]
                            text_hover_color sidebar_tab_colors["accent"]

                    null height 14
                    text _("Overview") style "pref_label_text" color tab_colors["accent"]

                    for row_label, row_value in sidebar_rows:
                        hbox:
                            xfill True
                            text row_label style "pref_muted_text" color ("#e7ecf7" if pref_is_visuals else "#b9c5d8")
                            text row_value style "pref_sidebar_value_text" color tab_colors["accent"] xalign 1.0

            frame:
                style "pref_main_frame"
                background pref_main_bg
                xsize 1450
                ysize 896

                vbox:
                    spacing 18

                    frame:
                        background pref_header_bg
                        xfill True
                        ysize 120
                        xpadding 18
                        ypadding 14

                        vbox:
                            spacing 5
                            text pref_heading style "pref_screen_title" color tab_colors["accent"]
                            text pref_subtitle style "pref_screen_subtitle"

                    fixed:
                        xsize 1450
                        ysize 740

                        if pref_tab == "audio":
                            use preferences_tab_audio()
                        elif pref_tab == "display":
                            use preferences_tab_display()
                        elif pref_tab == "access":
                            use preferences_tab_access(pref_access_yadj)
                        elif pref_tab == "visuals":
                            use preferences_tab_visuals()
                        else:
                            use preferences_tab_controls(pref_remapper, pref_yadj)

    hbox:
        xalign 0.5
        yalign 0.975
        spacing 20

        use ui_png_button(pref_L("pref_button_main_menu"), MainMenu(), xsize=260, ysize=56, text_style="ui_btn_text_small")
        if main_menu:
            use ui_png_button(pref_L("pref_button_back"), ShowMenu("main_menu"), xsize=220, ysize=56, text_style="ui_btn_text_small")
        else:
            use ui_png_button(pref_L("pref_button_back"), Return(), xsize=220, ysize=56, text_style="ui_btn_text_small")
        use ui_png_button(pref_L("pref_button_default"), Function(reset_preferences), xsize=260, ysize=56, text_style="ui_btn_text_small")
