# preferences_tabs/controls_tab.rpy

default pref_controls_section_tab = "bindings"
default pref_controls_binding_category = "all"
default pref_controls_binding_search = ""
default pref_controls_selected_action = "button_select"
default pref_controls_selected_slot = 0

init -1 python:
    import math

    try:
        import pygame_sdl2 as pref_controls_pygame
        from pygame_sdl2.controller import get_string_for_axis as pref_controls_axis_name
        from pygame_sdl2.controller import get_string_for_button as pref_controls_button_name
    except Exception:
        import pygame as pref_controls_pygame

        def pref_controls_axis_name(axis):
            return str(axis)

        def pref_controls_button_name(button):
            return str(button)

    from renpy.store import Null, config, pad_config, persistent

    PREF_CONTROLS_LAYOUT_ORDER = [
        ("playstation", "PLAYSTATION"),
        ("xbox", "XBOX"),
        ("nintendo", "NINTENDO"),
        ("steam", "STEAM"),
        ("generic", "GENERIC"),
    ]

    PREF_CONTROLS_KEYBOARD_ACTIONS = [
        ("Advance Dialogue", "dismiss", ("Enter", "Space")),
        ("Open Menu", "game_menu", ("Esc", "M")),
        ("Skip", "skip", ("Left Ctrl", "Right Ctrl")),
        ("Rollback", "rollback", ("Page Up", "-")),
        ("Hide UI", "hide_windows", ("H", "-")),
        ("Quick Save", "quick_save", ("F5", "-")),
        ("Quick Load", "quick_load", ("F9", "-")),
    ]

    PREF_CONTROLS_MOUSE_ACTIONS = [
        ("Advance", "dismiss", ("Left Click", "-")),
        ("Open Menu", "game_menu", ("Right Click", "-")),
        ("Scroll Back", "rollback", ("Mouse Wheel Up", "-")),
        ("Wheel Down", "toggle_afm", ("Mouse Wheel Down", "-")),
    ]

    PREF_CONTROLS_NAVIGATION_ACTIONS = [
        ("Move Left", "focus_left", ("Left Arrow", "A")),
        ("Move Right", "focus_right", ("Right Arrow", "D")),
        ("Move Up", "focus_up", ("Up Arrow", "W")),
        ("Move Down", "focus_down", ("Down Arrow", "S")),
        ("Confirm / Select", "dismiss", ("Enter", "Space")),
        ("Back / Cancel", "game_menu", ("Esc", "Backspace")),
    ]

    PREF_CONTROLS_BINDING_FILTERS = [
        ("all", "ALL"),
        ("dialogue", "DIALOGUE"),
        ("menus", "MENUS"),
        ("system", "SYSTEM"),
    ]

    PREF_CONTROLS_BINDING_CATEGORY_MAP = {
        "button_select": "dialogue",
        "dismiss": "dialogue",
        "toggle_afm": "dialogue",
        "toggle_skip": "dialogue",
        "rollback": "dialogue",
        "rollforward": "dialogue",
        "game_menu": "menus",
        "hide_windows": "system",
        "screenshot": "system",
        "save_delete": "system",
        "fast_skip": "system",
    }

    def pref_controls_layout_label(layout=None):
        current = str(layout or getattr(persistent, "controller_layout", "generic") or "generic").lower()
        return {
            "playstation": "PlayStation",
            "xbox": "Xbox",
            "nintendo": "Nintendo",
            "steam": "Steam",
            "generic": "Generic",
        }.get(current, current.replace("_", " ").title())

    def pref_controls_controller_count():
        try:
            return len(getattr(renpy.store, "renpy_controllers", {}) or {})
        except Exception:
            return 0

    def pref_controls_has_gamepad():
        return pref_controls_controller_count() > 0

    def _pref_controls_refresh_layout_redraw():
        try:
            pad_config.refresh_redrawables(0, 1, None, force=True)
        except Exception:
            pass

    def pref_controls_ensure_toggle_defaults():
        changed = False

        if not hasattr(persistent, "controller_vibration_enabled"):
            persistent.controller_vibration_enabled = True
            changed = True

        if not hasattr(persistent, "controller_trigger_effects_enabled"):
            persistent.controller_trigger_effects_enabled = True
            changed = True

        if changed:
            try:
                renpy.save_persistent()
            except Exception:
                pass

    def _pref_controls_save_and_refresh():
        try:
            renpy.save_persistent()
        except Exception:
            pass
        renpy.restart_interaction()

    def pref_controls_set_layout(layout):
        layout = str(layout or "generic").lower()
        if not hasattr(persistent, "controller_guid_to_type") or persistent.controller_guid_to_type is None:
            persistent.controller_guid_to_type = {}

        persistent.controller_layout = layout

        try:
            for controller in (getattr(renpy.store, "renpy_controllers", {}) or {}).values():
                guid = controller.get_guid_string()
                persistent.controller_guid_to_type[guid] = layout
        except Exception:
            pass

        _pref_controls_refresh_layout_redraw()
        _pref_controls_save_and_refresh()

    def pref_controls_cycle_layout(reverse=False):
        order = [name for name, _label in PREF_CONTROLS_LAYOUT_ORDER]
        current = str(getattr(persistent, "controller_layout", "generic") or "generic").lower()
        if current not in order:
            current = "generic"
        index = order.index(current)
        if reverse:
            index -= 1
        else:
            index += 1
        pref_controls_set_layout(order[index % len(order)])

    def pref_controls_deadzone_ratio(stick="left"):
        try:
            current = float(pad_config.get_stick_dead_zone(stick=stick))
            maximum = float(pad_config.get_stick_max(stick=stick))
        except Exception:
            current = float(getattr(pad_config, "DEFAULT_DEADZONE", 4096))
            maximum = float(getattr(pad_config, "STICK_MAX", 32767))

        if maximum <= 0.0:
            return 0.0

        return max(0.0, min(1.0, current / maximum))

    def pref_controls_deadzone_percent(stick="left"):
        return _pref_percent_text(pref_controls_deadzone_ratio(stick), step=0.01)

    def pref_controls_sensitivity_ratio(stick="left"):
        current = float(getattr(persistent, stick + "_stick_sensitivity", getattr(pad_config, "DEFAULT_SENSITIVITY", 1.0)))
        minimum = float(getattr(pad_config, "MINIMUM_SENSITIVITY", 0.2))
        default = float(getattr(pad_config, "DEFAULT_SENSITIVITY", 1.0))
        maximum = float(getattr(pad_config, "MAXIMUM_SENSITIVITY", 3.0))

        if maximum <= minimum:
            return 0.5

        if current <= default:
            span = max(0.0001, default - minimum)
            ratio = 0.5 * ((current - minimum) / span)
        else:
            span = max(0.0001, maximum - default)
            ratio = 0.5 + (0.5 * ((current - default) / span))

        return max(0.0, min(1.0, ratio))

    def pref_controls_sensitivity_percent(stick="left"):
        return _pref_percent_text(pref_controls_sensitivity_ratio(stick), step=0.01)

    def pref_controls_sensitivity_label(value=None):
        default = float(getattr(pad_config, "DEFAULT_SENSITIVITY", 1.0))
        current = float(default if value is None else value)
        if current < (default - 0.12):
            return "Low"
        if current > (default + 0.12):
            return "High"
        return "Normal"

    def pref_controls_sensitivity_summary():
        left = float(getattr(persistent, "left_stick_sensitivity", getattr(pad_config, "DEFAULT_SENSITIVITY", 1.0)))
        right = float(getattr(persistent, "right_stick_sensitivity", getattr(pad_config, "DEFAULT_SENSITIVITY", 1.0)))
        if abs(left - right) > 0.25:
            return "Mixed"
        return pref_controls_sensitivity_label((left + right) / 2.0)

    def pref_controls_metric_text(value, metric, stick=None):
        try:
            adjustment = getattr(value, "_adjustment", None)
            if adjustment is None:
                adjustment = value.get_adjustment()
            current = float(getattr(adjustment, "value", 0.0))
        except Exception:
            adjustment = None
            current = 0.0

        if metric == "deadzone":
            minimum = float(getattr(pad_config, "MINIMUM_DEADZONE", 1024))
            maximum = float(getattr(pad_config, "STICK_MAX", 32767))
            ratio = ((current + minimum) / maximum) if maximum > 0.0 else 0.0
            return _pref_percent_text(max(0.0, min(1.0, ratio)), step=0.01)

        if metric == "sensitivity":
            ratio = current / 10.0
            return _pref_percent_text(max(0.0, min(1.0, ratio)), step=0.01)

        if stick is not None:
            return pref_controls_deadzone_percent(stick)

        return "0%"

    def pref_controls_live_metric_dd(st, at, value, metric, stick=None, style="pref_label_text", color=None):
        kwargs = {}
        if style:
            kwargs["style"] = style
        if color:
            kwargs["color"] = color
        return Text(pref_controls_metric_text(value, metric, stick=stick), **kwargs), 0.05

    def pref_controls_live_metric_displayable(value, metric, stick=None, style="pref_label_text", color=None):
        return DynamicDisplayable(pref_controls_live_metric_dd, value, metric, stick, style, color)

    def pref_controls_normalize_key_label(label):
        if isinstance(label, bytes):
            try:
                label = label.decode("utf-8")
            except Exception:
                label = str(label)
        else:
            label = str(label or "")

        stripped = label.strip()
        if (len(stripped) >= 3) and (stripped[0:2].lower() == "b'") and stripped.endswith("'"):
            stripped = stripped[2:-1]
        elif (len(stripped) >= 4) and (stripped[0:2].lower() == 'b"') and stripped.endswith('"'):
            stripped = stripped[2:-1]

        normalized = stripped.replace("_", " ").replace("-", " ").strip().lower()
        mapping = {
            "return": "Enter",
            "kp enter": "Num Enter",
            "escape": "Esc",
            "space": "Space",
            "backspace": "Backspace",
            "tab": "Tab",
            "capslock": "Caps Lock",
            "pageup": "Page Up",
            "pagedown": "Page Down",
            "backquote": "`",
            "left ctrl": "Ctrl",
            "right ctrl": "Ctrl",
            "left shift": "Shift",
            "right shift": "Shift",
            "left alt": "Alt",
            "right alt": "Alt",
            "left super": "Super",
            "right super": "Super",
            "menu": "Menu",
            "left": "Left Arrow",
            "right": "Right Arrow",
            "up": "Up Arrow",
            "down": "Down Arrow",
            "wheelup": "Mouse Wheel Up",
            "wheeldown": "Mouse Wheel Down",
        }
        return mapping.get(normalized, normalized.title())

    def pref_controls_key_name(code):
        code = str(code or "")
        constant = getattr(pref_controls_pygame, "K_" + code, None)
        if constant is not None:
            try:
                label = pref_controls_pygame.key.name(constant)
            except Exception:
                label = code
        else:
            label = code
        return pref_controls_normalize_key_label(label).upper()

    def pref_controls_key_event_label(key, mod=0):
        try:
            base = pref_controls_pygame.key.name(key)
        except Exception:
            base = str(key)

        key_label = pref_controls_normalize_key_label(base).upper()
        modifiers = []

        if (mod & getattr(pref_controls_pygame, "KMOD_CTRL", 0)) and key_label != "CTRL":
            modifiers.append("CTRL")
        if (mod & getattr(pref_controls_pygame, "KMOD_ALT", 0)) and key_label != "ALT":
            modifiers.append("ALT")
        if (mod & getattr(pref_controls_pygame, "KMOD_SHIFT", 0)) and key_label != "SHIFT":
            modifiers.append("SHIFT")

        if modifiers:
            return " + ".join(modifiers + [key_label])
        return key_label

    def pref_controls_mouse_label(button):
        mapping = {
            "1": "LEFT CLICK",
            "2": "MIDDLE CLICK",
            "3": "RIGHT CLICK",
            "4": "WHEEL UP",
            "5": "WHEEL DOWN",
            "6": "MOUSE 6",
            "7": "MOUSE 7",
        }
        return mapping.get(str(button), "MOUSE " + str(button))

    def pref_controls_token_text(token):
        if token is None:
            return ""
        if isinstance(token, bytes):
            try:
                return token.decode("utf-8")
            except Exception:
                try:
                    return token.decode("latin-1")
                except Exception:
                    return ""
        token = str(token)
        stripped = token.strip()
        if (len(stripped) >= 3) and (stripped[0:2].lower() == "b'") and stripped.endswith("'"):
            return stripped[2:-1]
        if (len(stripped) >= 4) and (stripped[0:2].lower() == 'b"') and stripped.endswith('"'):
            return stripped[2:-1]
        return token

    def pref_controls_token_label(token):
        token = pref_controls_token_text(token)
        if (not token) or token.startswith("pad_") or token.startswith("repeat_pad_"):
            return None

        if token.startswith("mouseup_") or token.startswith("mousedown_"):
            return pref_controls_mouse_label(token.split("_", 1)[1]).upper()

        parts = token.split("_")
        modifiers = []
        key_code = None
        index = 0

        while index < len(parts):
            part = parts[index]

            if part in ("keydown", "keyup", "repeat", "anyrepeat", "noshift"):
                index += 1
                continue

            if part in ("alt", "ctrl", "shift", "meta", "command", "oscmd"):
                modifiers.append({
                    "alt": "ALT",
                    "ctrl": "CTRL",
                    "shift": "SHIFT",
                    "meta": "META",
                    "command": "CMD",
                    "oscmd": "CMD",
                }[part])
                index += 1
                continue

            if part == "K":
                key_code = "_".join(parts[index + 1:])
                break

            if part.startswith("K"):
                key_code = part[2:] if part.startswith("K_") else part[1:]
                tail = "_".join(parts[index + 1:])
                if tail:
                    key_code = (key_code + "_" + tail) if key_code else tail
                break

            index += 1

        if key_code is None:
            cleaned = token.replace("_", " ").strip()
            return cleaned.upper() if cleaned else None

        key_label = pref_controls_key_name(key_code)
        if modifiers:
            return " + ".join(modifiers + [key_label])
        return key_label

    def pref_controls_labels_for(action, device="keyboard", limit=2):
        labels = []

        try:
            bindings = list(config.keymap.get(action, []))
        except Exception:
            bindings = []

        for binding in bindings:
            token = pref_controls_token_text(binding)
            is_mouse = token.startswith("mouseup_") or token.startswith("mousedown_")

            if device == "keyboard" and is_mouse:
                continue
            if device == "mouse" and not is_mouse:
                continue

            label = pref_controls_token_label(token)
            if (not label) or (label in labels):
                continue

            labels.append(label)
            if len(labels) >= limit:
                break

        return labels

    def _pref_controls_rows(specs, device="keyboard"):
        rows = []
        for title, action, fallback in specs:
            rows.append((title, fallback[0], fallback[1]))
        return rows

    def pref_controls_keyboard_rows():
        return _pref_controls_rows(PREF_CONTROLS_KEYBOARD_ACTIONS, device="keyboard")

    def pref_controls_mouse_rows():
        return _pref_controls_rows(PREF_CONTROLS_MOUSE_ACTIONS, device="mouse")

    def pref_controls_navigation_rows():
        return _pref_controls_rows(PREF_CONTROLS_NAVIGATION_ACTIONS, device="keyboard")

    def pref_controls_icon_for_button(button_name):
        return {
            "a": "pad_a",
            "b": "pad_b",
            "x": "pad_x",
            "y": "pad_y",
            "back": "pad_select",
            "start": "pad_start",
            "guide": "pad_home",
            "leftshoulder": "pad_l1",
            "rightshoulder": "pad_r1",
            "lefttrigger": "pad_l2",
            "righttrigger": "pad_r2",
            "leftstick": "pad_l3",
            "rightstick": "pad_r3",
            "dpup": "pad_up",
            "dpdown": "pad_down",
            "dpleft": "pad_left",
            "dpright": "pad_right",
        }.get(str(button_name or "").lower())

    def pref_controls_label_for_button(button_name):
        icon_name = pref_controls_icon_for_button(button_name)
        if icon_name:
            try:
                return pad_config.get_alt_text([icon_name.replace("pad_", "")], as_list=False, is_event=False, alt_tag=False).upper()
            except Exception:
                pass
        return str(button_name or "button").replace("_", " ").upper()

    def pref_controls_restore_bindings(remapper=None):
        try:
            pad_remap.reset_to_default(remapper)
        except Exception:
            pass
        _pref_controls_save_and_refresh()

    def _pref_controls_reset_tuning_state():
        pref_controls_ensure_toggle_defaults()

        for field, value in (
            ("hold_to_skip", False),
            ("controller_vibration_enabled", True),
            ("controller_trigger_effects_enabled", True),
            ("left_stick_invert_x", False),
            ("left_stick_invert_y", False),
            ("right_stick_invert_x", False),
            ("right_stick_invert_y", False),
            ("left_stick_sensitivity", getattr(pad_config, "DEFAULT_SENSITIVITY", 1.0)),
            ("right_stick_sensitivity", getattr(pad_config, "DEFAULT_SENSITIVITY", 1.0)),
            ("left_stick_dead_zone_fallback", getattr(pad_config, "DEFAULT_DEADZONE", 4096)),
            ("right_stick_dead_zone_fallback", getattr(pad_config, "DEFAULT_DEADZONE", 4096)),
        ):
            setattr(persistent, field, value)

        for field in (
            "left_stick_dead_zone",
            "right_stick_dead_zone",
            "left_stick_max",
            "right_stick_max",
        ):
            setattr(persistent, field, {})

    def pref_controls_restore_tuning():
        _pref_controls_reset_tuning_state()
        _pref_controls_save_and_refresh()

    def pref_controls_restore_layout():
        persistent.controller_layout = "generic"
        persistent.controller_guid_to_type = {}
        _pref_controls_refresh_layout_redraw()
        _pref_controls_save_and_refresh()

    def pref_controls_restore_all(remapper=None):
        _pref_controls_reset_tuning_state()
        persistent.controller_layout = "generic"
        persistent.controller_guid_to_type = {}
        try:
            pad_remap.reset_to_default(remapper)
        except Exception:
            pass
        _pref_controls_refresh_layout_redraw()
        _pref_controls_save_and_refresh()

    def pref_controls_binding_category_for(action):
        return PREF_CONTROLS_BINDING_CATEGORY_MAP.get(str(action or ""), "system")

    def pref_controls_filter_remap_rows(remap_rows, category="all", search_text=""):
        category = str(category or "all").lower()
        query = str(search_text or "").strip().lower()
        rows = []

        for title, act, act_id, pad_images in remap_rows:
            if category != "all" and pref_controls_binding_category_for(act) != category:
                continue
            if query and query not in str(title or "").lower() and query not in str(act or "").lower():
                continue
            rows.append((title, act, act_id, pad_images))

        return rows

    def pref_controls_action_keysyms(action):
        try:
            bindings = list((persistent.pad_bindings or {}).get(action, []))
        except Exception:
            bindings = []

        keysyms = []
        for binding in bindings:
            token = str(binding or "")
            if token.startswith("repeat_"):
                continue
            if token not in keysyms:
                keysyms.append(token)

        return keysyms[:3]

    def pref_controls_binding_display(keysym):
        token = str(keysym or "")
        if not token:
            return (None, "Empty")

        if token.startswith("repeat_"):
            token = token[len("repeat_"):]

        if not token.startswith("pad_"):
            return (None, pref_controls_token_label(token) or token.upper())

        button_name = token[4:]
        for suffix in ("_press", "_release", "_pos", "_neg", "_zero"):
            if button_name.endswith(suffix):
                button_name = button_name[:-len(suffix)]
                break

        return (
            pref_controls_icon_for_button(button_name),
            pref_controls_label_for_button(button_name),
        )

    def pref_controls_selected_title(remap_rows, action):
        if not action:
            return ""

        for title, act, _act_id, _pad_images in remap_rows:
            if act == action:
                return title

        return str(action).replace("_", " ").title()

    def pref_controls_action_slot_rows(action):
        keysyms = pref_controls_action_keysyms(action)
        rows = []

        for index in range(3):
            if index < len(keysyms):
                icon_name, label = pref_controls_binding_display(keysyms[index])
                rows.append({
                    "index": index,
                    "keysym": keysyms[index],
                    "icon": icon_name,
                    "label": label,
                    "empty": False,
                })
            else:
                rows.append({
                    "index": index,
                    "keysym": None,
                    "icon": None,
                    "label": "Empty",
                    "empty": True,
                })

        return rows

    def pref_controls_remaps_edited_count():
        count = 0

        try:
            remappable_actions = [act for _title, act, _priority in pad_remap.REMAPPABLE_EVENTS]
        except Exception:
            remappable_actions = []

        for action in remappable_actions:
            current = pref_controls_action_keysyms(action)
            try:
                default_values = [x for x in list(pad_remap.DEFAULT_BINDINGS.get(action, [])) if not str(x or "").startswith("repeat_")]
            except Exception:
                default_values = []

            if current != default_values[:3]:
                count += 1

        return count

    def pref_controls_empty_slots_count():
        total = 0

        try:
            remappable_actions = [act for _title, act, _priority in pad_remap.REMAPPABLE_EVENTS]
        except Exception:
            remappable_actions = []

        for action in remappable_actions:
            total += max(0, 3 - len(pref_controls_action_keysyms(action)))

        return total

    def pref_controls_can_clear_slot(action, slot_index):
        keysyms = pref_controls_action_keysyms(action)

        if slot_index < 0 or slot_index >= len(keysyms):
            return False

        if action in pad_remap.REQUIRED_EVENTS and len(keysyms) <= 1:
            return False

        return True

    def pref_controls_clear_slot(remapper, action, slot_index):
        keysyms = pref_controls_action_keysyms(action)
        if not pref_controls_can_clear_slot(action, slot_index):
            return

        remapper.remove_button(keysyms[slot_index], action)
        _pref_controls_save_and_refresh()

    def pref_controls_restore_action_default(remapper, action):
        defaults = []

        try:
            defaults = [x for x in list(pad_remap.DEFAULT_BINDINGS.get(action, [])) if not str(x or "").startswith("repeat_")]
        except Exception:
            defaults = []

        for keysym in list(pref_controls_action_keysyms(action)):
            remapper.remove_button(keysym, action)

        for keysym in defaults:
            remapper.add_button(keysym, action)

        _pref_controls_save_and_refresh()

    def pref_controls_edit_binding_slot(title, action, slot_index, yadj, remapper):
        before = pref_controls_action_keysyms(action)
        existing = before[slot_index] if 0 <= slot_index < len(before) else None

        renpy.call_in_new_context("listen_for_remap", title, action, yadj, remapper)

        after = pref_controls_action_keysyms(action)
        new_keysyms = [keysym for keysym in after if keysym not in before]

        if existing and new_keysyms and existing in after:
            remapper.remove_button(existing, action)

        _pref_controls_save_and_refresh()

    class PrefControlsInputProbe(Null):
        def __init__(self):
            self.reset()
            super(PrefControlsInputProbe, self).__init__()

        def reset(self):
            self.left_x = 0.0
            self.left_y = 0.0
            self.right_x = 0.0
            self.right_y = 0.0
            self.last_input = "NONE"
            self.last_controller_icon = None

        def current_input_text(self):
            return self.last_input or "NONE"

        def _clamp_axis(self, value):
            return max(-1.0, min(1.0, float(value)))

        def _apply_axis_preview(self, stick, axis, value):
            value = self._clamp_axis(value)

            deadzone = pref_controls_deadzone_ratio(stick)
            if abs(value) <= deadzone:
                value = 0.0
            else:
                remainder = (abs(value) - deadzone) / max(0.0001, 1.0 - deadzone)
                value = math.copysign(remainder, value)

            if getattr(persistent, "{}_stick_invert_{}".format(stick, axis), False):
                value *= -1.0

            sensitivity = float(getattr(persistent, "{}_stick_sensitivity".format(stick), getattr(pad_config, "DEFAULT_SENSITIVITY", 1.0)))
            default = float(getattr(pad_config, "DEFAULT_SENSITIVITY", 1.0)) or 1.0
            value *= (sensitivity / default)

            return self._clamp_axis(value)

        def _set_axis(self, attr, value):
            current = getattr(self, attr, 0.0)
            if abs(current - value) < 0.01:
                return False
            setattr(self, attr, value)
            return True

        def _set_current_input(self, label, icon_name=None):
            label = str(label or "NONE").upper()
            changed = False

            if self.last_input != label:
                self.last_input = label
                changed = True

            if self.last_controller_icon != icon_name:
                self.last_controller_icon = icon_name
                changed = True

            return changed

        def event(self, ev, x, y, st):
            changed = False

            try:
                if ev.type == pref_controls_pygame.CONTROLLERAXISMOTION:
                    axis_name = str(pref_controls_axis_name(ev.axis) or "").lower()
                    raw_value = float(getattr(ev, "value", 0.0)) / float(max(1, getattr(pad_config, "STICK_MAX", 32767)))

                    if axis_name in ("leftx", "lefty", "rightx", "righty"):
                        stick = "left" if axis_name.startswith("left") else "right"
                        axis = "x" if axis_name.endswith("x") else "y"
                        preview = self._apply_axis_preview(stick, axis, raw_value)
                        changed = self._set_axis(stick + "_" + axis, preview) or changed

                    elif axis_name in ("lefttrigger", "triggerleft"):
                        if abs(raw_value) > 0.1:
                            changed = self._set_current_input(pref_controls_label_for_button("lefttrigger"), "pad_l2") or changed

                    elif axis_name in ("righttrigger", "triggerright"):
                        if abs(raw_value) > 0.1:
                            changed = self._set_current_input(pref_controls_label_for_button("righttrigger"), "pad_r2") or changed

                elif ev.type == pref_controls_pygame.CONTROLLERBUTTONDOWN:
                    button_name = str(pref_controls_button_name(ev.button) or ev.button).lower()
                    changed = self._set_current_input(
                        pref_controls_label_for_button(button_name),
                        pref_controls_icon_for_button(button_name),
                    ) or changed

                elif ev.type == pref_controls_pygame.KEYDOWN:
                    changed = self._set_current_input(pref_controls_key_event_label(ev.key, getattr(ev, "mod", 0))) or changed

                elif ev.type == pref_controls_pygame.MOUSEBUTTONDOWN:
                    changed = self._set_current_input(pref_controls_mouse_label(getattr(ev, "button", 0))) or changed
            except Exception:
                return None

            if changed:
                renpy.restart_interaction()

            return None


