# Presentation only. Replace the PNG layers or paths here to reskin the game.
# Match rules, timekeeping, results and personal bests live in ellrijord_memory.

init -2 python:
    ELL_MEMORY_TSUKI_ART = "gui/inventory_system/collectibles/tsuki_plushies.png"
    ELL_MEMORY_REACTIONS = {
        "ready": ("Ready? Let's find all their little friends!",),
        "thinking": ("Where was the other one hiding?", "Take your time. I believe in you!"),
        "match": ("A perfect pair! Look at them together.", "One more plushie reunion!", "You remembered! I knew you would."),
        "miss": ("Not quite! Remember where those two are hiding.", "Ooh, close. We'll find their friends next time."),
        "complete": ("All together again! That was lovely. Another round?",),
    }

    def ell_memory_time(seconds):
        seconds = max(0, int(seconds))
        return "{:02d}:{:02d}".format(seconds // 60, seconds % 60)

    def ell_memory_reaction(game):
        choices = ELL_MEMORY_REACTIONS[getattr(game, "reaction", "ready")]
        return choices[game.moves % len(choices)]


transform ell_memory_card_hover:
    subpixel True
    on idle:
        ease 0.16 yoffset 0
    on hover:
        ease 0.16 yoffset -5

transform ell_memory_face_out:
    xalign 0.5
    yalign 0.5
    xzoom 1.0
    easein 0.12 xzoom 0.0
    alpha 0.0

transform ell_memory_face_in:
    xalign 0.5
    yalign 0.5
    alpha 0.0
    xzoom 0.0
    pause 0.12
    alpha 1.0
    easeout 0.14 xzoom 1.0

transform ell_memory_matched_glow:
    alpha 0.5
    ease 1.4 alpha 0.85
    ease 1.4 alpha 0.5
    repeat

transform ell_memory_error_flash:
    alpha 0.9
    ease 0.75 alpha 0.15


screen ell_memory_stat(caption, value, icon):
    frame:
        xysize (374, 78)
        padding (18, 12)
        background Frame(ell_minigame_ui("stat"), 32, 32)
        hbox:
            spacing 16
            add Transform(ell_minigame_ui("icon_" + icon), xysize=(42, 42)) yalign 0.5
            vbox:
                spacing 4
                text caption style "ell_memory_caption" size 14
                text value style "ell_minigame_body" size 23


screen ell_memory_setup(deck_id="tsuki_plushies"):
    modal True
    zorder 250
    key "game_menu" action Return(None)
    use ell_minigame_shell("Tsuki's Memory Challenge", "Classic  |  " + ELL_MEMORY_DECKS[deck_id]["name"]):
        fixed:
            xfill True
            ysize 700
            vbox:
                align (0.5, 0.5)
                spacing 16
                text "Choose your challenge" style "ell_minigame_title" size 30 xalign 0.5
                for difficulty_id, caption, columns, rows in ELL_MEMORY_DIFFICULTIES:
                    $ pairs = columns * rows // 2
                    $ available = ell_memory_can_play(difficulty_id, deck_id)
                    use ell_minigame_button("{}   ·   {} × {}   ·   {} pairs".format(caption, columns, rows, pairs), Return(difficulty_id), icon="moon", width=820, height=70, disabled=not available, button_id="memory_difficulty_" + difficulty_id)
                text "Bigger challenges will open when more plushies arrive." style "ell_minigame_body" size 20 xalign 0.5 color "#A58AC5"
                text "Find each pair. Keep an eye on your moves. Have fun!" style "ell_minigame_body" size 20 xalign 0.5
        use ell_minigame_controls(Return(None))


screen ell_memory_card(deck_id, card_id, revealed, matched, card_width, card_height):
    $ _base = ell_memory_art(deck_id, "front" if revealed else "back")
    $ _illustration = ell_memory_art(deck_id, "illustration", card_id) if revealed else None
    fixed:
        xysize (card_width, card_height)
        if _base:
            add Transform(_base, xysize=(card_width, card_height))
        else:
            add Solid("#FFF1DB" if revealed else "#493459")
        if revealed:
            if _illustration:
                add Transform(_illustration, xysize=(card_width, card_height))
            text ell_memory_card_name(deck_id, card_id):
                style "ell_minigame_body"
                size max(12, int(card_width * 0.12))
                color "#493459"
                xalign 0.5
                ypos int(card_height * 0.865)
                text_align 0.5
                xmaximum int(card_width * 0.83)
        elif not _base:
            add Transform(ell_minigame_ui("icon_moon"), xysize=(card_width // 2, card_width // 2)) align (0.5, 0.5)


screen ell_memory_card_button(game, index, card_id, card_width, card_height):
    $ _revealed = index in game.opened or index in game.matched
    $ _matched = index in game.matched
    $ _turning = index in getattr(game, "turning", ())
    button at ell_memory_card_hover:
        id ("memory_card_" + str(index))
        xysize (card_width, card_height)
        padding (0, 0)
        background None
        hover_background None
        sensitive not game.locked and not _revealed
        action Return(("flip", index))
        fixed:
            xysize (card_width, card_height)
            if _turning:
                fixed at ell_memory_face_out:
                    xysize (card_width, card_height)
                    use ell_memory_card(game.deck_id, card_id, not _revealed, False, card_width, card_height)
                fixed at ell_memory_face_in:
                    xysize (card_width, card_height)
                    use ell_memory_card(game.deck_id, card_id, _revealed, _matched, card_width, card_height)
            else:
                use ell_memory_card(game.deck_id, card_id, _revealed, _matched, card_width, card_height)
            if _matched:
                $ _glow = ell_memory_art(game.deck_id, "highlight")
                if _glow:
                    add Transform(_glow, xysize=(card_width, card_height)) at ell_memory_matched_glow
            elif game.locked and index in game.opened:
                $ _error = ell_memory_art(game.deck_id, "incorrect")
                if _error:
                    add Transform(_error, xysize=(card_width, card_height)) at ell_memory_error_flash


screen ell_memory_companion(game):
    frame:
        xpos 1232
        ypos 230
        xysize (608, 688)
        padding (24, 20)
        background Frame(ell_minigame_ui("panel"), 36, 36)
        fixed:
            xysize (560, 648)
            # The existing artwork is referenced directly, never rewritten.
            add AlphaMask(Transform(Crop((0, 30, 1024, 1110), ELL_MEMORY_TSUKI_ART), xysize=(560, 458), fit="cover"), Transform(ell_minigame_ui("portrait_mask"), xysize=(560, 458)))
            frame:
                xpos 0
                ypos 474
                xysize (560, 174)
                padding (24, 20)
                background Frame(ell_minigame_ui("dialogue"), 36, 36)
                vbox:
                    spacing 12
                    hbox:
                        spacing 12
                        add Transform(ell_minigame_ui("icon_moon"), xysize=(30, 30))
                        text "Tsuki" style "ell_minigame_title" size 27 color "#E4C575"
                    text ell_memory_reaction(game) style "ell_minigame_body" size 23 xmaximum 505


screen ellrijord_memory_screen(game):
    modal True
    zorder 250
    key "game_menu" action ShowMenu("showmenu")
    add ell_minigame_ui("background")
    text "Tsuki's Memory Challenge" style "ell_minigame_title" size 44 xalign 0.5 ypos 45
    $ _caption = ell_memory_difficulty(game.difficulty_id)[1]
    text ("CLASSIC   ·   " + _caption.upper()) style "ell_memory_caption" xalign 0.5 ypos 103
    fixed:
        xpos 1710
        ypos 48
        use ell_minigame_icon_button("save", ShowMenu("save"), "Save game", "minigame_save")
    fixed:
        xpos 1782
        ypos 48
        use ell_minigame_icon_button("menu", ShowMenu("showmenu"), "Pause menu", "minigame_pause")

    $ _best = ell_memory_best(game.deck_id, game.difficulty_id, game.mode)
    $ _best_text = "{} moves · {}".format(_best["moves"], ell_memory_time(_best["elapsed_seconds"])) if _best else "Set your first best"
    if game.complete and (_best is None or (game.moves, game.elapsed) < (_best["moves"], _best["elapsed_seconds"])):
        $ _best_text = "{} moves · {}".format(game.moves, ell_memory_time(game.elapsed))
    hbox:
        xpos 188
        ypos 137
        spacing 16
        use ell_memory_stat("MOVES", str(game.moves), "moon")
        use ell_memory_stat("TIME", ell_memory_time(game.elapsed), "clock")
        use ell_memory_stat("MATCHED PAIRS", "{} / {}".format(len(game.matched) // 2, game.pairs), "pairs")
        use ell_memory_stat("PERSONAL BEST", _best_text, "trophy")

    frame:
        xpos 80
        ypos 230
        xysize (1120, 688)
        padding (24, 22)
        background Frame(ell_minigame_ui("panel"), 36, 36)
        fixed:
            xysize (1072, 644)
            $ _card_height = min(205, (622 - 12 * (game.rows - 1)) // game.rows, (1036 - 12 * (game.columns - 1)) // game.columns * 560 // 400)
            $ _card_width = _card_height * 400 // 560
            grid game.columns game.rows:
                align (0.5, 0.5)
                spacing 12
                for i, card_id in enumerate(game.cards):
                    use ell_memory_card_button(game, i, card_id, _card_width, _card_height)
    use ell_memory_companion(game)
    text ("Every plushie has found a friend!" if game.complete else "Find two matching plushies. Each pair of flips is one move.") style "ell_minigame_body" color ("#E4C575" if game.complete else "#A58AC5") size 19 xalign 0.5 ypos 930
    hbox:
        xalign 0.5
        ypos 971
        spacing 24
        use ell_minigame_button("Restart", Return(("restart", None)), "restart", button_id="memory_restart")
        use ell_minigame_button("Instructions", ShowMenu("ell_memory_instructions"), "instructions", button_id="memory_instructions")
        use ell_minigame_button("Finish" if game.complete else "Exit", Return(("finish" if game.complete else "leave", None)), "exit", button_id="minigame_back")
    $ _tip = GetTooltip()
    if _tip:
        text _tip style "ell_minigame_body" size 16 xpos 1655 ypos 113
    if game.locked:
        timer 0.85 action Return(("hide", None))
    elif not game.complete:
        timer 1.0 action Return(("tick", None))


screen ell_memory_instructions():
    tag menu
    modal True
    key "game_menu" action Return()
    use ell_minigame_shell("How to play", "Tsuki's Memory Challenge · Classic"):
        fixed:
            xfill True
            ysize 700
            vbox:
                align (0.5, 0.5)
                spacing 28
                text "Find a friend for every plushie" style "ell_minigame_title" size 36 xalign 0.5
                text "Turn over two cards. If they match, they stay face up." style "ell_minigame_body" xalign 0.5
                text "If they don't match, remember them before they turn back." style "ell_minigame_body" xalign 0.5
                text "Each pair of flips counts as one move. Match every pair to finish." style "ell_minigame_body" xalign 0.5
                text "Your personal best is the fewest moves; time breaks a tie." style "ell_minigame_body" xalign 0.5
                text "The timer pauses while instructions, save or pause menus are open." style "ell_minigame_body" color "#A58AC5" xalign 0.5
                text "You can save and resume your board later." style "ell_minigame_body" color "#E7A9BC" xalign 0.5
        hbox:
            xalign 0.5
            use ell_minigame_button("Back to the cards", Return(), "play", width=370, button_id="memory_instructions_back")


screen ell_memory_restart_confirm():
    modal True
    zorder 250
    key "game_menu" action Return(False)
    add ell_minigame_ui("background")
    frame:
        align (0.5, 0.5)
        xysize (930, 330)
        padding (42, 36)
        background Frame(ell_minigame_ui("panel"), 36, 36)
        vbox:
            spacing 28
            xalign 0.5
            text "Start a new round?" style "ell_minigame_title" size 36 xalign 0.5
            text "Your current board will be shuffled and your counters reset." style "ell_minigame_body" size 22 xalign 0.5
            hbox:
                xalign 0.5
                spacing 24
                use ell_minigame_button("Keep playing", Return(False), "play", width=300, button_id="memory_restart_no")
                use ell_minigame_button("Restart", Return(True), "restart", width=300, button_id="memory_restart_yes")
