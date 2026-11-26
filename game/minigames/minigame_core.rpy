# Shared entry point, presentation and result contract for optional activities.
# Launch with `call ell_minigames` from the normal story context (Day 2+).

default ell_minigame_last_result = None

init -4 python:
    ELL_MINIGAMES = {
        "tsuki_memory": {
            "title": "Tsuki's Memory Challenge",
            "description": "Find the matching pairs in Tsuki's plushie deck.",
            "label": "ellrijord_memory",
            "unlock_day": 2,
        },
    }

    def ell_minigame_available(minigame_id):
        entry = ELL_MINIGAMES.get(minigame_id)
        return bool(entry and ell_day >= entry["unlock_day"])

    def ell_minigame_result(minigame_id, status, **details):
        # Results are save-local data. Future rewards/reactions can consume this
        # after the label returns, without being triggered by screen prediction.
        return dict(details, minigame_id=minigame_id, status=status)


style ell_minigame_text is inv_body_text:
    size 23

style ell_minigame_heading is inv_section_title:
    size 30


screen ell_minigame_shell(title, subtitle):
    add ell_minigame_ui("background")
    frame:
        align (0.5, 0.5)
        xysize (1760, 980)
        padding (34, 26)
        background Frame(ell_minigame_ui("panel"), 36, 36)
        vbox:
            spacing 14
            text title style "ell_minigame_title" size 42 xalign 0.5
            text subtitle style "ell_minigame_body" color "#A58AC5" xalign 0.5
            transclude


screen ell_minigame_controls(exit_action, exit_label="Back"):
    hbox:
        xalign 0.5
        spacing 24
        use ell_minigame_button("Save", ShowMenu("save"), "save", width=220, height=60, button_id="minigame_save")
        use ell_minigame_button("Menu", ShowMenu("showmenu"), "menu", width=220, height=60, button_id="minigame_pause")
        use ell_minigame_button(exit_label, exit_action, "exit", width=340, height=60, button_id="minigame_back")


screen ell_minigames_menu():
    modal True
    zorder 250
    key "game_menu" action Return(None)
    use ell_minigame_shell("Minigames", "Take a break. Return here to replay the available games."):
        fixed:
            xfill True
            ysize 700
            vbox:
                align (0.5, 0.5)
                spacing 24
                for minigame_id, entry in ELL_MINIGAMES.items():
                    text entry["description"] style "ell_minigame_text" xalign 0.5
                    use ell_minigame_button(entry["title"], Return(minigame_id), "play", width=760, height=78, disabled=not ell_minigame_available(minigame_id), button_id="minigame_" + minigame_id)
        use ell_minigame_controls(Return(None))


label ell_minigames(_previous_quick_menu=None):
    if ell_day < 2:
        return
    $ _previous_quick_menu = quick_menu
    $ quick_menu = False
    $ renpy.stop_skipping()
    while True:
        call screen ell_minigames_menu
        if not ell_minigame_available(_return):
            $ quick_menu = _previous_quick_menu
            return
        call expression ELL_MINIGAMES[_return]["label"] from ell_minigames_dispatch