style pref_controls_chip_text is pref_setting_btn_text:
    size 15
    color "#eef2ff"
    selected_color "#1b2431"

style pref_controls_tab_text is pref_setting_btn_text:
    size 17

style pref_controls_slot_header is pref_label_text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 16
    text_align 0.5
    color "#d9c9f3"

style pref_controls_section_label is pref_label_text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 18
    color "#dbc3ff"

style pref_controls_search_text is input:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 18
    color "#eef2ff"
    selected_color "#eef2ff"
    selected_idle_color "#eef2ff"
    selected_hover_color "#eef2ff"
    hover_color "#eef2ff"

style pref_controls_help_text is pref_label_text:
    size 15
    color "#d8dff0"


screen pref_controls_button(label, action, tab_colors, selected=False, button_id=None, xsize=180, ysize=44, text_style="pref_setting_btn_text"):
    use pref_small_button(label, action, selected=selected, text_style=text_style, button_id=button_id, xsize=xsize, ysize=ysize, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])


screen pref_controls_tab_button(label, section, current_section, tab_colors, button_id=None, xsize=152):
    use pref_controls_button(label, SetVariable("pref_controls_section_tab", section), tab_colors, selected=(current_section == section), button_id=button_id, xsize=xsize, ysize=42, text_style="pref_controls_tab_text")


