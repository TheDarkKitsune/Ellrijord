# custom_roadmap_updates.rpy
# Dedicated roadmap screen opened from the Roadmap news tile.

init -2 python:
    def _roadmap_l(key, fallback):
        txt = L(key)
        return txt if txt != key else fallback

    def _roadmap_chunk(items, parts, split_index=None):
        if parts <= 1:
            return [items]
        if parts == 2 and split_index is not None:
            split = max(1, min(int(split_index), len(items) - 1))
            return [items[:split], items[split:]]
        size = (len(items) + parts - 1) // parts
        return [items[i * size:(i + 1) * size] for i in range(parts)]

    ROADMAP_PHASES = [
        {
            "title_key": "roadmap_phase_1_title",
            "title": "Chapter I — Where the Void First Whispers",
            "width": 548,
            "columns": 1,
            "items": [
                {"key": "roadmap_phase_1_item_1", "text": "Within the academy and its surrounding city, new bonds form and destinies begin to intertwine."},
                {"key": "roadmap_phase_1_item_2", "text": "✨ 3 Main Romance Routes"},
                {"key": "roadmap_phase_1_item_3", "text": "✨ 1 Hidden Unlockable Route"},
                {"key": "roadmap_phase_1_item_4", "text": "✨ 6–8 Hours of Story-Driven Content"},
                {"key": "roadmap_phase_1_item_5", "text": "✨ School, City & Forest Exploration"},
                {"key": "roadmap_phase_1_item_6", "text": "✨ Branching Relationship Paths"},
                {"key": "roadmap_phase_1_item_7", "text": "✨ Emotional Confessions & Route-Specific Endings"},
                {"key": "roadmap_phase_1_item_8", "text": "This chapter introduces the core cast, the fragile warmth of budding romance, and the first quiet signs that something unseen is stirring beyond the veil of ordinary life."},
            ],
        },
        {
            "title_key": "roadmap_phase_2_title",
            "title": "Chapter II — When Hearts Deepen and Shadows Stir",
            "width": 548,
            "columns": 1,
            "items": [
                {"key": "roadmap_phase_2_item_1", "text": "The world grows wider. The forest darkens. The consequences of choice begin to take shape."},
                {"key": "roadmap_phase_2_item_2", "text": "✨ 3 New Romance Routes"},
                {"key": "roadmap_phase_2_item_3", "text": "✨ Expanded Forest & Night Exploration"},
                {"key": "roadmap_phase_2_item_4", "text": "✨ Void Corruption System"},
                {"key": "roadmap_phase_2_item_5", "text": "✨ Dream Sequence Events"},
                {"key": "roadmap_phase_2_item_6", "text": "✨ New City Locations & Hidden Underground Areas"},
                {"key": "roadmap_phase_2_item_7", "text": "✨ Deeper Emotional & Supernatural Arcs"},
                {"key": "roadmap_phase_2_item_8", "text": "As relationships strengthen and secrets surface, the balance between light and Void becomes increasingly fragile. New paths open — and with them, new risks."},
            ],
        },
        {
            "title_key": "roadmap_phase_3_title",
            "title": "Chapter III — When Ellrijord Steps Forward",
            "width": 548,
            "columns": 1,
            "items": [
                {"key": "roadmap_phase_3_item_1", "text": "The hidden forces behind the story step into full view."},
                {"key": "roadmap_phase_3_item_2", "text": "✨ Full Lady Ender Route"},
                {"key": "roadmap_phase_3_item_3", "text": "✨ Major Story-Altering Decisions"},
                {"key": "roadmap_phase_3_item_4", "text": "✨ Supernatural & Political Intrigue Routes"},
                {"key": "roadmap_phase_3_item_5", "text": "✨ Expanded Supporting Cast"},
                {"key": "roadmap_phase_3_item_6", "text": "✨ Multiple Route Outcomes"},
                {"key": "roadmap_phase_3_item_7", "text": "✨ High-Impact, World-Shaping Consequences"},
                {"key": "roadmap_phase_3_item_8", "text": "This chapter marks a turning point. Long-held mysteries unravel, loyalties are tested, and the choices made along the way will shape the fate of more than just a single heart."},
            ],
        },
    ]


style roadmap_title_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 56
    color "#ecf6ff"
    outlines [(3, "#06152a", 0, 0)]
    xalign 0.5

style roadmap_launch_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 30
    color "#5a2f8f"
    outlines [(2, "#0a1c35", 0, 0)]
    text_align 0.5
    xalign 0.5

style roadmap_launch_date_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 24
    color "#d9e8f7"
    outlines [(2, "#0a1c35", 0, 0)]
    text_align 0.5
    xalign 0.5

