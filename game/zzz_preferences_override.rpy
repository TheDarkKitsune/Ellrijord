# zzz_preferences_override.rpy
# Last-loaded override to prevent pref_tab NameError in legacy screens.

init -999 python:
    if not hasattr(store, "pref_tab"):
        store.pref_tab = "audio"


screen pref_tab_button(label, value, current_tab=None):
    $ _current = current_tab if current_tab is not None else getattr(store, "pref_tab", "audio")
    textbutton label:
        action [SetScreenVariable("pref_tab", value), SetVariable("pref_tab", value)]
        selected (_current == value)
