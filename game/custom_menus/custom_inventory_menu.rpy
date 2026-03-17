init -5 python:
    ELL_INVENTORY_TABS = [
        {"id": "quests", "label": "📜 Quests"},
        {"id": "achievements", "label": "🏆 Achievements"},
        {"id": "inventory", "label": "🎒 Inventory"},
        {"id": "collectibles", "label": "💎 Collectibles"},
        {"id": "characters", "label": "👥 Characters"},
    ]

    ELL_INVENTORY_TAB_COLORS = {
        "quests": {
            "accent": "#d8b24f",
            "accent_soft": "#d8b24f22",
            "selected_bg": "#f1dfaa",
            "selected_text": "#4d3810",
        },
        "achievements": {
            "accent": "#9b6cff",
            "accent_soft": "#9b6cff22",
            "selected_bg": "#dccdff",
            "selected_text": "#35205f",
        },
        "inventory": {
            "accent": "#63a8ff",
            "accent_soft": "#63a8ff22",
            "selected_bg": "#cfe3ff",
            "selected_text": "#173a66",
        },
        "collectibles": {
            "accent": "#35c7c2",
            "accent_soft": "#35c7c222",
            "selected_bg": "#c7f3f1",
            "selected_text": "#0d5350",
        },
        "characters": {
            "accent": "#ff7fb6",
            "accent_soft": "#ff7fb622",
            "selected_bg": "#ffd2e4",
            "selected_text": "#6d2244",
        },
    }

    def ell_inventory_items():
        items = getattr(renpy.store, "ell_inventory_items", [])
        if callable(items):
            return []
        return list(items)

    def ell_inventory_summary_rows():
        plushies_found = len(set(getattr(renpy.store.persistent, "plushies_found", set())))
        frames_found = len(set(getattr(renpy.store.persistent, "picture_frames_found", set())))
        active_quests = len(set(getattr(renpy.store, "ell_active_quests", set())))
        completed_quests = len(set(getattr(renpy.store, "ell_completed_quests", set())))

        return [
            ("Active Quests", str(active_quests)),
            ("Completed Quests", str(completed_quests)),
            ("Plushies Found", "{}/25".format(plushies_found)),
            ("Picture Frames", "{}/25".format(frames_found)),
        ]

    def ell_inventory_search_blob(item):
        return " ".join([str(v).lower() for v in item.values() if v is not None])

    def ell_inventory_matches(item, search_text):
        if not search_text:
            return True
        return search_text.lower().strip() in ell_inventory_search_blob(item)

    def ell_inventory_quest_items():
        out = []
        progress_map = dict(getattr(renpy.store, "ell_quest_progress", {}))

        for quest_id in sorted(set(getattr(renpy.store, "ell_active_quests", set()))):
            quest = renpy.store.ELL_QUESTS.get(quest_id, None)
            if not quest:
                continue
            target = max(1, int(quest.get("target", 1)))
            progress = int(progress_map.get(quest_id, 0))
            out.append({
                "title": quest.get("title", quest_id),
                "status": "Active",
                "progress": int((float(progress) / float(target)) * 100),
                "progress_text": "{}/{}".format(progress, target),
                "desc": quest.get("description", ""),
                "giver": quest.get("giver", ""),
            })

        for quest_id in sorted(set(getattr(renpy.store, "ell_completed_quests", set()))):
            quest = renpy.store.ELL_QUESTS.get(quest_id, None)
            if not quest:
                continue
            target = max(1, int(quest.get("target", 1)))
            out.append({
                "title": quest.get("title", quest_id),
                "status": "Completed",
                "progress": 100,
                "progress_text": "{}/{}".format(target, target),
                "desc": quest.get("description", ""),
                "giver": quest.get("giver", ""),
            })

        return out

    def ell_inventory_achievement_items():
        out = []
        achievement_cls = getattr(renpy.store, "Achievement", None)
        if achievement_cls is None:
            return out

        for ach in achievement_cls.all_achievements:
            unlocked = ach.has()
            has_progress_bar = bool(ach.stat_max and ach.show_progress_bar)
            progress_raw = int(ach.stat_progress or 0) if ach.stat_max else 0
            if unlocked:
                rarity = "Unlocked"
            elif has_progress_bar and progress_raw > 0:
                rarity = "{}/{}".format(progress_raw, int(ach.stat_max))
            else:
                rarity = "Locked"
            if has_progress_bar:
                progress = int((float(progress_raw) / float(max(1, ach.stat_max))) * 100)
            else:
                progress = 100 if unlocked else 0

            if ach.id == "platinum_achievement":
                badge_icon = "👑"
            elif ach.id == "picture_frame_hunter_25":
                badge_icon = "🖼"
            elif "tsuki" in ach.id.lower() or "plush" in ach.id.lower() or "plush" in ach.name.lower():
                badge_icon = "🦊"
            elif "story" in ach.id.lower() or "story" in ach.name.lower():
                badge_icon = "📜"
            else:
                badge_icon = "🏆"

            ach_id = ach.id.lower()
            ach_name = ach.name.lower()
            if ach_id == "platinum_achievement" or "platinum" in ach_name:
                rarity_tier = "platinum"
                rarity_border = "#b57cff"
                rarity_glow = "#e0c2ff"
            elif "gold" in ach_name or "hunter" in ach_name:
                rarity_tier = "gold"
                rarity_border = "#d9b24c"
                rarity_glow = "#f4df9c"
            elif "silver" in ach_name:
                rarity_tier = "silver"
                rarity_border = "#b7c3d2"
                rarity_glow = "#e4ebf3"
            else:
                rarity_tier = "bronze"
                rarity_border = "#b97846"
                rarity_glow = "#dfb18b"

            out.append({
                "title": ach.name,
                "badge_icon": badge_icon,
                "rarity_tier": rarity_tier,
                "rarity": rarity,
                "rarity_color": "#c9a3ff" if unlocked else ("#b98cff" if has_progress_bar else "#9aa6ba"),
                "glow_top": (rarity_glow + "88") if unlocked else ((rarity_border + "66") if has_progress_bar else "#6d5e8a44"),
                "glow_bottom": (rarity_glow + "66") if unlocked else ((rarity_border + "50") if has_progress_bar else "#6d5e8a30"),
                "glow_side": (rarity_glow + "88") if unlocked else ((rarity_border + "66") if has_progress_bar else "#6d5e8a44"),
                "accent_strip": rarity_glow if unlocked else (rarity_border if has_progress_bar else "#5d5374"),
                "card_bg": "#3b215a66" if unlocked else ("#24173d88" if has_progress_bar else "#1a1f2d88"),
                "badge_bg": "#3a1456" if unlocked else ("#241042" if has_progress_bar else "#171326"),
                "desc": ach.description,
                "progress": progress,
                "show_progress_bar": has_progress_bar,
                "timestamp": ach.timestamp if unlocked else "",
            })

        return out

    def ell_inventory_collectible_items():
        plushies_found = set(getattr(renpy.store.persistent, "plushies_found", set()))
        picture_frames_found = set(getattr(renpy.store.persistent, "picture_frames_found", set()))

        return [
            {
                "title": "Tsuki's Plushies",
                "type": "Collection",
                "found": len(plushies_found) > 0,
                "status": "{}/25 found".format(len(plushies_found)),
                "desc": "Hidden plushies scattered through the story.",
            },
            {
                "title": "Picture Frames",
                "type": "Collection",
                "found": len(picture_frames_found) > 0,
                "status": "{}/25 found".format(len(picture_frames_found)),
                "desc": "Secret picture frames tied to exploration.",
            },
        ]

    def ell_inventory_character_items():
        typed_name = getattr(renpy.store, "mc_first_name", "")
        female_name = typed_name if (getattr(renpy.store, "mc_gender", None) == "female" and typed_name) else "Akari"
        male_name = typed_name if (getattr(renpy.store, "mc_gender", None) == "male" and typed_name) else "Kaito"

        out = [
            {"name": female_name, "role": "Protagonist", "affinity": "Light", "desc": "Female player route lead."},
            {"name": male_name, "role": "Protagonist", "affinity": "Void", "desc": "Male player route lead."},
            {"name": "Tsuki", "role": "Younger Sister", "affinity": "Home", "desc": "Central to the plushie collection quest."},
            {"name": "Rika", "role": "Year 2", "affinity": "Mystery", "desc": "Mentioned in the opening school route."},
        ]

        return out

    def ell_inventory_tab_items(tab_id, search_text=""):
        if tab_id == "quests":
            items = ell_inventory_quest_items()
        elif tab_id == "achievements":
            items = ell_inventory_achievement_items()
        elif tab_id == "collectibles":
            items = ell_inventory_collectible_items()
        elif tab_id == "characters":
            items = ell_inventory_character_items()
        else:
            items = ell_inventory_items()

        return items