style roadmap_brand_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 32
    color "#d7ebff"
    outlines [(2, "#08182f", 0, 0)]
    xalign 0.5

style roadmap_phase_title_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 20
    color "#f7ecff"
    outlines [(1, "#2b2440", 0, 0)]
    text_align 0.5
    xalign 0.5
    yalign 0.5

style roadmap_item_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 16
    color "#f2f8ff"
    outlines [(2, "#061428", 0, 0)]
    line_spacing 2

style roadmap_note_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 18
    color "#d9e9fb"
    outlines [(1, "#081b33", 0, 0)]
    line_spacing 2
    text_align 0.5
    xalign 0.5

style roadmap_intro_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 18
    color "#d9e9fb"
    outlines [(1, "#081b33", 0, 0)]
    line_spacing 4
    text_align 0.5
    xalign 0.5

style roadmap_path_title_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 24
    color "#f7ecff"
    outlines [(2, "#1d1230", 0, 0)]
    text_align 0.5
    xalign 0.5

style roadmap_path_body_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 18
    color "#d9e9fb"
    outlines [(1, "#081b33", 0, 0)]
    line_spacing 2
    text_align 0.5
    xalign 0.5


screen roadmap_phase_items(entries):
    vbox:
        spacing 10
        for i, entry in enumerate(entries):
            $ item_text = _roadmap_l(entry.get("key", ""), entry.get("text", ""))
            if i == 1 and item_text.startswith("✨"):
                null height 6
            if i > 0 and (not item_text.startswith("✨")):
                null height 16
            text item_text style "roadmap_item_text"


screen roadmap_phase_card(phase):
    $ phase_width = int(phase.get("width", 360))
    $ phase_columns = max(1, int(phase.get("columns", 1)))
    $ phase_chunks = _roadmap_chunk(phase.get("items", []), phase_columns, phase.get("split_index", None))

    frame:
        background Solid("#08223fdd")
        xsize phase_width
        yfill True
        padding (0, 0)

        vbox:
            spacing 0

            frame:
                background Solid("#5a2f8f")
                xfill True
                ysize 70
                padding (12, 8)
                text _roadmap_l(phase.get("title_key", ""), phase.get("title", "")) style "roadmap_phase_title_text"

            frame:
                background Solid("#041427dd")
                xfill True
                yfill True
                padding (20, 20)

                if phase_columns > 1:
                    hbox:
                        spacing 14
                        xfill True
                        for chunk in phase_chunks:
                            vbox:
                                xsize int((phase_width - 48) / phase_columns)
                                use roadmap_phase_items(chunk)
                else:
                    use roadmap_phase_items(phase_chunks[0])


screen roadmap_updates_detail():
    modal True
    zorder 210
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))

    add Solid("#000a")

    fixed:
        xalign 0.5
        yalign 0.5
        xsize 1760
        ysize 950

        add Solid("#0a335a") xsize 1760 ysize 950
        add Solid("#062949c9") xpos 6 ypos 6 xsize 1748 ysize 938

        text _roadmap_l("roadmap_title", "The Chronicle of Ellrijord") style "roadmap_title_text":
            xalign 0.5
            ypos 44

        text _roadmap_l("roadmap_intro", "The story of Ellrijord unfolds in three great chapters — each expanding the world, deepening its bonds,\nand drawing the light and the Void ever closer together.\nWhat begins as a quiet tale of school life and hidden emotions will grow into something far greater.") style "roadmap_intro_text":
            xalign 0.5
            ypos 132
            xsize 1140

        fixed:
            xpos 1370
            ypos 24
            use ui_png_button(L("news_close"), Hide("roadmap_updates_detail"), zoom=0.55, text_style="ui_btn_text_small", use_alt=mm_alt)

        hbox:
            xalign 0.5
            ypos 220
            spacing 18
            ysize 600

            for phase in ROADMAP_PHASES:
                use roadmap_phase_card(phase)

        add Solid("#9fb9d040") xpos 220 ypos 822 xsize 1320 ysize 1

        text _roadmap_l("roadmap_path_title", "The Path Continues") style "roadmap_path_title_text":
            xalign 0.5
            ypos 830

        text _roadmap_l("roadmap_summary", "Ellrijord's journey is one of growth — of characters, of relationships, and of the world itself.\nAs the story unfolds, new chapters will bring deeper emotion, greater stakes, and expanding horizons.") style "roadmap_path_body_text":
            xalign 0.5
            ypos 866
            xsize 1260

        text _roadmap_l("roadmap_note_2", "The Chronicle is not yet complete.") style "roadmap_note_text":
            xalign 0.5
            ypos 916