screen pref_controls_text_chip(text_value, tab_colors, xsize=160, ysize=44, selected=False, text_style="pref_controls_chip_text"):
    $ chip_background = pref_button_surface(xsize, ysize, tab_colors["accent"], tab_colors["selected_bg"], selected=selected)
    $ chip_text_color = tab_colors["selected_text"] if selected else pref_ui_text_color("button")
    fixed:
        xsize xsize
        ysize ysize
        add chip_background
        text (text_value or "--") style text_style color chip_text_color xsize (xsize - 16) xalign 0.5 yalign 0.5 text_align 0.5


screen pref_controls_toggle_row(label, on_action, off_action, on_selected, tab_colors, on_id=None, label_width=250, button_width=150):
    hbox:
        spacing 12
        fixed:
            xsize label_width
            ysize 48
            text label style "pref_setting_label" yalign 0.5
        use pref_controls_button("ON", on_action, tab_colors, selected=on_selected, button_id=on_id, xsize=button_width, ysize=44)
        use pref_controls_button("OFF", off_action, tab_colors, selected=(not on_selected), xsize=button_width, ysize=44)


screen pref_controls_dual_toggle_row(label, selected_value, left_label, right_label, left_action, right_action, tab_colors, label_width=250, button_width=112, row_height=42):
    hbox:
        spacing 12

        fixed:
            xsize label_width
            ysize row_height
            text label style "pref_setting_label" yalign 0.5

        use pref_controls_button(left_label, left_action, tab_colors, selected=(selected_value == "left"), xsize=button_width, ysize=38)
        use pref_controls_button(right_label, right_action, tab_colors, selected=(selected_value == "right"), xsize=button_width, ysize=38)


