# 00_pref_tab_guard.rpy
# Ensures pref_tab exists even if legacy screens reference it.

init -999 python:
    if not hasattr(store, "pref_tab"):
        store.pref_tab = "audio"
