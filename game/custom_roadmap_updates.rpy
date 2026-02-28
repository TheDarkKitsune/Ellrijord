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
            "title": "LAUNCH",
            "width": 620,
            "columns": 2,
            "split_index": 14,
            "items": [
                {"key": "roadmap_phase_1_item_1", "text": "Goal: polished vertical slice with 3-4 romance routes."},
                {"key": "roadmap_phase_1_item_2", "text": "Arc scope: complete launch story that teases the void plot."},
                {"key": "roadmap_phase_1_item_3", "text": "Scope rule: no combat system at launch."},
                {"key": "roadmap_phase_1_item_4", "text": "Scope rule: no large branching war arc."},
                {"key": "roadmap_phase_1_item_5", "text": "Scope rule: school-life + mystery slow burn focus."},
                {"key": "roadmap_phase_1_item_6", "text": "Playable length: 10-14 in-game days."},
                {"key": "roadmap_phase_1_item_7", "text": "Content target: 3 main routes + 1 hidden unlock route."},
                {"key": "roadmap_phase_1_item_8", "text": "Runtime target: 6-8 hours total."},
                {"key": "roadmap_phase_1_item_9", "text": "Route 1 Reina Takamine: strict start, hidden burden, void-aware reveal."},
                {"key": "roadmap_phase_1_item_10", "text": "Reina climax: rooftop confession during first void anomaly."},
                {"key": "roadmap_phase_1_item_11", "text": "Route 2 Mimi Usagiyama: comfort arc, anxiety growth, protective MC beats."},
                {"key": "roadmap_phase_1_item_12", "text": "Mimi climax: forest night event."},
                {"key": "roadmap_phase_1_item_13", "text": "Route 3 Poko Kazunami: comedy-heavy with suspicious artifact theft angle."},
                {"key": "roadmap_phase_1_item_14", "text": "Poko climax: city after-hours incident."},
                {"key": "roadmap_phase_1_item_15", "text": "Hidden route after first clear: Lady Ender Echo (partial route)."},
                {"key": "roadmap_phase_1_item_16", "text": "Echo route beats: dream interactions, void link, cliffhanger ending."},
                {"key": "roadmap_phase_1_item_17", "text": "Launch maps (school hub): classroom, courtyard, rooftop, club hallway."},
                {"key": "roadmap_phase_1_item_18", "text": "City map: cafe, shrine, arcade, night street."},
                {"key": "roadmap_phase_1_item_19", "text": "Forest map: clearing + ruins (ruins locked until midgame)."},
                {"key": "roadmap_phase_1_item_20", "text": "Map rule: keep it small; depth over width."},
                {"key": "roadmap_phase_1_item_21", "text": "Day system: Morning -> School -> After School -> Evening."},
                {"key": "roadmap_phase_1_item_22", "text": "Affection system: hidden numeric variable per heroine."},
                {"key": "roadmap_phase_1_item_23", "text": "Route lock window: Day 6-8 via affection thresholds."},
                {"key": "roadmap_phase_1_item_24", "text": "Void events: minor anomaly (Day 5), major anomaly (finale)."},
            ],
        },
        {
            "title_key": "roadmap_phase_2_title",
            "title": "PHASE 2 - EXPANSION UPDATE",
            "width": 390,
            "columns": 1,
            "items": [
                {"key": "roadmap_phase_2_item_1", "text": "Goal: deepen the world + add 3 routes (6-12 months)."},
                {"key": "roadmap_phase_2_item_2", "text": "Tilly Ashford route: energetic chaos + comic relief."},
                {"key": "roadmap_phase_2_item_3", "text": "Tilly focus: hidden emotional depth + major forest event."},
                {"key": "roadmap_phase_2_item_4", "text": "New Route: Mio Shirasaki (transfer student)."},
                {"key": "roadmap_phase_2_item_5", "text": "Mio focus: subtle void sensitivity + mystery-heavy route."},
                {"key": "roadmap_phase_2_item_6", "text": "New Route: Sakura Aoyama (pink-haired calm type)."},
                {"key": "roadmap_phase_2_item_7", "text": "Sakura focus: emotional healing + soft romance path."},
                {"key": "roadmap_phase_2_item_8", "text": "Forest expansion: deeper area + void distortion zone."},
                {"key": "roadmap_phase_2_item_9", "text": "Forest expansion: night exploration events."},
                {"key": "roadmap_phase_2_item_10", "text": "Light void mechanics: visual glitches."},
                {"key": "roadmap_phase_2_item_11", "text": "Light void mechanics: choice-driven corruption meter."},
                {"key": "roadmap_phase_2_item_12", "text": "Light void mechanics: small dream sequences."},
                {"key": "roadmap_phase_2_item_13", "text": "City expansion: underground area + Bellmont subplot."},
                {"key": "roadmap_phase_2_item_14", "text": "City expansion: late-night city event."},
                {"key": "roadmap_phase_2_item_15", "text": "Narrative reveal: why MC is special."},
                {"key": "roadmap_phase_2_item_16", "text": "Narrative reveal: what Tsuki senses."},
                {"key": "roadmap_phase_2_item_17", "text": "Narrative reveal: Reina's prior void encounter."},
            ],
        },
        {
            "title_key": "roadmap_phase_3_title",
            "title": "PHASE 3 - MAJOR ARC",
            "width": 390,
            "columns": 1,
            "items": [
                {"key": "roadmap_phase_3_item_1", "text": "Major arc: Ellrijord fully enters the story."},
                {"key": "roadmap_phase_3_item_2", "text": "Return to Ellrijord: limited arc (2-3 chapters)."},
                {"key": "roadmap_phase_3_item_3", "text": "Areas: broken Yggdrasil ruins + void-controlled zones."},
                {"key": "roadmap_phase_3_item_4", "text": "Full Lady Ender route."},
                {"key": "roadmap_phase_3_item_5", "text": "Lady Ender route tone: redemption vs tragic duality."},
                {"key": "roadmap_phase_3_item_6", "text": "Major choice: save or destroy Lady Ender."},
                {"key": "roadmap_phase_3_item_7", "text": "New route: Yukino Kuzunoha (older sister arc)."},
                {"key": "roadmap_phase_3_item_8", "text": "New route: Lilith Ravenshade (void-born route)."},
                {"key": "roadmap_phase_3_item_9", "text": "New route: Aria Bellmont (political intrigue route)."},
                {"key": "roadmap_phase_3_item_10", "text": "Strategy: large cast, avoid all routes at launch."},
                {"key": "roadmap_phase_3_item_11", "text": "School core (launch): Reina, Mimi, Poko, Tsuki (anchor)."},
                {"key": "roadmap_phase_3_item_12", "text": "City support (phase 2+): Bellmont siblings, Kuroe, Aoi, Emi, Kaya."},
                {"key": "roadmap_phase_3_item_13", "text": "Supernatural cast (phase 3): Lady Ender, Lilith, Yukino, Ellrijord cast."},
            ],
        },
    ]


