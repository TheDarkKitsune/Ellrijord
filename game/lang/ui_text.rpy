# lang/ui_text.rpy
# Centralized UI strings for menus/tooltips.

init -2 python:
    UI_TEXT = {}

    def register_ui_lang(code, mapping):
        if not isinstance(mapping, dict):
            return
        UI_TEXT[code] = mapping

    if not hasattr(persistent, "ui_lang"):
        persistent.ui_lang = "en_us"

    def get_ui_lang():
        lang = getattr(persistent, "ui_lang", "en_us")
        return lang if lang in UI_TEXT else "en_us"

    def set_ui_lang(lang):
        if lang in UI_TEXT:
            persistent.ui_lang = lang
            renpy.save_persistent()
            renpy.restart_interaction()

    def get_ui_lang_label(code):
        mapping = UI_TEXT.get(code, {})
        return mapping.get("lang_name", code)

    def L(key):
        lang = get_ui_lang()
        return UI_TEXT.get(lang, {}).get(key, UI_TEXT.get("en_us", {}).get(key, key))