screen pref_controls_status_row(icon_name, label, value_text, tab_colors):
    hbox:
        spacing 12

        fixed:
            xsize 28
            ysize 28
            if icon_name:
                add Transform(icon_name, fit="contain", xsize=22, ysize=22, xalign=0.5, yalign=0.5)

        fixed:
            xsize 258
            ysize 30
            text (label + ":") style "pref_setting_label" yalign 0.5

        fixed:
            xsize 210
            ysize 30
            text value_text style "pref_label_text" color pref_ui_text_color("percent", tab_colors["accent"]) yalign 0.5


screen pref_controls_status_chip_row(label, value_text, tab_colors, label_width=250, chip_width=170):
    hbox:
        spacing 14

        fixed:
            xsize label_width
            ysize 42
            text label style "pref_setting_label" yalign 0.5

        use pref_controls_text_chip((value_text or "--").upper(), tab_colors, xsize=chip_width, ysize=40, selected=True)


screen pref_controls_axis_row(label, stick, axis, normal_selected, tab_colors, normal_id=None, label_width=250, button_width=150):
    hbox:
        spacing 12
        fixed:
            xsize label_width
            ysize 48
            text label style "pref_setting_label" yalign 0.5
        use pref_controls_button("NORMAL", SetStickInversion(stick, axis, False), tab_colors, selected=normal_selected, button_id=normal_id, xsize=button_width, ysize=44)
        use pref_controls_button("INVERTED", SetStickInversion(stick, axis, True), tab_colors, selected=(not normal_selected), xsize=button_width, ysize=44)


