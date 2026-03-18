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
                "id": "plushies",
                "title": "Tsuki's Plushies",
                "type": "Collection",
                "found": len(plushies_found) > 0,
                "found_count": len(plushies_found),
                "total_count": 25,
                "status": "{}/25 found".format(len(plushies_found)),
                "desc": "Hidden plushies scattered through the story.",
                "display_image": "gui/tsuki_plushies.png",
            },
            {
                "id": "picture_frames",
                "title": "Picture Frames",
                "type": "Collection",
                "found": len(picture_frames_found) > 0,
                "found_count": len(picture_frames_found),
                "total_count": 25,
                "status": "{}/25 found".format(len(picture_frames_found)),
                "desc": "Secret picture frames tied to exploration.",
                "display_image": "gui/picture_frames.png",
            },
        ]

    def ell_collectible_thumbnail_path(collectible_id, entry_id):
        plush_map = {
            "cat_plush_1": "secrets/plushies/kittycat_plush.png",
        }
        frame_map = {
            "picture1": "secrets/Picture Frames/picture1.png",
        }

        if collectible_id == "plushies":
            return plush_map.get(entry_id, None)
        if collectible_id == "picture_frames":
            return frame_map.get(entry_id, None)
        return None

    def ell_collectible_preview_slots(collectible_id, slot_count=7):
        if collectible_id == "plushies":
            found_ids = sorted(set(getattr(renpy.store.persistent, "plushies_found", set())))
        else:
            found_ids = sorted(set(getattr(renpy.store.persistent, "picture_frames_found", set())))

        previews = []

        for entry_id in found_ids[:slot_count]:
            previews.append(ell_collectible_thumbnail_path(collectible_id, entry_id))

        while len(previews) < slot_count:
            previews.append(None)

        return previews

    def ell_inventory_character_portrait(*candidates):
        for candidate in candidates:
            if renpy.loadable(candidate):
                return candidate
        return "gui/window_icon.png"

    def ell_inventory_character_items():
        typed_name = getattr(renpy.store, "mc_first_name", "")
        female_name = typed_name if (getattr(renpy.store, "mc_gender", None) == "female" and typed_name) else "Akari"
        male_name = typed_name if (getattr(renpy.store, "mc_gender", None) == "male" and typed_name) else "Kaito"

        out = [
            {
                "id": "akari",
                "name": female_name,
                "role": "Protagonist",
                "affinity": "Light",
                "desc": "Female player route lead.",
                "portrait": ell_inventory_character_portrait("gui/Akari.png"),
                "personality": "Determined, warm, observant, quietly stubborn.",
                "description_long": "The Light-route protagonist. She pushes forward even when the day starts badly and tends to carry other people with her momentum.",
                "favorite_spots": ["Home bedroom in the morning", "School grounds after classes"],
                "storyline": "Her route focuses on connection, trust, and the brighter side of Ellrijord's mysteries.",
            },
            {
                "id": "kaito",
                "name": male_name,
                "role": "Protagonist",
                "affinity": "Void",
                "desc": "Male player route lead.",
                "portrait": ell_inventory_character_portrait("gui/Kaito.png"),
                "personality": "Dry, resilient, introspective, quietly protective.",
                "description_long": "The Void-route protagonist. He tends to process things internally first, but becomes decisive once he commits to a path.",
                "favorite_spots": ["Home bedroom in the morning", "School grounds after classes"],
                "storyline": "His route leans more heavily into tension, distance, and the stranger corners of the story.",
            },
            {
                "id": "tsuki",
                "name": "Tsuki",
                "role": "Younger Sister",
                "affinity": "Home",
                "desc": "Central to the plushie collection quest.",
                "portrait": ell_inventory_character_portrait("game/Ellrijord Characters/Family/MC Family/Tsuki Kuzunoha.png", "Ellrijord Characters/Family/MC Family/Tsuki Kuzunoha.png"),
                "personality": "Teasing, energetic, affectionate, impossible to ignore.",
                "description_long": "Tsuki anchors the early home scenes and gives the opening route a lot of its energy. She is also tied closely to the plushie side content.",
                "favorite_spots": ["Home kitchen before school", "Shared family spaces"],
                "storyline": "She is one of the first characters to shape the player's daily rhythm and side discoveries.",
            },
            {
                "id": "rika",
                "name": "Rika",
                "role": "Year 2",
                "affinity": "Mystery",
                "desc": "Mentioned in the opening school route.",
                "portrait": ell_inventory_character_portrait("game/Ellrijord Characters/Year 2s/Rika Kuzunoha.png", "Ellrijord Characters/Year 2s/Rika Kuzunoha.png"),
                "personality": "Reserved, intriguing, hard to place at first glance.",
                "description_long": "Rika enters the codex as someone the opening route points toward before fully explaining her role.",
                "favorite_spots": ["School corridors", "Anywhere the story starts hinting at secrets"],
                "storyline": "She currently sits in the story as a mystery hook that suggests more is coming later.",
            },
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

screen inventory_character_detail(character=None):

    modal True
    zorder 200

    if character:
        $ detail_accent = ELL_INVENTORY_TAB_COLORS["characters"]["accent"]
        $ detail_soft = ELL_INVENTORY_TAB_COLORS["characters"]["accent_soft"]

        add Solid("#020617dd")

        fixed:
            xfill True
            yfill True

            button:
                action Hide("inventory_character_detail")
                background "#00000000"
                hover_background "#00000000"
                xfill True
                yfill True

            frame:
                background "#08121eea"
                xpos 210
                ypos 90
                xsize 1500
                ysize 900
                xpadding 28
                ypadding 28

                fixed:
                    xfill True
                    yfill True

                    hbox:
                        xfill True
                        spacing 28

                        frame:
                            background "#101a28"
                            xsize 640
                            ysize 844
                            xpadding 0
                            ypadding 0

                            if renpy.loadable(character.get("portrait", "")):
                                add Transform(character["portrait"], xalign=0.5, yalign=1.0, xsize=620, ysize=820)
                            else:
                                add Transform("gui/window_icon.png", xalign=0.5, yalign=0.5, xsize=220, ysize=220)

                        vbox:
                            spacing 20
                            xsize 780

                            frame:
                                background "#140f26dd"
                                xfill True
                                ysize 74
                                xpadding 24
                                ypadding 12

                                hbox:
                                    xfill True
                                    text character["name"] style "inv_section_title"
                                    textbutton "X":
                                        action Hide("inventory_character_detail")
                                        background "#00000000"
                                        hover_background "#ffffff12"
                                        text_style "inv_section_title"
                                        text_color detail_accent
                                        xalign 1.0

                            frame:
                                background detail_soft
                                xfill True
                                xpadding 20
                                ypadding 14

                                vbox:
                                    spacing 6
                                    text "Personality" style "inv_body_text" color detail_accent
                                    text character.get("personality", "Unknown.") style "inv_muted_text"

                            frame:
                                background "#ffffff0a"
                                xfill True
                                xpadding 20
                                ypadding 14

                                vbox:
                                    spacing 6
                                    text "Description" style "inv_body_text" color detail_accent
                                    text character.get("description_long", character.get("desc", "")) style "inv_muted_text"

                            frame:
                                background detail_soft
                                xfill True
                                xpadding 20
                                ypadding 14

                                vbox:
                                    spacing 6
                                    text "Details" style "inv_body_text" color detail_accent
                                    text "Role: {}".format(character["role"]) style "inv_muted_text"
                                    text "Affinity: {}".format(character["affinity"]) style "inv_muted_text"

                            frame:
                                background "#ffffff0a"
                                xfill True
                                xpadding 20
                                ypadding 14

                                vbox:
                                    spacing 8
                                    text "Favorite Spots" style "inv_body_text" color detail_accent
                                    for spot in character.get("favorite_spots", []):
                                        text "• {}".format(spot) style "inv_muted_text"

                            frame:
                                background detail_soft
                                xfill True
                                xpadding 20
                                ypadding 14

                                vbox:
                                    spacing 6
                                    text "Storyline" style "inv_body_text" color detail_accent
                                    text character.get("storyline", "No details yet.") style "inv_muted_text"


screen inventory_menu():

    tag menu

    default inv_tab = "quests"
    default inv_scroll = ui.adjustment()
    default inv_inventory_scroll = ui.adjustment()
    default inv_collectible_id = "plushies"

    if "ell_sync_collectible_quests" in globals():
        on "show" action Function(ell_sync_collectible_quests)
    if "inventory" in globals():
        on "show" action Function(inventory.ensure_shape, 35, 7, False)

    $ bag_idle = "gui/Bag btn_720p.png"
    $ summary_rows = ell_inventory_summary_rows()
    $ tab_items = ell_inventory_tab_items(inv_tab)
    $ tab_label = next((t["label"] for t in ELL_INVENTORY_TABS if t["id"] == inv_tab), "Inventory")
    $ tab_colors = ELL_INVENTORY_TAB_COLORS.get(inv_tab, ELL_INVENTORY_TAB_COLORS["quests"])
    $ inventory_obj = getattr(store, "inventory", None)
    $ inventory_has_items = bool(inventory_obj and any(inventory_obj.get_items()))
    $ inventory_entry_count = (inventory_obj.total_item_count() if inventory_obj else 0)
    $ selected_collectible = next((c for c in ell_inventory_collectible_items() if c["id"] == inv_collectible_id), None)
    if selected_collectible is None and inv_tab == "collectibles":
        $ selected_collectible = ell_inventory_collectible_items()[0]
        $ inv_collectible_id = selected_collectible["id"]
    $ selected_collectible_status = selected_collectible["status"] if selected_collectible else "0/25 found"
    $ selected_collectible_previews = ell_collectible_preview_slots(selected_collectible["id"]) if selected_collectible else []
    $ selected_collectible_art_xsize = 372
    $ selected_collectible_art_ysize = 372
    $ selected_collectible_art_xpos = 1248
    $ selected_collectible_art_ypos = 408
    if selected_collectible and selected_collectible["id"] == "plushies":
        $ selected_collectible_art_xsize = 320
        $ selected_collectible_art_ysize = 480
    elif selected_collectible and selected_collectible["id"] == "picture_frames":
        $ selected_collectible_art_xsize = 320
        $ selected_collectible_art_ysize = 480

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
                            text _("{0} entries".format(inventory_entry_count if inv_tab == "inventory" else len(tab_items))) style "inv_body_text" color tab_colors["accent"]

                    if inv_tab == "inventory":
                        fixed:
                            xsize 1328
                            ysize 620
                            clipping True

                            if inventory_obj:
                                vbox:
                                    spacing 16
                                    xfill True

                                    frame:
                                        style "inv_card_frame"
                                        xfill True
                                        background tab_colors["accent_soft"]

                                        hbox:
                                            xfill True
                                            spacing 30

                                            vbox:
                                                spacing 4
                                                text _("Unlocked Slots") style "inv_label_text"
                                                text str(inventory_obj.unlocked_slots) style "inv_section_title"

                                            vbox:
                                                spacing 4
                                                text _("Total Slots") style "inv_label_text"
                                                text str(inventory_obj.slot_count) style "inv_section_title"

                                            vbox:
                                                spacing 4
                                                text _("Items Carried") style "inv_label_text"
                                                text str(inventory_obj.total_item_count()) style "inv_section_title"

                                            vbox:
                                                spacing 4
                                                text _("Max Stack") style "inv_label_text"
                                                text str(inventory_obj.max_items_per_slot) style "inv_section_title"

                                    vpgrid:
                                        cols 7
                                        spacing 3
                                        mousewheel True
                                        draggable True
                                        pagekeys True
                                        yadjustment inv_inventory_scroll
                                        scrollbars None
                                        xsize 1328
                                        ysize 500

                                        for slot in range(inventory_obj.slot_count):
                                            $ slot_data = inventory_obj.slots[slot]
                                            $ slot_unlocked = inventory_obj.is_slot_unlocked(slot)
                                            frame:
                                                background ("components/inventory_system/gui/slot_bg.png" if slot_unlocked else "components/inventory_system/gui/locked_slot_bg.png")
                                                xsize 176
                                                ysize 176
                                                xpadding 10
                                                ypadding 10

                                                if slot_unlocked and slot_data:
                                                    $ slot_item, slot_qty = list(slot_data.items())[0]
                                                    $ slot_icon = inventory_obj._icon_path(slot_item)
                                                    $ label_xpos = 60
                                                    if slot_item == "uniform_skirt":
                                                        $ label_xpos = 68
                                                    elif slot_item == "uniform_shoes":
                                                        $ label_xpos = 70
                                                    fixed:
                                                        xfill True
                                                        yfill True

                                                        if renpy.loadable(slot_icon):
                                                            add Transform(slot_icon, xsize=150, ysize=150, xpos=-10, ypos=-10)
                                                        else:
                                                            text inventory_obj._display_name(slot_item) style "inv_label_text":
                                                                xalign 0.5
                                                                ypos 38
                                                                text_align 0.5
                                                                xsize 140

                                                        text inventory_obj._display_name(slot_item) style "inv_label_text":
                                                            xpos label_xpos
                                                            xanchor 0.5
                                                            ypos 140
                                                            text_align 0.5
                                                            xsize 150
                                                elif slot_unlocked:
                                                    text _("Empty") style "inv_muted_text":
                                                        xalign 0.5
                                                        yalign 0.5
                                                else:
                                                    text _("Locked") style "inv_muted_text":
                                                        xalign 0.5
                                                        yalign 0.5

                            else:
                                frame:
                                    style "inv_card_frame"
                                    xfill True
                                    ysize 220
                                    background tab_colors["accent_soft"]

                                    vbox:
                                        spacing 10
                                        xalign 0.5
                                        yalign 0.5
                                        text _("Inventory system failed to initialize.") style "inv_section_title" color tab_colors["accent"] xalign 0.5
                                        text _("Check `inventory_core.rpy` for startup errors.") style "inv_muted_text" xalign 0.5

                    else:
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
                                            frame:
                                                style "inv_card_frame"
                                                xfill True
                                                ysize 620
                                                background tab_colors["accent_soft"]

                                                fixed:
                                                    xfill True
                                                    ysize 620

                                                    frame:
                                                        background "#0c1624aa"
                                                        xpos 16
                                                        ypos 16
                                                        xsize 1296
                                                        ysize 438
                                                        xpadding 18
                                                        ypadding 18

                                                        fixed:
                                                            xfill True
                                                            yfill True

                                                            vbox:
                                                                xpos 0
                                                                ypos 0
                                                                spacing 14
                                                                xsize 520

                                                                for c in tab_items:
                                                                    $ collectible_selected = (selected_collectible and selected_collectible["id"] == c["id"])
                                                                    button:
                                                                        style "inv_card_button"
                                                                        action SetScreenVariable("inv_collectible_id", c["id"])
                                                                        xsize 620
                                                                        ysize 126

                                                                        fixed:
                                                                            xsize 620
                                                                            ysize 126

                                                                            add Solid("#12303bcc" if collectible_selected else "#101726cc")
                                                                            add Solid(tab_colors["accent"] if collectible_selected else "#5e7684") xpos 0 ypos 0 xsize 6 ysize 126
                                                                            add Solid(tab_colors["accent"] if collectible_selected else "#314756") xpos 6 ypos 0 xsize 614 ysize 2
                                                                            add Solid(tab_colors["accent"] if collectible_selected else "#314756") xpos 6 ypos 124 xsize 614 ysize 2
                                                                            add Solid(tab_colors["accent"] if collectible_selected else "#314756") xpos 618 ypos 2 xsize 2 ysize 122

                                                                            frame:
                                                                                background "#111a28"
                                                                                xpos 18
                                                                                ypos 22
                                                                                xsize 74
                                                                                ysize 74
                                                                                xpadding 6
                                                                                ypadding 6

                                                                                if c["id"] == "plushies" and renpy.loadable("secrets/plushies/kittycat_plush.png"):
                                                                                    add Transform("secrets/plushies/kittycat_plush.png", xalign=0.5, yalign=0.5, xsize=58, ysize=58)
                                                                                elif c["id"] == "picture_frames" and renpy.loadable("secrets/Picture Frames/picture1.png"):
                                                                                    add Transform("secrets/Picture Frames/picture1.png", xalign=0.5, yalign=0.5, xsize=58, ysize=58)
                                                                                else:
                                                                                    add Transform("gui/window_icon.png", xalign=0.5, yalign=0.5, xsize=58, ysize=58)

                                                                            vbox:
                                                                                xpos 106
                                                                                ypos 14
                                                                                spacing 8
                                                                                xsize 320

                                                                                text c["title"] style "inv_section_title"
                                                                                text c["desc"] style "inv_muted_text" xmaximum 320

                                                                            text c["status"] style "inv_body_text" color tab_colors["accent"]:
                                                                                xpos 430
                                                                                ypos 44
                                                                                xsize 164
                                                                                text_align 1.0

                                                            if selected_collectible and renpy.loadable(selected_collectible["display_image"]):
                                                                add Transform(
                                                                    selected_collectible["display_image"],
                                                                    xanchor=1.0,
                                                                    yanchor=1.0,
                                                                    xpos=selected_collectible_art_xpos,
                                                                    ypos=selected_collectible_art_ypos,
                                                                    xsize=selected_collectible_art_xsize,
                                                                    ysize=selected_collectible_art_ysize
                                                                )

                                                    frame:
                                                        background "#0a1622c8"
                                                        xpos 16
                                                        ypos 474
                                                        xsize 1296
                                                        ysize 136
                                                        xpadding 18
                                                        ypadding 14

                                                        vbox:
                                                            spacing 10

                                                            text selected_collectible_status style "inv_body_text" color tab_colors["accent"] size 20

                                                            hbox:
                                                                spacing 12
                                                                for preview_path in selected_collectible_previews:
                                                                    fixed:
                                                                        xsize 108
                                                                        ysize 78

                                                                        add Solid("#06111bcc")
                                                                        add Solid(tab_colors["accent_soft"] if preview_path else "#ffffff10") xpos 0 ypos 0 xsize 108 ysize 2
                                                                        add Solid(tab_colors["accent_soft"] if preview_path else "#ffffff10") xpos 0 ypos 76 xsize 108 ysize 2
                                                                        add Solid(tab_colors["accent_soft"] if preview_path else "#ffffff10") xpos 0 ypos 0 xsize 2 ysize 78
                                                                        add Solid(tab_colors["accent_soft"] if preview_path else "#ffffff10") xpos 106 ypos 0 xsize 2 ysize 78

                                                                        if preview_path and renpy.loadable(preview_path):
                                                                            add Transform(preview_path, xalign=0.5, yalign=0.5, xsize=92, ysize=58)
                                                                        else:
                                                                            add Solid("#0f1b27") xpos 6 ypos 6 xsize 96 ysize 66
                                                                            text "?" style "inv_section_title" color "#7d8ca6":
                                                                                xalign 0.5
                                                                                yalign 0.5

                                        elif inv_tab == "characters":
                                            for ch in tab_items:
                                                button:
                                                    style "inv_card_button"
                                                    xfill True
                                                    action Show("inventory_character_detail", character=ch)

                                                    fixed:
                                                        xfill True
                                                        ysize 112

                                                        add Solid(tab_colors["accent_soft"])
                                                        add Solid(tab_colors["accent"]) xpos 0 ypos 0 xsize 8 ysize 112
                                                        add Solid(tab_colors["accent"]) xpos 8 ypos 0 ysize 3
                                                        add Solid(tab_colors["accent"]) xpos 8 ypos 109 ysize 3
                                                        add Solid(tab_colors["accent"]) xpos 8 ypos 3 xsize 3 ysize 106
                                                        add Solid(tab_colors["accent"]) xpos 1325 ypos 3 xsize 3 ysize 106

                                                        frame:
                                                            background tab_colors["accent_soft"]
                                                            xpos 22
                                                            ypos 10
                                                            xsize 90
                                                            ysize 90
                                                            xpadding 7
                                                            ypadding 7

                                                            if renpy.loadable(ch.get("portrait", "")):
                                                                add Transform(
                                                                    ch["portrait"],
                                                                    xalign=0.5,
                                                                    yalign=0.5,
                                                                    xsize=76,
                                                                    ysize=76
                                                                )
                                                            else:
                                                                add Transform(
                                                                    "gui/window_icon.png",
                                                                    xalign=0.5,
                                                                    yalign=0.5,
                                                                    xsize=64,
                                                                    ysize=64
                                                                )

                                                        vbox:
                                                            xpos 126
                                                            ypos 8
                                                            spacing 6
                                                            xsize 760

                                                            text ch["name"] style "inv_section_title"
                                                            text ch["desc"] style "inv_muted_text"

                                                        vbox:
                                                            xpos 930
                                                            ypos 18
                                                            spacing 6
                                                            xsize 220
                                                            text ch["role"] style "inv_body_text" color tab_colors["accent"] xalign 0.5
                                                            text ch["affinity"] style "inv_label_text" color tab_colors["accent"] xalign 0.5

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
                                                    text _("No Quests Yet") style "inv_section_title" color tab_colors["accent"] xalign 0.5
                                                    text _("Your adventure hasn't begun.") style "inv_body_text" xalign 0.5
                                                    text _("Explore the world to discover your first quest.") style "inv_muted_text" xalign 0.5
                                                elif inv_tab == "inventory":
                                                    text _("Inventory Empty") style "inv_section_title" color tab_colors["accent"] xalign 0.5
                                                    text _("You are not carrying anything yet.") style "inv_body_text" xalign 0.5
                                                    text _("Items you discover during exploration will appear here.") style "inv_muted_text" xalign 0.5
                                                elif inv_tab == "collectibles":
                                                    text _("No Collectibles Found") style "inv_section_title" color tab_colors["accent"] xalign 0.5
                                                    text _("The world is still hiding its secrets.") style "inv_body_text" xalign 0.5
                                                    text _("Rare finds and special discoveries will show up here.") style "inv_muted_text" xalign 0.5
                                                elif inv_tab == "characters":
                                                    text _("No Character Notes Yet") style "inv_section_title" color tab_colors["accent"] xalign 0.5
                                                    text _("You haven't filled out this section yet.") style "inv_body_text" xalign 0.5
                                                    text _("Important people you meet can be surfaced here over time.") style "inv_muted_text" xalign 0.5
                                                else:
                                                    text _("No Achievements Yet") style "inv_section_title" color tab_colors["accent"] xalign 0.5
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
