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
        "pref_theme_accent": "gold",
        "pref_button_glow": "low",
        "pref_panel_border_style": "simple",
        "pref_selected_highlight_style": "fill",
        "pref_custom_high_contrast": False,
        "pref_confirm_prompts": True,
        "pref_remember_last_tab": True,
        "pref_last_settings_tab": "display",
    }

    UI_THEME_ASSET_PACKS = {
        "classic": {
            "window_icon": "gui/window_icon.png",
            "game_menu_background": "gui/menu/game_menu.png",
            "textbox": "gui/hud/msgbox_720p.png",
            "namebox": "gui/hud/msgbox_name_header_720p.png",
            "choice_idle": "gui/button/choice_label_720p.png",
            "choice_hover": "gui/button/choice_label_hover_720p.png",
            "slot_idle": "gui/button/slot_idle_background.png",
            "slot_hover": "gui/button/slot_hover_background.png",
        },
        "komic": {
            "window_icon": "gui/KOMIC/window_icon.png",
            "game_menu_background": "gui/KOMIC/Overlays/game_menu.png",
            "textbox": "gui/KOMIC/textbox.png",
            "textbox_overlay": "gui/KOMIC/textbox_transparent.png",
            "namebox": "gui/KOMIC/frame.png",
            "choice_idle": "gui/KOMIC/Buttons/choice_idle.png",
            "choice_hover": "gui/KOMIC/Buttons/choice_hover.png",
            "slot_idle": "gui/KOMIC/Buttons/slot_idle_background.png",
            "slot_hover": "gui/KOMIC/Buttons/slot_hover_background.png",
            "quick_continue_idle": "gui/KOMIC/QuickMenuButtons/btn_continue_idle.png",
            "quick_continue_hover": "gui/KOMIC/QuickMenuButtons/btn_continue_hover.png",
            "quick_history_idle": "gui/KOMIC/QuickMenuButtons/btn_history_idle.png",
            "quick_history_hover": "gui/KOMIC/QuickMenuButtons/btn_history_hover.png",
            "quick_load_idle": "gui/KOMIC/QuickMenuButtons/btn_load_idle.png",
            "quick_load_hover": "gui/KOMIC/QuickMenuButtons/btn_load_hover.png",
            "quick_options_idle": "gui/KOMIC/QuickMenuButtons/btn_options_idle.png",
            "quick_options_hover": "gui/KOMIC/QuickMenuButtons/btn_options_hover.png",
            "quick_save_idle": "gui/KOMIC/QuickMenuButtons/btn_save_idle.png",
            "quick_save_hover": "gui/KOMIC/QuickMenuButtons/btn_save_hover.png",
            "quick_skip_idle": "gui/KOMIC/QuickMenuButtons/btn_skip_idle.png",
            "quick_skip_hover": "gui/KOMIC/QuickMenuButtons/btn_skip_hover.png",
            "ctc_1": "gui/KOMIC/CTCs/ctc_1.png",
            "ctc_2": "gui/KOMIC/CTCs/ctc_2.png",
            "ctc_3": "gui/KOMIC/CTCs/ctc_3.png",
            "ctc_4": "gui/KOMIC/CTCs/ctc_4.png",
            "ctc_5": "gui/KOMIC/CTCs/ctc_5.png",
            "cursor_1": "gui/KOMIC/Cursors/cursor_1.png",
            "cursor_2": "gui/KOMIC/Cursors/cursor_2.png",
        },
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

    def ensure_audio_pref_defaults():
        changed = False
        if (not hasattr(persistent, "pref_ambient_volume")) or (getattr(persistent, "pref_ambient_volume", None) is None):
            persistent.pref_ambient_volume = 1.0
            changed = True
        if (not hasattr(persistent, "pref_loop_music")) or (getattr(persistent, "pref_loop_music", None) is None):
            persistent.pref_loop_music = True
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

    def _pref_quantize_fraction(value, step=0.1, low=0.0, high=1.0):
        step = max(0.001, float(step or 0.1))
        clamped = _pref_clamp(value, low, high)
        snapped = round(clamped / step) * step
        return round(_pref_clamp(snapped, low, high), 4)

    def _pref_percent_text(value, step=0.1):
        snapped = _pref_quantize_fraction(value, step=step)
        return "{}%".format(int(round(snapped * 100.0)))

    def pref_ambient_volume():
        ensure_audio_pref_defaults()
        return _pref_quantize_fraction(getattr(persistent, "pref_ambient_volume", 1.0), 0.1)

    def apply_ambient_volume():
        ensure_audio_pref_defaults()
        try:
            renpy.music.set_volume(pref_ambient_volume(), channel="ambient")
        except Exception:
            pass

    def pref_audio_bool(attr_name, default=True):
        return bool(getattr(renpy.game.preferences, attr_name, default))

    def pref_disable_engine_high_contrast():
        prefs = renpy.game.preferences
        try:
            renpy.store.Preference("high contrast text", "disable")()
        except Exception:
            pass
        if hasattr(prefs, "high_contrast"):
            prefs.high_contrast = False

    def pref_custom_high_contrast_enabled():
        ensure_visual_pref_defaults()
        return bool(pref_visual_value("pref_custom_high_contrast", False))

    def pref_menu_high_contrast_choice():
        return pref_custom_high_contrast_enabled()

    def pref_set_custom_high_contrast(value):
        persistent.pref_custom_high_contrast = bool(value)
        pref_disable_engine_high_contrast()
        try:
            renpy.save_persistent()
        except Exception:
            pass
        try:
            pref_refresh_accessibility_styles()
        except Exception:
            pass
        try:
            renpy.style.rebuild()
        except Exception:
            pass
        renpy.restart_interaction()

    def pref_set_menu_high_contrast_choice(value):
        pref_set_custom_high_contrast(value)

    def pref_loop_music_enabled():
        ensure_audio_pref_defaults()
        return bool(getattr(persistent, "pref_loop_music", True))

    def set_pref_audio_bool(attr_name, value):
        prefs = renpy.game.preferences
        if hasattr(prefs, attr_name):
            setattr(prefs, attr_name, bool(value))
        renpy.restart_interaction()

    def toggle_pref_audio_bool(attr_name, default=True):
        set_pref_audio_bool(attr_name, not pref_audio_bool(attr_name, default))

    def set_pref_loop_music(value):
        ensure_audio_pref_defaults()
        persistent.pref_loop_music = bool(value)
        renpy.save_persistent()
        renpy.restart_interaction()

    def toggle_pref_loop_music():
        set_pref_loop_music(not pref_loop_music_enabled())

    def pref_bar_value_percent(bar_value, default=0.0, step=0.1):
        try:
            if hasattr(bar_value, "value") and hasattr(bar_value, "change"):
                current = getattr(bar_value, "value", default)
            else:
                adjustment = bar_value.get_adjustment()
                current = getattr(adjustment, "value", default)
        except Exception:
            current = default
        return _pref_percent_text(current, step=step)

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
        if pref_custom_high_contrast_enabled():
            return pref_color_alpha(base_color, 0.96)
        intensity = 0.34 + (_pref_clamp(pref_visual_value("pref_highlight_intensity", 0.70)) * 0.66)
        return pref_color_alpha(base_color, intensity)

    def pref_background_dim_alpha():
        return 0.08 + (_pref_clamp(pref_visual_value("pref_menu_background_dim", 0.60)) * 0.22)

    def pref_background_glow_alpha():
        if not pref_visual_value("pref_screen_effects", True):
            return 0.0
        return 0.03 + (_pref_clamp(pref_visual_value("pref_menu_background_dim", 0.60)) * 0.08)

    def pref_visual_percent(field):
        return _pref_percent_text(pref_visual_value(field, 0.0), step=0.1)

    def pref_visual_bool(field, default=False):
        return bool(pref_visual_value(field, default))

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
        preferred = "feather" if pref_cursor_style_key() == "feather" else "komic"

        if config.mouse is None:
            return "default"

        if preferred in config.mouse:
            return preferred

        return "default" if "default" in config.mouse else None

    def pref_dialogue_window_style_key(style_name=None):
        if style_name is None:
            current = pref_visual_value("pref_dialogue_window_style", "classic")
        else:
            current = style_name

        current = str(current or "classic").lower().replace(" ", "_")

        return {
            "classic": "classic",
            "soft": "komic",
            "dark_glass": "komic",
            "darkglass": "komic",
            "komic": "komic",
            "bright": "bright",
            "fantasy": "fantasy",
            "minimal": "minimal",
        }.get(current, "classic")

    def pref_uses_komic_ui(style_name=None):
        return pref_dialogue_window_style_key(style_name) == "komic"

    def pref_ui_pack_key(style_name=None):
        return "komic" if pref_uses_komic_ui(style_name) else "classic"

    def pref_ui_asset(asset_key, style_name=None, fallback=None):
        pack_key = pref_ui_pack_key(style_name)
        path = UI_THEME_ASSET_PACKS.get(pack_key, {}).get(asset_key)
        classic = UI_THEME_ASSET_PACKS["classic"].get(asset_key)

        if path and renpy.loadable(path):
            return path
        if classic and renpy.loadable(classic):
            return classic
        if fallback and renpy.loadable(fallback):
            return fallback
        return fallback or classic or path

    def pref_window_icon_path(style_name=None):
        return pref_ui_asset("window_icon", style_name, fallback="gui/window_icon.png")

    def pref_game_menu_background(style_name=None):
        return pref_ui_asset("game_menu_background", style_name, fallback="gui/menu/game_menu.png")

    def pref_choice_button_asset(hovered=False, style_name=None):
        return pref_ui_asset("choice_hover" if hovered else "choice_idle", style_name)

    def pref_slot_button_asset(hovered=False, style_name=None):
        return pref_ui_asset("slot_hover" if hovered else "slot_idle", style_name)

    def pref_komic_quick_button_asset(name, hovered=False):
        return pref_ui_asset("quick_{}_{}".format(name, "hover" if hovered else "idle"), "komic")

    def pref_dialogue_window_height(style_name=None):
        return 302 if pref_uses_komic_ui(style_name) else 251

    def pref_dialogue_text_color(style_name=None):
        if pref_custom_high_contrast_enabled():
            return "#fffaf2"
        if pref_uses_komic_ui(style_name):
            return "#f8fcff"
        return "#5f515a"

    def pref_komic_ctc_displayable():
        frames = [
            pref_ui_asset("ctc_1", "komic"),
            pref_ui_asset("ctc_2", "komic"),
            pref_ui_asset("ctc_3", "komic"),
            pref_ui_asset("ctc_4", "komic"),
            pref_ui_asset("ctc_5", "komic"),
        ]

        if not all(frame and renpy.loadable(frame) for frame in frames):
            return Solid("#00000000")

        return Animation(
            frames[0], 0.10,
            frames[1], 0.10,
            frames[2], 0.10,
            frames[3], 0.10,
            frames[4], 0.10,
            frames[3], 0.10,
            frames[2], 0.10,
            frames[1], 0.10,
        )

    def pref_visual_window_style_label():
        return {
            "classic": "Classic",
            "komic": "KOMIC",
            "bright": "Bright",
            "fantasy": "Fantasy Frame",
            "minimal": "Minimal",
        }.get(pref_dialogue_window_style_key(), "Classic")

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
            "glass": "ornate",
            "soft_glow": "soft_glow",
            "softglow": "soft_glow",
        }
        return mapping.get(current, "ornate")

    def pref_panel_border_style_label():
        return {
            "nothing": "Nothing",
            "simple": "Simple",
            "ornate": "Glass",
            "soft_glow": "Soft Glow",
        }.get(pref_panel_border_style_key(), "Glass")

    def pref_selected_highlight_style_key():
        current = str(pref_visual_value("pref_selected_highlight_style", "glow") or "glow").lower()
        return current if current in ("fill", "outline", "glow") else "glow"

    def pref_selected_highlight_style_label():
        return pref_selected_highlight_style_key().title()

    _pref_button_surface_cache = {}
    _pref_panel_surface_cache = {}
    _pref_square_surface_cache = {}
    _pref_controls_remap_rows_cache = {}

    def pref_button_surface(width, height, accent, selected_bg, selected=False, hovered=False, base_color="#00000048", hover_color="#00000062"):
        width = max(1, int(width or 1))
        height = max(1, int(height or 1))
        accent = accent or "#d8b24f"
        selected_bg = selected_bg or accent
        glow_alpha = pref_button_glow_alpha()
        highlight_style = pref_selected_highlight_style_key()
        high_contrast = pref_custom_high_contrast_enabled()
        cache_key = (
            width,
            height,
            accent,
            selected_bg,
            bool(selected),
            bool(hovered),
            base_color,
            hover_color,
            round(glow_alpha, 4),
            highlight_style,
            high_contrast,
        )
        cached = _pref_button_surface_cache.get(cache_key)
        if cached is not None:
            return cached

        if high_contrast:
            fill = pref_selected_fill(selected_bg) if selected else ("#131b28f4" if hovered else "#0c121cf2")
            outer = "#f5f7fb" if selected else ("#dce5f3" if hovered else "#8c97aa")
            inner = pref_color_alpha(accent if selected else "#ffffff", 0.92 if selected else 0.30)
            thickness = 3 if selected else 2

            layers = [
                Transform(Solid(fill), xsize=width, ysize=height),
                Transform(Solid(outer), xsize=width, ysize=thickness),
                Transform(Solid(outer), ypos=(height - thickness), xsize=width, ysize=thickness),
                Transform(Solid(outer), xsize=thickness, ysize=height),
                Transform(Solid(outer), xpos=(width - thickness), xsize=thickness, ysize=height),
                Transform(Solid(inner), xpos=8, ypos=8, xsize=max(1, width - 16), ysize=2),
            ]

            if selected and width > 20 and height > 20:
                layers.append(Transform(Solid(pref_color_alpha("#000000", 0.16)), xpos=4, ypos=4, xsize=max(1, width - 8), ysize=max(1, height - 8)))

            surface = Fixed(*layers, xsize=width, ysize=height)
            _pref_button_surface_cache[cache_key] = surface
            return surface

        layers = [
            Transform(Solid(hover_color if (hovered and not selected) else base_color), xsize=width, ysize=height),
        ]

        edge_alpha = glow_alpha * (0.26 if not hovered and not selected else 0.58 if hovered and not selected else 0.82)

        if selected:
            if highlight_style == "fill":
                layers.append(Transform(Solid(pref_selected_fill(selected_bg)), xsize=width, ysize=height))
            elif highlight_style == "outline":
                border_color = pref_color_alpha(selected_bg, 0.96)
                layers.extend([
                    Transform(Solid(border_color), xsize=width, ysize=2),
                    Transform(Solid(border_color), ypos=(height - 2), xsize=width, ysize=2),
                    Transform(Solid(border_color), xsize=2, ysize=height),
                    Transform(Solid(border_color), xpos=(width - 2), xsize=2, ysize=height),
                ])
            else:
                glow_fill = pref_color_alpha(selected_bg, min(1.0, 0.20 + (glow_alpha * 0.50)))
                glow_edge = pref_color_alpha(selected_bg, min(1.0, 0.52 + glow_alpha))
                layers.extend([
                    Transform(Solid(glow_fill), xsize=width, ysize=height),
                    Transform(Solid(glow_edge), xsize=width, ysize=2),
                    Transform(Solid(glow_edge), ypos=(height - 2), xsize=width, ysize=2),
                    Transform(Solid(glow_edge), xsize=2, ysize=height),
                    Transform(Solid(glow_edge), xpos=(width - 2), xsize=2, ysize=height),
                ])
                if width > 8 and height > 8:
                    layers.append(Transform(Solid(pref_color_alpha(accent, glow_alpha * 0.30)), xpos=3, ypos=3, xsize=(width - 6), ysize=(height - 6)))

        if edge_alpha > 0.0 and width > 12 and height > 8:
            edge_color = pref_color_alpha(accent, min(1.0, edge_alpha))
            side_color = pref_color_alpha(accent, min(1.0, edge_alpha * 0.72))
            layers.extend([
                Transform(Solid(edge_color), xpos=6, xsize=(width - 12), ysize=1),
                Transform(Solid(edge_color), xpos=6, ypos=(height - 1), xsize=(width - 12), ysize=1),
                Transform(Solid(side_color), ypos=4, xsize=1, ysize=(height - 8)),
                Transform(Solid(side_color), xpos=(width - 1), ypos=4, xsize=1, ysize=(height - 8)),
            ])

        surface = Fixed(*layers, xsize=width, ysize=height)
        _pref_button_surface_cache[cache_key] = surface
        return surface

    def pref_panel_surface(width, height, background, accent):
        width = max(1, int(width or 1))
        height = max(1, int(height or 1))
        accent = accent or "#d8b24f"
        border_style = pref_panel_border_style_key()
        high_contrast = pref_custom_high_contrast_enabled()
        cache_key = (width, height, background, accent, border_style, high_contrast)
        cached = _pref_panel_surface_cache.get(cache_key)
        if cached is not None:
            return cached

        if high_contrast:
            panel_fill = pref_color_alpha(background, 0.96)
            edge_color = "#d7e0ea88"
            accent_line = pref_color_alpha(accent, 0.82)
            accent_line_soft = pref_color_alpha(accent, 0.34)

            layers = [
                Transform(Solid("#03060cf2"), xsize=width, ysize=height),
                Transform(Solid(panel_fill), xsize=width, ysize=height),
                Transform(Solid(edge_color), xsize=width, ysize=2),
                Transform(Solid(edge_color), ypos=(height - 2), xsize=width, ysize=2),
                Transform(Solid(edge_color), xsize=2, ysize=height),
                Transform(Solid(edge_color), xpos=(width - 2), xsize=2, ysize=height),
                Transform(Solid(accent_line), xpos=12, ypos=12, xsize=max(1, width - 24), ysize=2),
                Transform(Solid(accent_line_soft), xpos=12, ypos=(height - 14), xsize=max(1, width - 24), ysize=1),
                Transform(Solid("#ffffff06"), xpos=4, ypos=4, xsize=max(1, width - 8), ysize=max(1, height - 8)),
            ]

            surface = Fixed(*layers, xsize=width, ysize=height)
            _pref_panel_surface_cache[cache_key] = surface
            return surface

        base_fill = pref_surface_color(background, "panel")
        inner_fill = pref_surface_color(background, "well")
        shell_border = "#6e6ca540"
        shell_fill = "#26295724"
        inner_sheen = "#9d8cff10"
        accent_top = pref_color_alpha(accent, 0.40)
        accent_bottom = pref_color_alpha(accent, 0.20)
        accent_glow = pref_color_alpha(accent, 0.12)

        if border_style == "simple":
            layers = [
                Transform(Solid(shell_fill), xsize=width, ysize=height),
                Transform(Solid(base_fill), xsize=width, ysize=height),
            ]
            layers.extend([
                Transform(Solid(shell_border), xsize=width, ysize=1),
                Transform(Solid(shell_border), ypos=(height - 1), xsize=width, ysize=1),
                Transform(Solid(shell_border), xsize=1, ysize=height),
                Transform(Solid(shell_border), xpos=(width - 1), xsize=1, ysize=height),
                Transform(Solid(accent_top), xpos=12, ypos=12, xsize=max(1, width - 24), ysize=1),
            ])
        elif border_style == "soft_glow":
            soft_wash = pref_color_alpha(accent, 0.05)
            soft_sheen = pref_color_alpha("#ffffff", 0.025)
            layers = [
                Transform(Solid(shell_fill), xsize=width, ysize=height),
                Transform(Solid(base_fill), xsize=width, ysize=height),
            ]
            layers.extend([
                Transform(Solid(soft_wash), xsize=width, ysize=height),
                Transform(Solid(soft_sheen), xsize=width, ysize=height),
                Transform(Solid(pref_color_alpha(accent, 0.22)), xpos=12, ypos=10, xsize=max(1, width - 24), ysize=1),
                Transform(Solid(pref_color_alpha(accent, 0.12)), xpos=12, ypos=11, xsize=max(1, width - 24), ysize=1),
                Transform(Solid(pref_color_alpha(accent, 0.14)), xpos=12, ypos=(height - 12), xsize=max(1, width - 24), ysize=1),
                Transform(Solid(pref_color_alpha(accent, 0.08)), xpos=12, ypos=(height - 13), xsize=max(1, width - 24), ysize=1),
            ])
        else:
            layers = [
                Transform(Solid(shell_fill), xsize=width, ysize=height),
            ]
            layers.extend([
                Transform(Solid(shell_border), xsize=width, ysize=1),
                Transform(Solid(shell_border), ypos=(height - 1), xsize=width, ysize=1),
                Transform(Solid(shell_border), xsize=1, ysize=height),
                Transform(Solid(shell_border), xpos=(width - 1), xsize=1, ysize=height),
                Transform(Solid(inner_sheen), xpos=1, ypos=1, xsize=max(1, width - 2), ysize=max(1, height - 2)),
                Transform(Solid(inner_fill), xpos=12, ypos=12, xsize=max(1, width - 24), ysize=max(1, height - 24)),
                Transform(Solid(accent_top), xpos=12, ypos=12, xsize=max(1, width - 24), ysize=1),
                Transform(Solid(accent_bottom), xpos=12, ypos=(height - 13), xsize=max(1, width - 24), ysize=1),
            ])

        surface = Fixed(*layers, xsize=width, ysize=height)
        _pref_panel_surface_cache[cache_key] = surface
        return surface

    def pref_square_surface(width=68, height=68, accent=None):
        width = max(1, int(width or 1))
        height = max(1, int(height or 1))
        accent = accent or "#d8b24f"
        high_contrast = pref_custom_high_contrast_enabled()
        cache_key = (width, height, accent, high_contrast)
        cached = _pref_square_surface_cache.get(cache_key)
        if cached is not None:
            return cached

        if high_contrast:
            surface = Fixed(
                Transform(Solid("#0c121cf2"), xsize=width, ysize=height),
                Transform(Solid("#dce5f3"), xsize=width, ysize=2),
                Transform(Solid("#dce5f3"), ypos=(height - 2), xsize=width, ysize=2),
                Transform(Solid("#dce5f3"), xsize=2, ysize=height),
                Transform(Solid("#dce5f3"), xpos=(width - 2), xsize=2, ysize=height),
                Transform(Solid(pref_color_alpha(accent, 0.86)), xpos=8, ypos=8, xsize=max(1, width - 16), ysize=2),
                xsize=width,
                ysize=height,
            )
            _pref_square_surface_cache[cache_key] = surface
            return surface

        surface = Fixed(
            Transform(Solid("#ffffff08"), xpos=2, ypos=2, xsize=max(1, width - 4), ysize=max(1, height - 4)),
            Transform(Solid(accent), xpos=0, ypos=0, xsize=width, ysize=2),
            xsize=width,
            ysize=height,
        )
        _pref_square_surface_cache[cache_key] = surface
        return surface

    def pref_prime_controls_ui_cache():
        theme = pref_ui_tab_colors("controls")
        accent = theme["accent"]
        selected_bg = theme["selected_bg"]

        pref_panel_surface(540, 720, theme["panel_bg"], accent)
        pref_panel_surface(885, 720, theme["panel_bg"], accent)
        pref_panel_surface(690, 682, theme["panel_bg"], accent)
        pref_panel_surface(690, 332, theme["panel_bg"], accent)
        pref_panel_surface(845, 682, theme["panel_bg"], accent)
        pref_panel_surface(740, 384, theme["panel_bg"], accent)
        pref_panel_surface(740, 682, theme["panel_bg"], accent)
        pref_panel_surface(740, 280, theme["panel_bg"], accent)
        pref_panel_surface(740, 250, theme["panel_bg"], accent)
        pref_panel_surface(740, 218, theme["panel_bg"], accent)
        pref_panel_surface(740, 178, theme["panel_bg"], accent)
        pref_panel_surface(740, 332, theme["panel_bg"], accent)
        pref_panel_surface(1450, 332, theme["panel_bg"], accent)
        pref_panel_surface(587, 418, theme["panel_bg"], accent)
        pref_panel_surface(587, 246, theme["panel_bg"], accent)
        pref_panel_surface(551, 78, "#10172acc", accent)
        pref_square_surface(68, 68, accent)

        for width, height in (
            (236, 46),
            (190, 46),
            (250, 46),
            (230, 46),
            (224, 44),
            (220, 46),
            (211, 46),
            (180, 44),
            (170, 44),
            (152, 42),
            (150, 44),
            (130, 42),
            (112, 112),
            (66, 66),
            (315, 40),
            (300, 42),
            (145, 44),
            (158, 54),
            (120, 40),
            (90, 40),
            (795, 56),
            (760, 70),
            (760, 66),
            (760, 60),
        ):
            pref_button_surface(width, height, accent, selected_bg, selected=False, hovered=False)
            pref_button_surface(width, height, accent, selected_bg, selected=False, hovered=True)
            pref_button_surface(width, height, accent, selected_bg, selected=True, hovered=False)

    def _pref_controls_bindings_cache_key(bindings):
        try:
            items = []
            for action, values in sorted(bindings.items()):
                items.append((action, tuple(sorted(values))))
            return tuple(items)
        except Exception:
            return None

    def pref_get_controls_remap_rows(remapper):
        bindings = remapper.get_current_bindings()
        cache_key = (
            _pref_controls_bindings_cache_key(bindings),
            str(getattr(persistent, "controller_layout", "generic")),
        )
        cached = _pref_controls_remap_rows_cache.get(cache_key)
        if cached is not None:
            return cached

        rows = []
        for title, act, p in pad_remap.REMAPPABLE_EVENTS:
            act_id = act.replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
            pad_images = pad_remap.get_images(act, bindings)
            rows.append((title, act, act_id, pad_images))

        _pref_controls_remap_rows_cache[cache_key] = rows
        return rows

    def pref_prime_controls_remap_cache(remapper):
        pref_get_controls_remap_rows(remapper)

    def pref_dialogue_window_background(style_name=None, alpha=None, width=1526, height=251):
        style_name = pref_dialogue_window_style_key(style_name)
        alpha = _pref_clamp(pref_visual_value("pref_textbox_opacity", 0.80) if alpha is None else alpha)
        base_asset = pref_ui_asset("textbox", style_name, fallback="gui/hud/msgbox_720p.png")
        base = Transform(base_asset, size=(width, height), xalign=0.5, yalign=0.0, alpha=alpha)

        if pref_custom_high_contrast_enabled():
            return Fixed(
                Transform(base_asset, size=(width, height), xalign=0.5, yalign=0.0, alpha=max(0.18, alpha * 0.28)),
                Transform(Solid("#04070ee4"), xsize=width, ysize=height),
                Transform(Solid("#f4f0dc"), xsize=width, ysize=2, ypos=0),
                Transform(Solid("#f4f0dc"), xsize=width, ysize=2, ypos=(height - 2)),
                xsize=width,
                ysize=height,
            )

        if style_name == "komic":
            return Transform(base_asset, size=(width, height), xalign=0.5, yalign=0.0, alpha=max(0.58, alpha))
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
                Transform(base_asset, size=(width, height), xalign=0.5, yalign=0.0, alpha=max(0.48, alpha * 0.78)),
                Transform(Solid("#2414347a"), xsize=width, ysize=height),
                Transform(Solid("#e0b5ff88"), xsize=width, ysize=2, ypos=2),
                Transform(Solid("#e0b5ff55"), xsize=width, ysize=2, ypos=(height - 4)),
                xsize=width,
                ysize=height,
            )
        if style_name == "minimal":
            return Fixed(
                Transform(base_asset, size=(width, height), xalign=0.5, yalign=0.0, alpha=max(0.42, alpha * 0.72)),
                Transform(Solid("#0d112488"), xsize=width, ysize=height),
                Transform(Solid("#c7d8ff55"), xsize=width, ysize=2, ypos=0),
                xsize=width,
                ysize=height,
            )
        return base

    def pref_dialogue_namebox_background(style_name=None, alpha=None, width=380, height=78):
        style_name = pref_dialogue_window_style_key(style_name)
        alpha = _pref_clamp(pref_visual_value("pref_textbox_opacity", 0.80) if alpha is None else alpha)
        base_asset = pref_ui_asset("namebox", style_name, fallback="gui/hud/msgbox_name_header_720p.png")
        base = Transform(base_asset, size=(width, height), alpha=alpha)

        if pref_custom_high_contrast_enabled():
            return Fixed(
                Transform(base_asset, size=(width, height), alpha=max(0.16, alpha * 0.24)),
                Transform(Solid("#04070ef2"), xsize=width, ysize=height),
                Transform(Solid("#f4f0dc"), xsize=width, ysize=2, ypos=0),
                Transform(Solid("#f4f0dc"), xsize=width, ysize=2, ypos=(height - 2)),
                xsize=width,
                ysize=height,
            )

        if style_name == "komic":
            return Fixed(
                Transform(base_asset, size=(width, height), alpha=max(0.42, alpha * 0.90)),
                Transform(Solid("#ffffff06"), xpos=8, ypos=8, xsize=max(1, width - 16), ysize=max(1, height - 16)),
                xsize=width,
                ysize=height,
            )
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
                Transform(base_asset, size=(width, height), alpha=max(0.48, alpha * 0.78)),
                Transform(Solid("#2414347a"), xsize=width, ysize=height),
                Transform(Solid("#e0b5ff88"), xsize=width, ysize=2, ypos=1),
                xsize=width,
                ysize=height,
            )
        if style_name == "minimal":
            return Fixed(
                Transform(base_asset, size=(width, height), alpha=max(0.42, alpha * 0.72)),
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
        return "display"

    def apply_visual_preferences():
        ensure_visual_pref_defaults()
        pref_disable_engine_high_contrast()
        duration = pref_transition_duration()
        transition = None if duration <= 0.01 else Dissolve(duration)
        config.window_show_transition = transition
        config.window_hide_transition = transition
        renpy.store.default_mouse = pref_mouse_cursor_name()
        try:
            pref_refresh_accessibility_styles()
        except Exception:
            pass

    ensure_visual_pref_defaults()
    ensure_audio_pref_defaults()
    try:
        renpy.music.register_channel("ambient", "sfx", True, True)
    except Exception:
        pass
    _feather_mouse_frames = [ ("gui/button/test.png", 2, 3) ] if renpy.loadable("gui/button/test.png") else None
    _komic_mouse_frames = [ ("gui/KOMIC/Cursors/cursor_1.png", 1, 1) ] if renpy.loadable("gui/KOMIC/Cursors/cursor_1.png") else None
    _default_mouse_frames = _komic_mouse_frames or _feather_mouse_frames

    if _default_mouse_frames:
        config.mouse = {
            "default": list(_default_mouse_frames),
        }

        if _feather_mouse_frames:
            config.mouse["feather"] = list(_feather_mouse_frames)

        if _komic_mouse_frames:
            config.mouse["komic"] = list(_komic_mouse_frames)
    else:
        config.mouse = None
    config.mouse_displayable = None
    apply_visual_preferences()
    apply_ambient_volume()

    class PersistentFloatAdjustment(BarValue):
        def __init__(self, field, default=0.0, step=0.1, changed=None):
            self.field = field
            self.default = float(default)
            self.step = step
            self._changed = changed
            self._adjustment = None
            super(PersistentFloatAdjustment, self).__init__()

        def current_value(self):
            return _pref_quantize_fraction(pref_visual_value(self.field, self.default), self.step)

        def get_adjustment(self):
            current = self.current_value()
            if abs(current - _pref_clamp(pref_visual_value(self.field, self.default))) > 0.0001:
                pref_set_visual_value(self.field, current)
            if self._adjustment is None:
                self._adjustment = ui.adjustment(
                    value=current,
                    range=1.0,
                    step=self.step,
                    adjustable=True,
                    changed=self.set_value,
                )
            elif abs(self._adjustment.value - current) > 0.0001:
                self._adjustment.value = current
            return self._adjustment

        def set_value(self, value):
            pref_set_visual_value(self.field, _pref_quantize_fraction(value, self.step))
            if self._changed is not None:
                self._changed()

    class QuantizedPreferenceAdjustment(BarValue):
        def __init__(self, pref_name, pref_attr, default=1.0, step=0.1):
            self.pref_name = pref_name
            self.pref_attr = pref_attr
            self.default = float(default)
            self.step = float(step)
            self._adjustment = None
            super(QuantizedPreferenceAdjustment, self).__init__()

        def current_value(self):
            prefs = renpy.game.preferences
            return _pref_quantize_fraction(getattr(prefs, self.pref_attr, self.default), self.step)

        def get_adjustment(self):
            current = _pref_clamp(getattr(renpy.game.preferences, self.pref_attr, self.default))
            snapped = self.current_value()
            if abs(snapped - current) > 0.0001:
                self.set_value(snapped)
            if self._adjustment is None:
                self._adjustment = ui.adjustment(
                    value=snapped,
                    range=1.0,
                    step=self.step,
                    adjustable=True,
                    changed=self.set_value,
                )
            elif abs(self._adjustment.value - snapped) > 0.0001:
                self._adjustment.value = snapped
            return self._adjustment

        def set_value(self, value):
            renpy.store.Preference(self.pref_name, _pref_quantize_fraction(value, self.step))()

    _pref_adjustment_cache = {}

    def pref_visual_adjustment(field, default=0.0, step=0.1, changed=None):
        key = ("visual_adj", field, float(default), float(step))
        adj = _pref_adjustment_cache.get(key)
        if adj is None:
            def _changed(value, _field=field, _step=step, _extra=changed):
                snapped = _pref_quantize_fraction(value, _step)
                pref_set_visual_value(_field, snapped)
                if _extra is not None:
                    _extra()

            adj = ui.adjustment(
                value=_pref_quantize_fraction(pref_visual_value(field, default), step),
                range=1.0,
                step=step,
                adjustable=True,
                force_step=True,
                changed=_changed,
            )
            _pref_adjustment_cache[key] = adj
        return adj

    def pref_quantized_adjustment(pref_name, pref_attr, default=1.0, step=0.1):
        key = ("pref_adj", pref_name, pref_attr, float(default), float(step))
        adj = _pref_adjustment_cache.get(key)
        if adj is None:
            def _changed(value, _pref_name=pref_name, _step=step):
                snapped = _pref_quantize_fraction(value, _step)
                adj.value = snapped
                renpy.store.Preference(_pref_name, snapped)()

            adj = ui.adjustment(
                value=_pref_quantize_fraction(getattr(renpy.game.preferences, pref_attr, default), step),
                range=1.0,
                step=step,
                adjustable=True,
                force_step=True,
                changed=_changed,
            )
            _pref_adjustment_cache[key] = adj
        return adj

    def pref_ambient_adjustment(step=0.1):
        key = ("ambient_adj", float(step))
        adj = _pref_adjustment_cache.get(key)
        if adj is None:
            def _changed(value, _step=step):
                snapped = _pref_quantize_fraction(value, _step)
                adj.value = snapped
                persistent.pref_ambient_volume = snapped
                apply_ambient_volume()

            adj = ui.adjustment(
                value=pref_ambient_volume(),
                range=1.0,
                step=step,
                adjustable=True,
                force_step=True,
                changed=_changed,
            )
            _pref_adjustment_cache[key] = adj
        return adj

    def set_all_mute(value):
        prefs = renpy.game.preferences
        if hasattr(prefs, "mute"):
            prefs.mute = {"music": value, "sound": value, "voice": value}
        for ch in ("music", "sound", "voice", "ambient"):
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
        if hasattr(prefs, "high_contrast"):
            prefs.high_contrast = False
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
        persistent.pref_ambient_volume = 1.0
        persistent.pref_loop_music = True

        set_all_mute(False)
        for ch in ("music", "sound", "voice"):
            try:
                renpy.music.set_volume(1.0, channel=ch)
            except Exception:
                pass
        apply_ambient_volume()

        for field, value in (
            ("hold_to_skip", False),
            ("left_stick_invert_x", False),
            ("left_stick_invert_y", False),
            ("right_stick_invert_x", False),
            ("right_stick_invert_y", False),
            ("left_stick_sensitivity", 1.0),
            ("right_stick_sensitivity", 1.0),
            ("left_stick_dead_zone_fallback", 4096),
            ("right_stick_dead_zone_fallback", 4096),
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
            "audio": "Volume balance and playback controls.",
            "controls": "Gamepad calibration, bindings, and stick tuning.",
            "access": "Readability, contrast, and narration support.",
            "visuals": "Customise the look and feel of the game interface.",
        }.get(current, "Screen mode, skip rules, and text pacing.")

    def pref_tab_colors(current):
        return PREF_TAB_COLORS.get(current, PREF_TAB_COLORS["display"])

    def pref_ui_tab_colors(current):
        colors = dict(pref_tab_colors(current))

        if not pref_custom_high_contrast_enabled():
            return colors

        accent = "#f3dfad"

        colors.update({
            "accent": accent,
            "accent_soft": pref_color_alpha(accent, 0.18),
            "selected_bg": "#fff1c9",
            "selected_text": "#0d1117",
            "sidebar_bg": "#05070cf4",
            "main_bg": "#06080de8",
            "header_bg": "#00000000",
            "panel_bg": "#09111df4",
            "well_bg": "#04070ef8",
        })

        return colors

    def pref_ui_text_color(role, accent=None):
        if pref_custom_high_contrast_enabled():
            return {
                "screen_title": accent or "#fff1c9",
                "screen_subtitle": "#f6f8fc",
                "section_title": "#fffaf0",
                "body": "#ffffff",
                "muted": "#dde4ee",
                "label": "#edf2f8",
                "sidebar_value": "#fff1c9",
                "setting_label": "#ffffff",
                "button": "#f5f7fb",
                "button_hover": accent or "#fff1c9",
                "selected_button": "#0d1117",
                "percent": "#fff1c9",
                "rule": accent or "#f3dfad",
            }.get(role, "#f5f7fb")

        return {
            "screen_title": "#f6f1e7",
            "screen_subtitle": "#d6deef",
            "section_title": accent or "#fcf7ee",
            "body": "#edf3ff",
            "muted": "#b9c5d8",
            "label": "#95a4bc",
            "sidebar_value": accent or "#edf3ff",
            "setting_label": "#edf3ff",
            "button": "#d8d1ea",
            "button_hover": accent or "#ffffff",
            "selected_button": "#1b2431",
            "percent": "#f1d08a",
            "rule": accent or "#fcf7ee",
        }.get(role, "#edf3ff")

    def pref_ui_strip_color(strong=True):
        if pref_custom_high_contrast_enabled():
            return "#000000c6" if strong else "#00000092"
        return "#00000000"

    def pref_refresh_accessibility_styles():
        try:
            _body = pref_ui_text_color("body")
            _muted = pref_ui_text_color("muted")
            _label = pref_ui_text_color("label")
            _button = pref_ui_text_color("button")
            _selected = pref_ui_text_color("selected_button")
            _hover = pref_ui_text_color("button_hover", pref_theme_palette()["accent"])
            style.pref_screen_title.color = pref_ui_text_color("screen_title")
            style.pref_screen_subtitle.color = pref_ui_text_color("screen_subtitle")
            style.pref_section_title.color = pref_ui_text_color("section_title")
            style.pref_body_text.color = _body
            style.pref_muted_text.color = _muted
            style.pref_label_text.color = _label
            style.pref_sidebar_value_text.color = pref_ui_text_color("sidebar_value")
            style.pref_setting_label.color = pref_ui_text_color("setting_label")
            style.pref_sidebar_button_text.color = _body
            style.pref_sidebar_button_text.hover_color = _hover
            style.pref_sidebar_button_text.selected_color = _selected
            style.pref_setting_btn_text.color = _button
            style.pref_setting_btn_text.hover_color = _hover
            style.pref_setting_btn_text.selected_color = _selected
        except Exception:
            pass

    def pref_sidebar_rows(current):
        prefs = renpy.game.preferences

        if current == "display":
            return [
                ("Mode", "Fullscreen" if getattr(prefs, "fullscreen", False) else "Window"),
                ("Skip Unseen", pref_bool_text(getattr(prefs, "skip_unseen", False))),
                ("Language", get_ui_lang_label(get_ui_lang())),
            ]

        if current == "audio":
            return [
                ("Mute All", "__live_audio_mute__"),
                ("Music", "__live_audio_music__"),
                ("Ambience", "__live_audio_ambient__"),
                ("SFX", "__live_audio_sfx__"),
                ("Voice", "__live_audio_voice__"),
                ("Ducking", "__live_audio_ducking__"),
            ]

        if current == "controls":
            if "pref_controls_section_tab" in globals() and pref_controls_section_tab == "bindings":
                prompt_label = str(getattr(persistent, "controller_layout", "generic")).replace("_", " ").title()
                if "pref_controls_layout_label" in globals():
                    prompt_label = pref_controls_layout_label()

                edited_count = pref_controls_remaps_edited_count() if "pref_controls_remaps_edited_count" in globals() else 0
                empty_count = pref_controls_empty_slots_count() if "pref_controls_empty_slots_count" in globals() else 0

                return [
                    ("Prompt Set", prompt_label),
                    ("Hold To Skip", pref_bool_text(getattr(persistent, "hold_to_skip", False))),
                    ("Remaps Edited", str(edited_count)),
                    ("Empty Slots", str(empty_count)),
                ]

            return [
                ("Hold To Skip", pref_bool_text(getattr(persistent, "hold_to_skip", False))),
                ("Layout", str(getattr(persistent, "controller_layout", "generic")).replace("_", " ").title()),
                ("Left Y Invert", pref_bool_text(getattr(persistent, "left_stick_invert_y", False))),
                ("Right Y Invert", pref_bool_text(getattr(persistent, "right_stick_invert_y", False))),
                ("Sensitivity", pref_controls_sensitivity_summary() if "pref_controls_sensitivity_summary" in globals() else "Normal"),
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
            ("Contrast", pref_bool_text(pref_menu_high_contrast_choice())),
            ("Self-Voicing", pref_bool_text(getattr(prefs, "self_voicing", False))),
        ]

    def next_pref_tab(current, step):
        try:
            idx = PREF_TABS.index(current)
        except Exception:
            idx = 0
        return PREF_TABS[(idx + step) % len(PREF_TABS)]

    def pref_sidebar_icon():
        themed_icon = pref_window_icon_path()
        for candidate in ("gui/logos/settings.png", themed_icon):
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

    def pref_live_bar_percent_dd(st, at, bar_value, default=0.0, style="pref_label_text", color=None, step=0.1):
        kwargs = {"style": style}
        if color is not None:
            kwargs["color"] = color
        return Text(pref_bar_value_percent(bar_value, default=default, step=step), **kwargs), 0.02

    def pref_live_bar_percent_displayable(bar_value, default=0.0, style="pref_label_text", color=None, step=0.1):
        return DynamicDisplayable(pref_live_bar_percent_dd, bar_value, default, style, color, step)

    def pref_live_attr_percent_dd(st, at, pref_attr, style="pref_label_text", color=None, step=0.1):
        kwargs = {"style": style}
        if color is not None:
            kwargs["color"] = color
        value = getattr(renpy.game.preferences, pref_attr, 1.0)
        return Text(_pref_percent_text(value, step=step), **kwargs), 0.02

    def pref_live_attr_percent_displayable(pref_attr, style="pref_label_text", color=None, step=0.1):
        return DynamicDisplayable(pref_live_attr_percent_dd, pref_attr, style, color, step)

    def pref_live_bool_dd(st, at, getter, true_text, false_text, style="pref_label_text", color=None):
        kwargs = {"style": style}
        if color is not None:
            kwargs["color"] = color
        return Text(true_text if getter() else false_text, **kwargs), 0.02

    def pref_live_bool_displayable(getter, true_text, false_text, style="pref_label_text", color=None):
        return DynamicDisplayable(pref_live_bool_dd, getter, true_text, false_text, style, color)

    def pref_audio_percent(pref_attr):
        return _pref_percent_text(getattr(renpy.game.preferences, pref_attr, 1.0), step=0.1)

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
    $ _text_color = pref_ui_text_color("button")
    $ _hover_text = pref_ui_text_color("button_hover", _accent)
    $ _selected_text_color = pref_ui_text_color("selected_button") if pref_custom_high_contrast_enabled() else _selected_text
    $ _xsize = 190 if xsize is None else xsize
    $ _ysize = 52 if ysize is None else ysize
    $ _idle_background = pref_button_surface(_xsize, _ysize, _accent, _selected_bg)
    $ _hover_background = pref_button_surface(_xsize, _ysize, _accent, _selected_bg, hovered=True)
    $ _selected_background = pref_button_surface(_xsize, _ysize, _accent, _selected_bg, selected=True)

    textbutton label:
        style "pref_choice_button"
        text_style text_style
        action action
        selected selected
        background _idle_background
        hover_background _hover_background
        selected_background _selected_background
        selected_hover_background _selected_background
        xsize _xsize
        ysize _ysize
        text_xalign 0.5
        text_yalign 0.5
        text_xmaximum (_xsize - 20)
        text_color _text_color
        text_hover_color _hover_text
        text_selected_color _selected_text_color
        text_selected_hover_color _selected_text_color
        if button_id is not None:
            id button_id


screen pref_tiny_button(label, action, selected=False, tooltip=None, use_alt=None, text_style="pref_setting_btn_text", button_id=None, xsize=None, ysize=None, accent=None, selected_bg=None, selected_text=None):
    $ _label = pref_L(label)
    use pref_small_button(_label, action, selected=selected, text_style=text_style, button_id=button_id, xsize=xsize, ysize=ysize, accent=accent, selected_bg=selected_bg, selected_text=selected_text)


screen pref_icon_button(img, action, tooltip_key=None, button_id=None):
    $ _accent = pref_theme_palette()["accent"]
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
            add pref_square_surface(68, 68, _accent)
            add Transform(img, fit="contain", xsize=48, ysize=48, xalign=0.5, yalign=0.5)


screen pref_add_binding_button(action, tooltip_key=None, button_id=None):
    $ _accent = pref_theme_palette()["accent"]
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
            add pref_square_surface(68, 68, _accent)
            text pref_L("pref_button_add_binding") style "pref_setting_btn_text" xsize 68 ysize 68 xalign 0.5 yalign 0.5 text_align 0.5


screen pref_hub_panel(title, subtitle=None, xsize=400, ysize=200, accent="#d8b24f", background="#241d4358", panel_accent=None):
    $ surface_accent = panel_accent if panel_accent is not None else pref_theme_palette()["accent"]
    $ _high_contrast = pref_custom_high_contrast_enabled()
    $ _title_color = pref_ui_text_color("section_title", accent)
    $ _subtitle_color = pref_ui_text_color("label")
    $ _rule_color = pref_color_alpha(pref_ui_text_color("rule", accent), 0.88 if _high_contrast else 0.40)
    fixed:
        xsize xsize
        ysize ysize
        clipping True

        add pref_panel_surface(xsize, ysize, background, surface_accent)

        vbox:
            xpos 18
            ypos 14
            xsize (xsize - 36)
            spacing 6

            if _high_contrast:
                frame:
                    background pref_ui_strip_color(True)
                    xfill True
                    xpadding 10
                    ypadding 6
                    vbox:
                        spacing 4
                        text title style "pref_section_title" color _title_color
                        if subtitle:
                            text subtitle style "pref_label_text" color _subtitle_color
            else:
                text title style "pref_section_title" color accent
                if subtitle:
                    text subtitle style "pref_label_text" color "#d5dcef"
            add Solid(_rule_color) xsize (xsize - 36) ysize (2 if _high_contrast else 1)
            transclude


screen pref_hub_slider_row(label_key, value, tooltip_key=None, variant="default", style_name="pref_bar", label_width=250, slider_width=360, dimmed=False, show_percent=False, percent_step=0.1):
    $ _row_alpha = 0.48 if dimmed else 1.0
    $ _setting_color = pref_ui_text_color("setting_label")
    $ _label_color = pref_ui_text_color("label")
    $ _percent_color = pref_ui_text_color("percent")

    hbox:
        at Transform(alpha=_row_alpha)
        spacing 12

        fixed:
            xsize label_width
            ysize 64
            text pref_L(label_key) style "pref_setting_label" color _setting_color yalign 0.5

        fixed:
            xsize 42
            ysize 64
            text pref_L("pref_label_min") style "pref_label_text" color _label_color xalign 1.0 yalign 0.5

        fixed:
            xsize slider_width
            ysize 64
            use ui_slider(value, style_name=style_name, variant=variant, xpos=0, ypos=16, xsize=slider_width, ysize=32)

        fixed:
            xsize 42
            ysize 64
            text pref_L("pref_label_max") style "pref_label_text" color _label_color xalign 0.0 yalign 0.5

        if show_percent:
            fixed:
                xsize 58
                ysize 64
                add pref_live_bar_percent_displayable(value, style="pref_label_text", color=_percent_color, step=percent_step) xalign 1.0 yalign 0.5


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

    default pref_tab = initial_pref_tab()
    default pref_remapper = pad_remap.ControllerRemap()
    default pref_yadj = ui.adjustment()
    default pref_access_yadj = ui.adjustment()

    on "show" action [Function(pref_disable_engine_high_contrast), Function(pref_refresh_accessibility_styles), Function(pref_prime_controls_ui_cache), Function(pref_prime_controls_remap_cache, pref_remapper)]
    on "hide" action Function(renpy.restart_interaction)

    key pad_config.get_event("page_left") action [SetScreenVariable("pref_tab", next_pref_tab(pref_tab, -1)), Function(remember_pref_tab, next_pref_tab(pref_tab, -1))]
    key pad_config.get_event("page_right") action [SetScreenVariable("pref_tab", next_pref_tab(pref_tab, 1)), Function(remember_pref_tab, next_pref_tab(pref_tab, 1))]
    key "K_q" action [SetScreenVariable("pref_tab", next_pref_tab(pref_tab, -1)), Function(remember_pref_tab, next_pref_tab(pref_tab, -1))]
    key "K_e" action [SetScreenVariable("pref_tab", next_pref_tab(pref_tab, 1)), Function(remember_pref_tab, next_pref_tab(pref_tab, 1))]

    $ tab_colors = pref_ui_tab_colors(pref_tab)
    $ _high_contrast = pref_custom_high_contrast_enabled()
    $ pref_heading = pref_tab_heading(pref_tab)
    $ pref_subtitle = pref_tab_subtitle(pref_tab)
    $ sidebar_rows = pref_sidebar_rows(pref_tab)
    $ sidebar_icon = pref_sidebar_icon()
    $ pref_shell_bg = "#00000000"
    $ pref_sidebar_bg = tab_colors["sidebar_bg"]
    $ pref_main_bg = tab_colors["main_bg"]
    $ pref_header_bg = tab_colors["header_bg"]
    $ pref_sidebar_w = 280
    $ pref_sidebar_h = 760
    $ pref_sidebar_spacing = 10

    add Transform("gui/inventory_system/gui/inventory_bg.png", xsize=config.screen_width, ysize=config.screen_height)
    add Solid(pref_color_alpha("#020617", 0.34 if _high_contrast else pref_background_dim_alpha()))
    if pref_visual_bool("pref_screen_effects") and (not _high_contrast):
        add Solid(pref_color_alpha("#8f6dff", pref_background_glow_alpha()))
    if not _high_contrast:
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
                            if _high_contrast:
                                frame:
                                    background pref_ui_strip_color(True)
                                    xpadding 10
                                    ypadding 6
                                    vbox:
                                        spacing 4
                                        text "CONFIG" style "pref_section_title" color pref_ui_text_color("section_title", tab_colors["accent"])
                                        text "Game settings and system options." style "pref_label_text" color pref_ui_text_color("label")
                            else:
                                text "CONFIG" style "pref_section_title"
                                text "Game settings and system options." style "pref_label_text"

                    null height 8

                    for tab in PREF_TABS:
                        $ sidebar_tab_colors = pref_ui_tab_colors(tab)
                        textbutton pref_L("pref_tab_" + tab):
                            style "pref_sidebar_button"
                            text_style "pref_sidebar_button_text"
                            action [SetScreenVariable("pref_tab", tab), Function(remember_pref_tab, tab)]
                            selected (pref_tab == tab)
                            selected_background pref_selected_fill(sidebar_tab_colors["selected_bg"])
                            text_color pref_ui_text_color("button")
                            text_selected_color sidebar_tab_colors["selected_text"]
                            text_hover_color pref_ui_text_color("button_hover", sidebar_tab_colors["accent"])

                    null height 14
                    text _("Overview") style "pref_label_text" color pref_ui_text_color("section_title", tab_colors["accent"])

                    for row_label, row_value in sidebar_rows:
                        hbox:
                            xfill True
                            text row_label style "pref_muted_text" color pref_ui_text_color("muted")
                            if row_value == "__live_audio_mute__":
                                add pref_live_bool_displayable(is_all_muted, pref_L("pref_button_on"), pref_L("pref_button_off"), style="pref_sidebar_value_text", color=pref_ui_text_color("sidebar_value", tab_colors["accent"])) xalign 1.0
                            elif row_value == "__live_audio_music__":
                                add pref_live_bar_percent_displayable(pref_quantized_adjustment("music volume", "music_volume"), style="pref_sidebar_value_text", color=pref_ui_text_color("sidebar_value", tab_colors["accent"])) xalign 1.0
                            elif row_value == "__live_audio_ambient__":
                                add pref_live_bar_percent_displayable(pref_ambient_adjustment(), style="pref_sidebar_value_text", color=pref_ui_text_color("sidebar_value", tab_colors["accent"])) xalign 1.0
                            elif row_value == "__live_audio_sfx__":
                                add pref_live_bar_percent_displayable(pref_quantized_adjustment("sound volume", "sound_volume"), style="pref_sidebar_value_text", color=pref_ui_text_color("sidebar_value", tab_colors["accent"])) xalign 1.0
                            elif row_value == "__live_audio_voice__":
                                add pref_live_bar_percent_displayable(pref_quantized_adjustment("voice volume", "voice_volume"), style="pref_sidebar_value_text", color=pref_ui_text_color("sidebar_value", tab_colors["accent"])) xalign 1.0
                            elif row_value == "__live_audio_ducking__":
                                add pref_live_bool_displayable(lambda : getattr(renpy.game.preferences, "self_voicing_volume_drop", 0.0) > 0.0, pref_L("pref_button_on"), pref_L("pref_button_off"), style="pref_sidebar_value_text", color=pref_ui_text_color("sidebar_value", tab_colors["accent"])) xalign 1.0
                            else:
                                text row_value style "pref_sidebar_value_text" color pref_ui_text_color("sidebar_value", tab_colors["accent"]) xalign 1.0

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

                        if _high_contrast:
                            frame:
                                background pref_ui_strip_color(True)
                                xpadding 12
                                ypadding 10
                                vbox:
                                    spacing 4
                                    text pref_heading style "pref_screen_title" color pref_ui_text_color("screen_title", tab_colors["accent"])
                                    text pref_subtitle style "pref_screen_subtitle" color pref_ui_text_color("screen_subtitle")
                        else:
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

                        use preferences_tab_controls(pref_remapper, pref_yadj, active=(pref_tab == "controls"))

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