screen pref_controls_slider_row(label, stick, metric, value, tab_colors, button_id=None, label_width=250, slider_width=280, metric_width=72):
    $ metric_color = pref_ui_text_color("percent", tab_colors["accent"])
    $ low_label = "MIN" if metric == "deadzone" else "LOW"
    $ high_label = "MAX" if metric == "deadzone" else "HIGH"

    hbox:
        spacing 12

        fixed:
            xsize label_width
            ysize 64
            text label style "pref_setting_label" yalign 0.5

        fixed:
            xsize 42
            ysize 64
            text low_label style "pref_label_text" xalign 1.0 yalign 0.5

        fixed:
            xsize slider_width
            ysize 64
            use ui_slider(value, style_name="pref_bar", xpos=0, ypos=16, xsize=slider_width, ysize=32, button_id=button_id)

        fixed:
            xsize 42
            ysize 64
            text high_label style "pref_label_text" xalign 0.0 yalign 0.5

        fixed:
            xsize metric_width
            ysize 64
            add pref_controls_live_metric_displayable(value, metric, stick=stick, style="pref_label_text", color=metric_color) xalign 1.0 yalign 0.5


screen pref_controls_reference_rows(rows, tab_colors, label_width=250, primary_width=170, secondary_width=170, primary_header="PRIMARY", secondary_header="ALT", action_header=None, show_headers=True, row_height=48, chip_height=44, row_spacing=10):
    vbox:
        spacing row_spacing

        if show_headers and rows:
            hbox:
                spacing 12
                fixed:
                    xsize label_width
                    ysize 24
                    if action_header:
                        text action_header style "pref_controls_slot_header" xalign 0.0 yalign 0.5
                    else:
                        null
                fixed:
                    xsize primary_width
                    ysize 24
                    text primary_header style "pref_controls_slot_header" xalign 0.5 yalign 0.5
                fixed:
                    xsize secondary_width
                    ysize 24
                    text secondary_header style "pref_controls_slot_header" xalign 0.5 yalign 0.5

        if rows:
            for title, primary, secondary in rows:
                hbox:
                    spacing 12
                    fixed:
                        xsize label_width
                        ysize row_height
                        text title style "pref_setting_label" yalign 0.5
                    use pref_controls_text_chip(primary, tab_colors, xsize=primary_width, ysize=chip_height)
                    use pref_controls_text_chip(secondary, tab_colors, xsize=secondary_width, ysize=chip_height)
        else:
            text "No bindings were found for this section." style "pref_label_text"


screen pref_controls_binding_filter_button(label, category, current_category, tab_colors, xsize=114):
    use pref_controls_button(label, SetVariable("pref_controls_binding_category", category), tab_colors, selected=(current_category == category), xsize=xsize, ysize=40, text_style="pref_controls_tab_text")


screen pref_controls_binding_slot_cell(icon_name, label_text, slot_action, tab_colors, selected=False, empty=False, xsize=158, ysize=54):
    $ button_bg = pref_button_surface(xsize, ysize, tab_colors["accent"], tab_colors["selected_bg"], selected=selected)

    button:
        style "pref_choice_button"
        background button_bg
        hover_background pref_button_surface(xsize, ysize, tab_colors["accent"], tab_colors["selected_bg"], selected=selected, hovered=True)
        selected_background button_bg
        selected_hover_background button_bg
        xsize xsize
        ysize ysize
        action slot_action

        fixed:
            xsize xsize
            ysize ysize

            if icon_name:
                add Transform(icon_name, fit="contain", xsize=38, ysize=38, xalign=0.5, yalign=0.5, xpos=58, ypos=14)
            elif empty:
                text "-" style "pref_setting_btn_text" xsize xsize text_align 0.5 xpos 58 ypos 30
            else:
                text label_text style "pref_setting_btn_text" xsize xsize text_align 0.5 xpos 58 ypos 30