style roadmap_title_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 62
    color "#ecf6ff"
    outlines [(3, "#06152a", 0, 0)]
    xalign 0.5

style roadmap_launch_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 30
    color "#e4c05b"
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
    size 18
    color "#0b1220"
    outlines [(1, "#f5dda0", 0, 0)]
    text_align 0.5
    xalign 0.5
    yalign 0.5

style roadmap_item_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 13
    color "#f2f8ff"
    outlines [(2, "#061428", 0, 0)]
    line_spacing 1

style roadmap_note_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 18
    color "#d9e9fb"
    outlines [(1, "#081b33", 0, 0)]
    text_align 0.5
    xalign 0.5


screen roadmap_phase_items(entries):
    vbox:
        spacing 10
        for entry in entries:
            text "- " + _roadmap_l(entry.get("key", ""), entry.get("text", "")) style "roadmap_item_text"


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
                background Solid("#dfbf5a")
                xfill True
                ysize 64
                padding (12, 8)
                text _roadmap_l(phase.get("title_key", ""), phase.get("title", "")) style "roadmap_phase_title_text"

            frame:
                background Solid("#041427dd")
                xfill True
                yfill True
                padding (14, 12)

                viewport:
                    mousewheel True
                    draggable True
                    scrollbars None
                    xfill True
                    yfill True

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
        ysize 920

        add Solid("#0a335a") xsize 1760 ysize 920
        add Solid("#062949c9") xpos 6 ypos 6 xsize 1748 ysize 908

        # Subtle blueprint-like accents.
        add Transform(Solid("#4f84b840"), xsize=860, ysize=2, rotate=-22, xpos=70, ypos=156)
        add Transform(Solid("#4f84b840"), xsize=780, ysize=2, rotate=18, xpos=920, ypos=142)
        add Transform(Solid("#4f84b840"), xsize=760, ysize=2, rotate=-14, xpos=980, ypos=640)
        add Transform(Solid("#4f84b840"), xsize=740, ysize=2, rotate=20, xpos=120, ypos=680)

        text _roadmap_l("roadmap_title", "DEVELOPMENT ROADMAP") style "roadmap_title_text":
            xalign 0.5
            ypos 56

        fixed:
            xpos 1370
            ypos 24
            use ui_png_button(L("news_close"), Hide("roadmap_updates_detail"), zoom=0.55, text_style="ui_btn_text_small", use_alt=mm_alt)

        hbox:
            xpos 44
            ypos 214
            spacing 16
            ysize 620

            frame:
                background Solid("#07233e00")
                xsize 160
                yfill True
                padding (8, 38)

                vbox:
                    spacing 20
                    text _roadmap_l("roadmap_launch", "LAUNCH") style "roadmap_launch_text"
                    text _roadmap_l("roadmap_launch_date", "TBA") style "roadmap_launch_date_text"

            for phase in ROADMAP_PHASES:
                use roadmap_phase_card(phase)

        text _roadmap_l("roadmap_summary", "This roadmap is divided into three phases and its contents may be adjusted as development continues.") style "roadmap_note_text":
            xalign 0.5
            ypos 870