style inv_shell_frame:
    background "#07111dcc"
    xpadding 28
    ypadding 28

style inv_sidebar_frame:
    background "#ffffff0a"
    xpadding 18
    ypadding 18

style inv_main_frame is inv_sidebar_frame

style inv_tab_button:
    background "#00000000"
    hover_background "#ffffff10"
    xfill True
    ypadding 14
    xpadding 18

style inv_tab_button_text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 25
    color "#eef3ff"
    hover_color "#ffffff"
    selected_color "#1b2431"

style inv_title is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 50
    color "#f6f1e7"

style inv_subtitle is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 20
    color "#d6deef"

style inv_section_title is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 30
    color "#fcf7ee"

style inv_body_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 22
    color "#edf3ff"

style inv_muted_text is inv_body_text:
    color "#b9c5d8"

style inv_label_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 16
    color "#95a4bc"

style inv_card_frame:
    background "#ffffff0b"
    xpadding 22
    ypadding 18

style inv_card_frame_achievement:
    background "#ffffff0b"
    xpadding 0
    ypadding 0

style inv_card_button:
    background "#ffffff0b"
    hover_background "#ffffff12"
    xpadding 0
    ypadding 0


screen inventory_menu():

    tag menu

    default inv_tab = "quests"
    default inv_scroll = ui.adjustment()

    if "ell_sync_collectible_quests" in globals():
        on "show" action Function(ell_sync_collectible_quests)

    $ bag_idle = "gui/Bag btn_720p.png"
    $ summary_rows = ell_inventory_summary_rows()
    $ tab_items = ell_inventory_tab_items(inv_tab)
    $ tab_label = next((t["label"] for t in ELL_INVENTORY_TABS if t["id"] == inv_tab), "Inventory")
    $ tab_colors = ELL_INVENTORY_TAB_COLORS.get(inv_tab, ELL_INVENTORY_TAB_COLORS["quests"])

    add Transform("gui/game_menu.png", xsize=config.screen_width, ysize=config.screen_height)
    add Solid("#020617bb")

    frame:
        style "inv_shell_frame"
        xpos 74
        ypos 64
        xsize 1772
        ysize 952

        hbox:
            spacing 22

            frame:
                style "inv_sidebar_frame"
                xsize 300
                ysize 896

                vbox:
                    spacing 14

                    hbox:
                        spacing 14
                        add Transform(bag_idle, xsize=72, ysize=72)
                        vbox:
                            spacing 2
                            text _("Inventory Hub") style "inv_section_title"
                            text _("Your in-game systems menu.") style "inv_label_text"

                    null height 8

                    for tab in ELL_INVENTORY_TABS:
                        $ sidebar_tab_colors = ELL_INVENTORY_TAB_COLORS.get(tab["id"], tab_colors)
                        textbutton _(tab["label"]):
                            style "inv_tab_button"
                            text_style "inv_tab_button_text"
                            action SetScreenVariable("inv_tab", tab["id"])
                            selected (inv_tab == tab["id"])
                            if inv_tab == tab["id"]:
                                selected_background sidebar_tab_colors["selected_bg"]
                                text_selected_color sidebar_tab_colors["selected_text"]
                            text_hover_color sidebar_tab_colors["accent"]

                    null height 18
                    text _("Overview") style "inv_label_text" color tab_colors["accent"]

                    for row_label, row_value in summary_rows:
                        hbox:
                            xfill True
                            text _(row_label) style "inv_muted_text"
                            text row_value style "inv_body_text" color tab_colors["accent"] xalign 1.0

            frame:
                style "inv_main_frame"
                xsize 1392
                ysize 896

                vbox:
                    spacing 18

                    hbox:
                        xfill True

                        vbox:
                            spacing 5
                            text _("Menu System") style "inv_label_text"
                            text _("Inventory Hub") style "inv_title"
                            text _("Browse and manage your progress.") style "inv_subtitle"

                    frame:
                        style "inv_card_frame"
                        background tab_colors["accent_soft"]
                        xfill True
                        ysize 92

                        hbox:
                            spacing 26
                            yalign 0.5

                            vbox:
                                spacing 4
                                text _(tab_label) style "inv_section_title" color tab_colors["accent"]
                                if inv_tab == "quests":
                                    text _("Active and completed story progress.") style "inv_muted_text"
                                elif inv_tab == "achievements":
                                    text _("Unlocked milestones and hidden rewards.") style "inv_muted_text"
                                elif inv_tab == "collectibles":
                                    text _("Exploration progress and secret finds.") style "inv_muted_text"
                                elif inv_tab == "characters":
                                    text _("Key cast members currently surfaced by the story.") style "inv_muted_text"
                                else:
                                    text _("Tracked items and future pickups.") style "inv_muted_text"

                            null width 40
                            text _("{0} entries".format(len(tab_items))) style "inv_body_text" color tab_colors["accent"]

                    fixed:
                        xsize 1328
                        ysize 620
                        clipping True

                        viewport:
                            mousewheel True
                            draggable True
                            pagekeys True
                            yadjustment inv_scroll
                            scrollbars None
                            xsize 1328
                            ysize 620

                            vbox:
                                spacing 16

                                if tab_items:

                                    if inv_tab == "quests":
                                        for q in tab_items:
                                            $ quest_card_bg = tab_colors["accent_soft"] if q["status"] == "Active" else "#ffffff0b"
                                            frame:
                                                style "inv_card_frame"
                                                xfill True
                                                background quest_card_bg

                                                vbox:
                                                    spacing 10

                                                    hbox:
                                                        xfill True
                                                        text q["title"] style "inv_section_title"
                                                        text _(q["status"]) style "inv_body_text" color tab_colors["accent"] xalign 1.0

                                                    if q.get("giver"):
                                                        text ("From: " + q["giver"]) style "inv_label_text"
                                                    text q["desc"] style "inv_muted_text"

                                                    hbox:
                                                        xfill True
                                                        text _("Progress") style "inv_label_text"
                                                        text q["progress_text"] style "inv_body_text" xalign 1.0

                                                    bar value StaticValue(q["progress"], 100):
                                                        xfill True
                                                        left_bar Frame(Solid(tab_colors["accent"]), 0, 0)
                                                        right_bar Frame(Solid("#0a1826"), 0, 0)

                                    elif inv_tab == "achievements":
                                        for a in tab_items:
                                            frame:
                                                style "inv_card_frame_achievement"
                                                xfill True
                                                background a["card_bg"]

                                                fixed:
                                                    xfill True
                                                    ysize 112

                                                    add Solid(a["accent_strip"]) xpos 0 ypos 0 xsize 8 ysize 112
                                                    add Solid(a["glow_top"]) xpos 8 ypos 0 ysize 3
                                                    add Solid(a["glow_bottom"]) xpos 8 ypos 109  ysize 3
                                                    add Solid(a["glow_side"]) xpos 8 ypos 3 xsize 3 ysize 106
                                                    add Solid(a["glow_side"]) xpos 1325 ypos 3 xsize 3 ysize 106

                                                    frame:
                                                        background a["badge_bg"]
                                                        xpos 22
                                                        ypos 10
                                                        xsize 90
                                                        ysize 90
                                                        xpadding 7
                                                        ypadding 7

                                                        text a["badge_icon"]:
                                                            xalign 0.5
                                                            yalign 0.5
                                                            size 64

                                                    vbox:
                                                        xpos 132
                                                        ypos 6
                                                        spacing 6
                                                        xsize 670

                                                        text a["title"] style "inv_section_title"
                                                        text a["desc"] style "inv_muted_text"
                                                        if a.get("timestamp"):
                                                            text a["timestamp"] style "inv_label_text"

                                                    text _(a["rarity"]) style "inv_body_text" color a["rarity_color"]:
                                                        xpos 880
                                                        ypos 10
                                                        xsize 320
                                                        text_align 0.5

                                                    if a.get("show_progress_bar", False):
                                                        fixed:
                                                            xpos 880
                                                            ypos 48
                                                            xsize 320
                                                            ysize 30

                                                            add Solid("#d8a8ff18") xpos 0 ypos 4 xsize 320 ysize 20
                                                            add Solid("#c58cff30") xpos 2 ypos 6 xsize 316 ysize 16
                                                            add Solid("#b06cff40") xpos 6 ypos 8 xsize 308 ysize 12
                                                            add Solid("#ffffff30") xpos 10 ypos 9 xsize 300 ysize 3

                                                            bar value StaticValue(a["progress"], 100):
                                                                xpos 0
                                                                ypos 6
                                                                xsize 320
                                                                ysize 14
                                                                left_bar Frame(Solid("#c58cff"), 0, 0)
                                                                right_bar Frame(Solid("#08121d"), 0, 0)

                                    elif inv_tab == "collectibles":
                                        for c in tab_items:
                                            frame:
                                                style "inv_card_frame"
                                                xfill True
                                                background tab_colors["accent_soft"]

                                                hbox:
                                                    xfill True
                                                    spacing 18

                                                    add Transform("gui/window_icon.png", xsize=64, ysize=64)

                                                    vbox:
                                                        spacing 6
                                                        text c["title"] style "inv_section_title"
                                                        text c["desc"] style "inv_muted_text"
                                                        text c["type"] style "inv_label_text"

                                                    text c["status"] style "inv_body_text" color tab_colors["accent"] xalign 1.0

                                    elif inv_tab == "characters":
                                        for ch in tab_items:
                                            frame:
                                                style "inv_card_frame"
                                                xfill True
                                                background tab_colors["accent_soft"]

                                                hbox:
                                                    xfill True
                                                    spacing 18

                                                    add Transform("gui/window_icon.png", xsize=64, ysize=64)

                                                    vbox:
                                                        spacing 6
                                                        text ch["name"] style "inv_section_title"
                                                        text ch["desc"] style "inv_muted_text"

                                                    vbox:
                                                        spacing 6
                                                        text ch["role"] style "inv_body_text" color tab_colors["accent"]
                                                        text ch["affinity"] style "inv_label_text" color tab_colors["accent"]

                                    else:
                                        for item in tab_items:
                                            frame:
                                                style "inv_card_frame"
                                                xfill True
                                                background tab_colors["accent_soft"]

                                                vbox:
                                                    spacing 8
                                                    text item.get("name", _("Unknown Item")) style "inv_section_title"
                                                    text item.get("description", _("No description yet.")) style "inv_muted_text"
                                else:
                                    frame:
                                        style "inv_card_frame"
                                        xfill True
                                        ysize 260
                                        background tab_colors["accent_soft"]

                                        vbox:
                                            spacing 14
                                            xalign 0.5
                                            yalign 0.5
                                            if inv_tab == "quests":
                                                text _("📜 No Quests Yet") style "inv_section_title" color tab_colors["accent"] xalign 0.5
                                                text _("Your adventure hasn't begun.") style "inv_body_text" xalign 0.5
                                                text _("Explore the world to discover your first quest.") style "inv_muted_text" xalign 0.5
                                            elif inv_tab == "inventory":
                                                text _("🎒 Inventory Empty") style "inv_section_title" color tab_colors["accent"] xalign 0.5
                                                text _("You are not carrying anything yet.") style "inv_body_text" xalign 0.5
                                                text _("Items you discover during exploration will appear here.") style "inv_muted_text" xalign 0.5
                                            elif inv_tab == "collectibles":
                                                text _("💎 No Collectibles Found") style "inv_section_title" color tab_colors["accent"] xalign 0.5
                                                text _("The world is still hiding its secrets.") style "inv_body_text" xalign 0.5
                                                text _("Rare finds and special discoveries will show up here.") style "inv_muted_text" xalign 0.5
                                            elif inv_tab == "characters":
                                                text _("👥 No Character Notes Yet") style "inv_section_title" color tab_colors["accent"] xalign 0.5
                                                text _("You haven't filled out this section yet.") style "inv_body_text" xalign 0.5
                                                text _("Important people you meet can be surfaced here over time.") style "inv_muted_text" xalign 0.5
                                            else:
                                                text _("🏆 No Achievements Yet") style "inv_section_title" color tab_colors["accent"] xalign 0.5
                                                text _("Your record is still unwritten.") style "inv_body_text" xalign 0.5
                                                text _("Milestones and hidden rewards will appear as you play.") style "inv_muted_text" xalign 0.5

    hbox:
        xalign 0.5
        yalign 0.975
        spacing 20

        if main_menu:
            use ui_png_button(_("Back"), ShowMenu("main_menu"), xsize=220, ysize=56, text_style="ui_btn_text_small")
        else:
            use ui_png_button(_("Back"), Return(), xsize=220, ysize=56, text_style="ui_btn_text_small")