screen pref_controls_remaps_panel(pref_remapper, pref_yadj, remap_rows, tab_colors, selected_action, selected_slot):
    $ current_category = str(pref_controls_binding_category or "all").lower()

    use pref_hub_panel("REMAPS", "Map controller actions and review existing bindings.", 845, 682, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
        vbox:
            spacing 14

            hbox:
                spacing 12
                fixed:
                    xsize 458
                    ysize 40

                    hbox:
                        spacing 8
                        for category, category_label in PREF_CONTROLS_BINDING_FILTERS:
                            use pref_controls_binding_filter_button(category_label, category, current_category, tab_colors, xsize=(90 if category != "dialogue" else 120))

                fixed:
                    xsize 315
                    ysize 40

                    add pref_button_surface(315, 40, tab_colors["accent"], tab_colors["selected_bg"])

                    hbox:
                        xpos 14
                        ypos 6
                        spacing 10

                        text "SEARCH" style "pref_label_text" color tab_colors["accent"] yalign 0.5

                        input:
                            value VariableInputValue("pref_controls_binding_search")
                            length 28
                            style "pref_controls_search_text"
                            xsize 220

            side "c r":
                xsize 809
                ysize 496

                viewport:
                    id "pref_controls_bindings_viewport"
                    xsize 776
                    yadjustment pref_yadj
                    mousewheel True
                    draggable True
                    has vbox
                    spacing 10

                    hbox:
                        spacing 12
                        fixed:
                            xsize 236
                            ysize 32
                            text "ACTION" style "pref_controls_slot_header" xalign 0.0 yalign 0.5
                        fixed:
                            xsize 158
                            ysize 32
                            text "PRIMARY" style "pref_controls_slot_header" xalign 0.5 yalign 0.5
                        fixed:
                            xsize 158
                            ysize 32
                            text "ALT 1" style "pref_controls_slot_header" xalign 0.5 yalign 0.5
                        fixed:
                            xsize 158
                            ysize 32
                            text "ALT 2" style "pref_controls_slot_header" xalign 0.5 yalign 0.5

                    if remap_rows:
                        for title, act, act_id, pad_images in remap_rows:
                            $ slot_rows = pref_controls_action_slot_rows(act)
                            $ row_selected = (selected_action == act)

                            fixed:
                                xsize 760
                                ysize 60

                                add pref_button_surface(760, 60, tab_colors["accent"], tab_colors["selected_bg"], selected=row_selected)

                                hbox:
                                    xpos 12
                                    ypos 0
                                    spacing 12

                                    fixed:
                                        xsize 236
                                        ysize 54
                                        text title style "pref_setting_label" yalign 0.5

                                    for slot_data in slot_rows:
                                        use pref_controls_binding_slot_cell(
                                            slot_data["icon"],
                                            slot_data["label"],
                                            [
                                                SetVariable("pref_controls_selected_action", act),
                                                SetVariable("pref_controls_selected_slot", slot_data["index"]),
                                            ],
                                            tab_colors,
                                            selected=(row_selected and selected_slot == slot_data["index"]),
                                            empty=slot_data["empty"],
                                            xsize=158,
                                            ysize=54,
                                        )
                    else:
                        frame:
                            background Null()
                            xfill True
                            ypadding 20
                            text "No actions match the current filter." style "pref_label_text" xalign 0.5

                use ui_vscrollbar_for("pref_controls_bindings_viewport")

            text "Select a slot on the table, then use the details panel to edit it." style "pref_label_text"


screen pref_controls_binding_details_panel(pref_remapper, pref_yadj, remap_rows, selected_action, selected_slot, selected_title, tab_colors):
    $ slot_rows = pref_controls_action_slot_rows(selected_action) if selected_action else []
    $ chosen_slot = slot_rows[selected_slot] if slot_rows and 0 <= selected_slot < len(slot_rows) else None
    $ clear_allowed = pref_controls_can_clear_slot(selected_action, selected_slot) if selected_action is not None else False
    $ button_action = NullAction() if not selected_action else Function(pref_controls_edit_binding_slot, selected_title, selected_action, selected_slot, pref_yadj, pref_remapper)
    $ clear_action = NullAction() if not clear_allowed else Function(pref_controls_clear_slot, pref_remapper, selected_action, selected_slot)
    $ restore_action = NullAction() if not selected_action else Function(pref_controls_restore_action_default, pref_remapper, selected_action)

    use pref_hub_panel("BINDING DETAILS", "Edit the selected action without leaving the remap table.", 587, 418, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
        vbox:
            spacing 14

            hbox:
                spacing 10
                text "SELECTED ACTION:" style "pref_setting_label"
                text (selected_title if selected_title else "None") style "pref_section_title" size 18 color pref_ui_text_color("percent", tab_colors["accent"])

            add Solid(tab_colors["accent"] + "44") xsize 551 ysize 1

            for slot_label, slot_index in (("PRIMARY", 0), ("ALT 1", 1), ("ALT 2", 2)):
                $ slot_info = slot_rows[slot_index] if slot_rows else {"icon": None, "label": "Empty", "empty": True}
                $ slot_text_color = pref_ui_text_color("percent", tab_colors["accent"]) if slot_index == selected_slot else pref_ui_text_color("body")
                hbox:
                    spacing 12

                    fixed:
                        xsize 132
                        ysize 34
                        text (slot_label + ":") style "pref_setting_label" yalign 0.5

                    fixed:
                        xsize 38
                        ysize 34
                        if slot_info["icon"]:
                            add Transform(slot_info["icon"], fit="contain", xsize=26, ysize=26, xalign=0.5, yalign=0.5)
                        else:
                            text "-" style "pref_label_text" xalign 0.5 yalign 0.5

                    fixed:
                        xsize 300
                        ysize 34
                        text slot_info["label"] style "pref_label_text" color slot_text_color yalign 0.5

            null height 4

            use pref_controls_button("CHANGE BINDING", button_action, tab_colors, selected=True, xsize=300, ysize=42)
            use pref_controls_button("CLEAR SLOT", clear_action, tab_colors, xsize=300, ysize=42)
            use pref_controls_button("RESTORE DEFAULT", restore_action, tab_colors, xsize=300, ysize=42)

            fixed:
                xsize 551
                ysize 78

                add pref_panel_surface(551, 78, "#10172acc", tab_colors["accent"])

                vbox:
                    xpos 14
                    ypos 12
                    spacing 4
                    text "Select a slot, then press a controller button to assign it." style "pref_controls_help_text"
                    text "Press Escape to cancel." style "pref_controls_help_text"


screen pref_controls_quick_help_panel(tab_colors):
    use pref_hub_panel("QUICK HELP", None, 587, 246, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
        vbox:
            spacing 10

            text "* Primary is the main assigned button." style "pref_controls_help_text"
            text "* Alt slots are optional backup inputs." style "pref_controls_help_text"
            text "* Duplicate bindings may be allowed for some actions." style "pref_controls_help_text"
            text "* Restoring a slot only affects the selected action." style "pref_controls_help_text"

            hbox:
                spacing 8
                text "LEGEND:" style "pref_setting_label"
                add Solid(tab_colors["accent"] + "44") xsize 412 ysize 1 yalign 0.5

            hbox:
                spacing 16

                for icon_name, label in (
                    ("pad_a", "Confirm"),
                    ("pad_b", "Back"),
                    ("pad_x", "Skip"),
                    ("pad_y", "History"),
                    ("pad_start", "Menu"),
                ):
                    hbox:
                        spacing 6
                        add Transform(icon_name, fit="contain", xsize=22, ysize=22) yalign 0.5
                        text label style "pref_controls_help_text" yalign 0.5


screen pref_controls_tuning_panel(tab_colors, tuning_yadj, left_deadzone_value, left_sensitivity_value, right_deadzone_value, right_sensitivity_value, title="CONTROLLER TUNING", subtitle="Tune stick behaviour, inversion, skip handling, and sensitivity.", panel_height=384, viewport_height=274):
    $ tune_content_w = 678
    $ tune_label_w = 228
    $ tune_button_w = 146
    $ tune_slider_w = 236
    $ tune_metric_w = 64

    use pref_hub_panel(title, subtitle, 740, panel_height, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
        side "c r":
            xsize 704
            ysize viewport_height

            viewport:
                id "pref_controls_tuning_viewport"
                xsize tune_content_w
                yadjustment tuning_yadj
                mousewheel True
                draggable True
                has vbox
                spacing 12

                text "SKIP" style "pref_controls_section_label" color tab_colors["accent"]
                add Solid(tab_colors["accent"] + "44") xsize tune_content_w ysize 1
                use pref_controls_toggle_row("HOLD TO SKIP", SetField(persistent, "hold_to_skip", True), SetField(persistent, "hold_to_skip", False), persistent.hold_to_skip, tab_colors, on_id="pref_controls_hold_to_skip_on_btn", label_width=tune_label_w, button_width=tune_button_w)

                text "LEFT STICK" style "pref_controls_section_label" color tab_colors["accent"]
                add Solid(tab_colors["accent"] + "44") xsize tune_content_w ysize 1
                use pref_controls_axis_row("X-AXIS INVERSION", "left", "x", (not persistent.left_stick_invert_x), tab_colors, normal_id="pref_controls_lx_normal_btn", label_width=tune_label_w, button_width=tune_button_w)
                use pref_controls_axis_row("Y-AXIS INVERSION", "left", "y", (not persistent.left_stick_invert_y), tab_colors, normal_id="pref_controls_ly_normal_btn", label_width=tune_label_w, button_width=tune_button_w)
                use pref_controls_slider_row("DEAD ZONE", "left", "deadzone", left_deadzone_value, tab_colors, button_id="pref_controls_l_deadzone_bar", label_width=tune_label_w, slider_width=tune_slider_w, metric_width=tune_metric_w)
                use pref_controls_slider_row("SENSITIVITY", "left", "sensitivity", left_sensitivity_value, tab_colors, button_id="pref_controls_l_sensitivity_bar", label_width=tune_label_w, slider_width=tune_slider_w, metric_width=tune_metric_w)

                text "RIGHT STICK" style "pref_controls_section_label" color tab_colors["accent"]
                add Solid(tab_colors["accent"] + "44") xsize tune_content_w ysize 1
                use pref_controls_axis_row("X-AXIS INVERSION", "right", "x", (not persistent.right_stick_invert_x), tab_colors, normal_id="pref_controls_rx_normal_btn", label_width=tune_label_w, button_width=tune_button_w)
                use pref_controls_axis_row("Y-AXIS INVERSION", "right", "y", (not persistent.right_stick_invert_y), tab_colors, normal_id="pref_controls_ry_normal_btn", label_width=tune_label_w, button_width=tune_button_w)
                use pref_controls_slider_row("DEAD ZONE", "right", "deadzone", right_deadzone_value, tab_colors, button_id="pref_controls_r_deadzone_bar", label_width=tune_label_w, slider_width=tune_slider_w, metric_width=tune_metric_w)
                use pref_controls_slider_row("SENSITIVITY", "right", "sensitivity", right_sensitivity_value, tab_colors, button_id="pref_controls_r_sensitivity_bar", label_width=tune_label_w, slider_width=tune_slider_w, metric_width=tune_metric_w)

            use ui_vscrollbar_for("pref_controls_tuning_viewport")


screen pref_controls_stick_meter(label, x_value, y_value, tab_colors):
    vbox:
        spacing 8
        xsize 130

        text label style "pref_controls_section_label" size 16 color tab_colors["accent"] xalign 0.5

        fixed:
            xsize 112
            ysize 112
            xalign 0.5

            add pref_button_surface(112, 112, tab_colors["accent"], tab_colors["selected_bg"])
            add Solid(tab_colors["accent"] + "33") xpos 55 ysize 112 xsize 2
            add Solid(tab_colors["accent"] + "33") ypos 55 xsize 112 ysize 2

            add Solid(tab_colors["accent"]) xpos int(52 + (x_value * 38.0)) ypos int(52 - (y_value * 38.0)) xsize 8 ysize 8


screen pref_controls_input_icon(icon_name, selected, tab_colors):
    $ icon_background = pref_button_surface(66, 66, tab_colors["accent"], tab_colors["selected_bg"], selected=selected)
    fixed:
        xsize 66
        ysize 66
        add icon_background
        add Transform(icon_name, fit="contain", xsize=42, ysize=42, xalign=0.5, yalign=0.5)


screen pref_controls_input_test_panel(probe, tab_colors, width=740, height=280, keyboard_only=False):
    $ subtitle = "Press a button, move a stick, or tap a key to preview live input." if not keyboard_only else "Press any key or mouse button to test the current keymap."
    use pref_hub_panel("INPUT TEST", subtitle, width, height, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
        vbox:
            spacing 12

            if not keyboard_only:
                hbox:
                    spacing 18

                    use pref_controls_stick_meter("LEFT STICK", probe.left_x, probe.left_y, tab_colors)

                    vbox:
                        spacing 8
                        xsize 350

                        text "BUTTON PREVIEW" style "pref_controls_section_label" size 16 color tab_colors["accent"] xalign 0.5

                        hbox:
                            xalign 0.5
                            spacing 10

                            for icon_name in ("pad_a", "pad_b", "pad_y", "pad_x"):
                                use pref_controls_input_icon(icon_name, (probe.last_controller_icon == icon_name), tab_colors)

                        text ("Controller detected: " + ("YES" if pref_controls_has_gamepad() else "NO")) style "pref_label_text" xalign 0.5

                    use pref_controls_stick_meter("RIGHT STICK", probe.right_x, probe.right_y, tab_colors)

            hbox:
                spacing 12
                yminimum 48

                text "CURRENT INPUT:" style "pref_setting_label" yalign 0.5

                if (not keyboard_only) and probe.last_controller_icon:
                    add Transform(probe.last_controller_icon, fit="contain", xsize=30, ysize=30) yalign 0.5

                use pref_controls_text_chip(probe.current_input_text(), tab_colors, xsize=(420 if keyboard_only else 470), ysize=44, selected=True)


screen pref_controls_gamepad_setup_panel(tab_colors):
    $ current_layout = str(getattr(persistent, "controller_layout", "generic") or "generic").lower()
    $ controller_detected_label = "Yes" if pref_controls_has_gamepad() else "No"
    $ active_layout_label = pref_controls_layout_label()
    $ sensitivity_label = pref_controls_sensitivity_summary()
    use pref_hub_panel("GAMEPAD SETUP", "Choose the button layout and icon prompts used by the game.", 690, 682, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
        vbox:
            spacing 16

            text "CONTROLLER LAYOUT" style "pref_controls_section_label" color tab_colors["accent"]
            add Solid(tab_colors["accent"] + "44") xsize 654 ysize 1

            hbox:
                spacing 12
                for layout_name, layout_label in PREF_CONTROLS_LAYOUT_ORDER[:3]:
                    use pref_controls_button(layout_label, Function(pref_controls_set_layout, layout_name), tab_colors, selected=(current_layout == layout_name), xsize=198, ysize=46)

            hbox:
                spacing 12
                xpos 92
                for layout_name, layout_label in PREF_CONTROLS_LAYOUT_ORDER[3:]:
                    use pref_controls_button(layout_label, Function(pref_controls_set_layout, layout_name), tab_colors, selected=(current_layout == layout_name), xsize=198, ysize=46)

            text "CALIBRATION" style "pref_controls_section_label" color tab_colors["accent"]
            add Solid(tab_colors["accent"] + "44") xsize 654 ysize 1

            hbox:
                spacing 12
                use pref_controls_button("CALIBRATE BUTTONS", GamepadCalibrate(), tab_colors, xsize=230, ysize=46)
                use pref_controls_button("ICON SET", Function(pref_controls_cycle_layout), tab_colors, xsize=150, ysize=46)

            text "PROFILE STATUS" style "pref_controls_section_label" color tab_colors["accent"]
            add Solid(tab_colors["accent"] + "44") xsize 654 ysize 1

            vbox:
                spacing 8
                use pref_controls_status_row("pad_start", "Controller Detected", controller_detected_label, tab_colors)
                use pref_controls_status_row("pad_home", "Active Layout", active_layout_label, tab_colors)
                use pref_controls_status_row("pad_select", "Sensitivity Profile", sensitivity_label, tab_colors)

            text "Layout buttons change the active prompt set immediately. Tuning stays on the right for direct testing." style "pref_label_text"


screen pref_controls_keyboard_panel(keyboard_rows, keyboard_yadj, tab_colors):
    use pref_hub_panel("KEYBOARD SHORTCUTS", "Review the current keyboard shortcuts used by this build.", 690, 682, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
        side "c r":
            xsize 654
            ysize 560

            viewport:
                id "pref_controls_keyboard_viewport"
                yadjustment keyboard_yadj
                mousewheel True
                draggable True
                has vbox
                spacing 10
                use pref_controls_reference_rows(keyboard_rows, tab_colors, label_width=250, primary_width=170, secondary_width=170, primary_header="PRIMARY", secondary_header="ALT", action_header="ACTION")

            use ui_vscrollbar_for("pref_controls_keyboard_viewport")

        text "Shortcuts are pulled from the active Ren'Py keymap for this build." style "pref_label_text"


screen pref_controls_restore_panel(pref_remapper, tab_colors):
    vbox:
        spacing 18

        hbox:
            spacing 20

            use pref_hub_panel("RESTORE BINDINGS", "Reset controller remaps and icon prompts without touching other preference tabs.", 690, 332, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                vbox:
                    spacing 14
                    hbox:
                        spacing 12
                        use pref_controls_button("RESET BINDINGS", CConfirm("Reset controller bindings to their defaults?", Function(pref_controls_restore_bindings, pref_remapper)), tab_colors, xsize=220, ysize=46)
                        use pref_controls_button("RESET LAYOUT", CConfirm("Reset the controller prompt set to Generic?", Function(pref_controls_restore_layout)), tab_colors, xsize=220, ysize=46)
                    text "Reset Bindings restores the remap table on the Bindings page." style "pref_label_text"
                    text "Reset Layout switches prompt icons back to the Generic set." style "pref_label_text"
                    text "These actions keep stick tuning intact." style "pref_label_text"

            use pref_hub_panel("RESTORE TUNING", "Restore skip handling, inversion, dead zones, and stick sensitivity.", 740, 332, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                vbox:
                    spacing 14
                    hbox:
                        spacing 12
                        use pref_controls_button("RESET TUNING", CConfirm("Reset hold-to-skip, inversion, dead zones, and sensitivity?", Function(pref_controls_restore_tuning)), tab_colors, xsize=220, ysize=46)
                        use pref_controls_button("RESET ALL CONTROLS", CConfirm("Reset bindings, layout, and all controller tuning?", Function(pref_controls_restore_all, pref_remapper)), tab_colors, xsize=250, ysize=46)
                    text "Reset Tuning restores the live controller adjustments shown on the right-side panels." style "pref_label_text"
                    text "Reset All Controls combines bindings, layout, and tuning into one controls-only restore." style "pref_label_text"
                    text "Use the footer Default button below if you want every settings tab reset too." style "pref_label_text"

        use pref_hub_panel("RESTORE OVERVIEW", "Current controls snapshot before resetting.", 1450, 332, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
            hbox:
                spacing 28

                vbox:
                    spacing 10
                    text "CURRENT STATUS" style "pref_controls_section_label" color tab_colors["accent"]
                    hbox:
                        spacing 12
                        fixed:
                            xsize 180
                            ysize 42
                            text "Hold To Skip" style "pref_setting_label" yalign 0.5
                        use pref_controls_text_chip(pref_bool_text(getattr(persistent, "hold_to_skip", False)), tab_colors, xsize=130, ysize=42, selected=True)
                    hbox:
                        spacing 12
                        fixed:
                            xsize 180
                            ysize 42
                            text "Layout" style "pref_setting_label" yalign 0.5
                        use pref_controls_text_chip(pref_controls_layout_label().upper(), tab_colors, xsize=170, ysize=42, selected=True)
                    hbox:
                        spacing 12
                        fixed:
                            xsize 180
                            ysize 42
                            text "Left Y Invert" style "pref_setting_label" yalign 0.5
                        use pref_controls_text_chip(pref_bool_text(getattr(persistent, "left_stick_invert_y", False)), tab_colors, xsize=130, ysize=42, selected=True)
                    hbox:
                        spacing 12
                        fixed:
                            xsize 180
                            ysize 42
                            text "Right Y Invert" style "pref_setting_label" yalign 0.5
                        use pref_controls_text_chip(pref_bool_text(getattr(persistent, "right_stick_invert_y", False)), tab_colors, xsize=130, ysize=42, selected=True)
                    hbox:
                        spacing 12
                        fixed:
                            xsize 180
                            ysize 42
                            text "Sensitivity" style "pref_setting_label" yalign 0.5
                        use pref_controls_text_chip(pref_controls_sensitivity_summary().upper(), tab_colors, xsize=150, ysize=42, selected=True)

                vbox:
                    spacing 10
                    text "WHAT RESETS" style "pref_controls_section_label" color tab_colors["accent"]
                    text "Reset Bindings: Controller remaps only." style "pref_label_text"
                    text "Reset Layout: Prompt icon set and controller prompt mapping." style "pref_label_text"
                    text "Reset Tuning: Hold-to-skip, inversion, dead zone, and sensitivity." style "pref_label_text"
                    text "Reset All Controls: Combines the three controls-specific resets above." style "pref_label_text"

                vbox:
                    spacing 10
                    text "NOTES" style "pref_controls_section_label" color tab_colors["accent"]
                    text "The Bindings and Gamepad tabs share the same live tuning values." style "pref_label_text"
                    text "Keyboard and mouse references read from the current engine keymap." style "pref_label_text"
                    text "Global Display, Audio, Access, and Interface settings are unchanged here." style "pref_label_text"


screen preferences_tab_controls(pref_remapper, pref_yadj, active=True):
    default pref_controls_misc_yadj = ui.adjustment()
    default pref_controls_keyboard_yadj = ui.adjustment()
    default pref_left_deadzone_value = StickDeadzoneAdjustment("left")
    default pref_left_sensitivity_value = StickSensitivityAdjustment("left")
    default pref_right_deadzone_value = StickDeadzoneAdjustment("right")
    default pref_right_sensitivity_value = StickSensitivityAdjustment("right")
    default pref_controls_probe = PrefControlsInputProbe()

    $ pref_controls_ensure_toggle_defaults()
    $ tab_colors = pref_ui_tab_colors("controls")
    $ pref_controls_section = pref_controls_section_tab if pref_controls_section_tab in ("bindings", "gamepad", "keyboard", "restore") else "bindings"
    $ remap_rows = pref_get_controls_remap_rows(pref_remapper)
    $ keyboard_rows = pref_controls_keyboard_rows()
    $ mouse_rows = pref_controls_mouse_rows()
    $ navigation_rows = pref_controls_navigation_rows()
    $ filtered_remap_rows = pref_controls_filter_remap_rows(remap_rows, pref_controls_binding_category, pref_controls_binding_search)
    $ filtered_actions = [act for _title, act, _act_id, _pad_images in filtered_remap_rows]
    $ selected_binding_action = pref_controls_selected_action if pref_controls_selected_action in filtered_actions else (filtered_actions[0] if filtered_actions else None)
    $ selected_binding_slot = max(0, min(2, int(pref_controls_selected_slot or 0)))
    $ selected_binding_title = pref_controls_selected_title(remap_rows, selected_binding_action)

    if active:
        fixed:
            xsize 1450
            ysize 740

            add pref_controls_probe

            vbox:
                spacing 16

                hbox:
                    spacing 12
                    xpos 10
                    use pref_controls_tab_button("BINDINGS", "bindings", pref_controls_section, tab_colors, button_id="pref_controls_bindings_tab")
                    use pref_controls_tab_button("GAMEPAD", "gamepad", pref_controls_section, tab_colors)
                    use pref_controls_tab_button("KEYBOARD", "keyboard", pref_controls_section, tab_colors)
                    use pref_controls_tab_button("RESTORE", "restore", pref_controls_section, tab_colors)

                if pref_controls_section == "bindings":
                    hbox:
                        spacing 18
                        use pref_controls_remaps_panel(pref_remapper, pref_yadj, filtered_remap_rows, tab_colors, selected_binding_action, selected_binding_slot)

                        vbox:
                            spacing 18
                            use pref_controls_binding_details_panel(pref_remapper, pref_yadj, remap_rows, selected_binding_action, selected_binding_slot, selected_binding_title, tab_colors)
                            use pref_controls_quick_help_panel(tab_colors)

                elif pref_controls_section == "gamepad":
                    hbox:
                        spacing 20
                        use pref_controls_gamepad_setup_panel(tab_colors)

                        vbox:
                            spacing 18
                            use pref_controls_tuning_panel(tab_colors, pref_controls_misc_yadj, pref_left_deadzone_value, pref_left_sensitivity_value, pref_right_deadzone_value, pref_right_sensitivity_value, title="STICK TUNING", subtitle="Adjust inversion, dead zone, and sensitivity while the prompt set stays visible on the left.")
                            use pref_controls_input_test_panel(pref_controls_probe, tab_colors)

                elif pref_controls_section == "keyboard":
                    hbox:
                        spacing 20
                        use pref_controls_keyboard_panel(keyboard_rows, pref_controls_keyboard_yadj, tab_colors)

                        vbox:
                            spacing 18

                            use pref_hub_panel("MOUSE SHORTCUTS", "Mouse bindings currently exposed by the game keymap.", 740, 250, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                                side "c r":
                                    xsize 704
                                    ysize 170

                                    viewport:
                                        id "pref_controls_mouse_viewport"
                                        mousewheel True
                                        draggable True
                                        has vbox
                                        spacing 8
                                        use pref_controls_reference_rows(mouse_rows, tab_colors, label_width=180, primary_width=150, secondary_width=150, primary_header="PRIMARY", secondary_header="ALT", action_header="ACTION", row_height=34, chip_height=30, row_spacing=6)

                                    use ui_vscrollbar_for("pref_controls_mouse_viewport")

                            use pref_hub_panel("MENU NAVIGATION", "Keyboard navigation actions used by menu focus movement.", 740, 250, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                                side "c r":
                                    xsize 704
                                    ysize 154

                                    viewport:
                                        id "pref_controls_navigation_viewport"
                                        mousewheel True
                                        draggable True
                                        has vbox
                                        spacing 8
                                        use pref_controls_reference_rows(navigation_rows, tab_colors, label_width=180, primary_width=150, secondary_width=150, primary_header="PRIMARY", secondary_header="ALT", action_header="ACTION", row_height=30, chip_height=26, row_spacing=4)

                                    use ui_vscrollbar_for("pref_controls_navigation_viewport")

                            use pref_controls_input_test_panel(pref_controls_probe, tab_colors, width=740, height=146, keyboard_only=True)

                else:
                    use pref_controls_restore_panel(pref_remapper, tab_colors)
