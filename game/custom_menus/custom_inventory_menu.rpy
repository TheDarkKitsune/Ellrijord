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
            "selected_bg": "#d5b1c6",
            "selected_text": "#5b3c18",
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
            "selected_bg": "#9fe8e4",
            "selected_text": "#0f4f52",
        },
        "characters": {
            "accent": "#ff7fb6",
            "accent_soft": "#ff7fb622",
            "selected_bg": "#ffd2e4",
            "selected_text": "#6d2244",
        },
    }

    ELL_CHARACTER_DETAIL_TABS = [
        ("overview", "Overview"),
        ("lore", "Lore"),
        ("relationships", "Relationships"),
        ("routine", "Routine / Locations"),
    ]

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
            ("Plushies Found", "{}/15".format(plushies_found)),
            ("Picture Frames", "{}/15".format(frames_found)),
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
                "kind": quest.get("kind", "side"),
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
                "kind": quest.get("kind", "side"),
                "progress": 100,
                "progress_text": "{}/{}".format(target, target),
                "desc": quest.get("description", ""),
                "giver": quest.get("giver", ""),
            })

        return out

    def ell_inventory_filter_quests(items, view_name):
        if view_name == "active":
            return [q for q in items if q.get("status") == "Active"]
        if view_name == "completed":
            return [q for q in items if q.get("status") == "Completed"]
        if view_name == "main":
            return [q for q in items if q.get("kind") == "story"]
        if view_name == "side":
            return [q for q in items if q.get("kind") != "story"]
        return items

    def ell_inventory_masked_divider(width, color="#d8b24f", height=5):
        return AlphaMask(
            Transform(Solid(color), xsize=width, ysize=height),
            Transform("gui/inventory_system/gui/inventory_divider_mask.png", xsize=width, ysize=height),
        )

    def ell_inventory_tab_shadow(width=96, height=52, color="#00000055", flip=False):
        return AlphaMask(
            Transform(Solid(color), xsize=width, ysize=height),
            Transform("gui/inventory_system/gui/inventory_tab_side_shadow_mask.png", xsize=width, ysize=height, xzoom=(-1 if flip else 1)),
        )

    def ell_inventory_fade_right(width, height, color):
        return AlphaMask(
            Transform(Solid(color), xsize=width, ysize=height),
            Transform("gui/inventory_system/gui/inventory_tab_side_shadow_mask.png", xsize=width, ysize=height),
        )

    def ell_inventory_tab_glow(width, color="#f4d892"):
        return Fixed(
            Transform(
                ell_inventory_masked_divider(width, color=color, height=5),
                alpha=0.9,
            ),
            Transform(
                ell_inventory_masked_divider(width + 28, color=color, height=9),
                xpos=-14,
                ypos=2,
                alpha=0.2,
            ),
            Transform(
                ell_inventory_masked_divider(width + 56, color=color, height=13),
                xpos=-28,
                ypos=5,
                alpha=0.1,
            ),
            xsize=width + 56,
            ysize=18,
        )

    def ell_inventory_achievement_items():
        out = []
        achievement_cls = getattr(renpy.store, "Achievement", None)
        if achievement_cls is None:
            return out

        for ach in achievement_cls.all_achievements:
            unlocked = ach.has()
            has_progress_bar = bool(ach.stat_max and ach.show_progress_bar)
            progress_raw = int(ach.stat_progress or 0) if ach.stat_max else 0
            has_progress = bool(ach.stat_max and progress_raw > 0)
            if unlocked:
                rarity = "Unlocked"
            elif has_progress:
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
                "badge_image": ach.idle_img,
                "rarity_tier": rarity_tier,
                "rarity": rarity,
                "rarity_color": "#f7e6b3" if unlocked else ("#edd0ff" if has_progress else "#d3bfd2"),
                "glow_top": (rarity_glow + "88") if unlocked else ((rarity_border + "66") if has_progress_bar else "#6d5e8a44"),
                "glow_bottom": (rarity_glow + "66") if unlocked else ((rarity_border + "50") if has_progress_bar else "#6d5e8a30"),
                "glow_side": (rarity_glow + "88") if unlocked else ((rarity_border + "66") if has_progress_bar else "#6d5e8a44"),
                "accent_strip": rarity_glow if unlocked else (rarity_border if has_progress_bar else "#5d5374"),
                "card_bg": "#5d33694c" if unlocked else ("#3b245b74" if has_progress else "#241d4358"),
                "badge_bg": "#3a1456" if unlocked else ("#2d1348" if has_progress else "#1a162c"),
                "border_color": (rarity_glow if unlocked else (rarity_border if has_progress else "#8d7b97")),
                "border_soft": (rarity_glow + "55") if unlocked else ((rarity_border + "44") if has_progress else "#c8b5cf24"),
                "status_text": ("{}/{}".format(progress_raw, int(ach.stat_max)) if has_progress else ("Unlocked" if unlocked else "Locked")),
                "status_icon": ("ÃƒÂ¢Ã…â€œÃ¢â‚¬Å“" if unlocked else "ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ¢â‚¬â„¢"),
                "desc": ach.description,
                "progress": progress,
                "progress_raw": progress_raw,
                "progress_max": int(ach.stat_max or 0),
                "show_progress_bar": has_progress_bar,
                "timestamp": ach.timestamp if unlocked else "",
            })

        return out

    def ell_inventory_collectible_items():
        plushies_found = set(getattr(renpy.store.persistent, "plushies_found", None) or [])
        picture_frames_found = set(getattr(renpy.store.persistent, "picture_frames_found", None) or [])
        paw_prints_found = set(getattr(renpy.store.persistent, "foxfire_paw_prints_found", None) or [])
        dream_fragments_found = set(getattr(renpy.store.persistent, "dream_fragments_found", None) or [])

        return [
            {
                "id": "plushies",
                "tab_label": "Plushies",
                "tab_icon": "🦊",
                "title": "Tsuki's Plushies",
                "type": "Collection",
                "found": len(plushies_found) > 0,
                "found_count": len(plushies_found),
                "total_count": 15,
                "status": "{}/15 found".format(len(plushies_found)),
                "desc": "Hidden plushies scattered through the story.",
                "display_image": "gui/inventory_system/collectibles/tsuki_plushies.png",
            },
            {
                "id": "picture_frames",
                "tab_label": "Frames",
                "tab_icon": "🖼",
                "title": "Picture Frames",
                "type": "Collection",
                "found": len(picture_frames_found) > 0,
                "found_count": len(picture_frames_found),
                "total_count": 15,
                "status": "{}/15 found".format(len(picture_frames_found)),
                "desc": "Secret picture frames tied to exploration.",
                "display_image": "gui/inventory_system/collectibles/picture_frames.png",
            },
            {
                "id": "foxfire_paw_prints",
                "tab_label": "Paw Prints",
                "tab_icon": "🐾",
                "title": "Foxfire Paw Prints",
                "type": "Collection",
                "found": len(paw_prints_found) > 0,
                "found_count": len(paw_prints_found),
                "total_count": 15,
                "status": "{}/15 found".format(len(paw_prints_found)),
                "desc": "These appear at night.",
                "display_image": "",
            },
            {
                "id": "dream_fragments",
                "tab_label": "Dreams",
                "tab_icon": "💎",
                "title": "Dream Fragments",
                "type": "Collection",
                "found": len(dream_fragments_found) > 0,
                "found_count": len(dream_fragments_found),
                "total_count": 15,
                "status": "{}/15 found".format(len(dream_fragments_found)),
                "desc": "Pieces of lost dreams from Ellrijord scattered around Midgard.",
                "display_image": "",
            },
            {
                "id": "mystic_relics",
                "tab_label": "Relics",
                "tab_icon": "🎭",
                "title": "Mystic Relics",
                "type": "Collection",
                "found": False,
                "found_count": 0,
                "total_count": 15,
                "status": "0/15 found",
                "desc": "Placeholder collectible entry for future content.",
                "display_image": "",
            },
        ]

    def ell_collectible_thumbnail_path(collectible_id, entry_id):
        plush_map = {
            "cat_plush_1": "secrets/plushies/kittycat_plush.png",
        }
        frame_map = {
            "picture1": "gui/inventory_system/collectibles/picture_frame1.png",
        }

        if collectible_id == "plushies":
            return plush_map.get(entry_id, None)
        if collectible_id == "picture_frames":
            return frame_map.get(entry_id, None)
        return None

    def ell_collectible_full_path(collectible_id, entry_id):
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

    def ell_collectible_icon_path(collectible_id):
        icon_map = {
            "plushies": "secrets/plushies/kittycat_plush.png",
            "picture_frames": "gui/inventory_system/collectibles/picture_frame1.png",
        }
        path = icon_map.get(collectible_id, None)
        if path and renpy.loadable(path):
            return path
        return None

    def ell_collectible_preview_slots(collectible_id, slot_count=7):
        if collectible_id == "plushies":
            found_ids = sorted(set(getattr(renpy.store.persistent, "plushies_found", set())))
        else:
            found_ids = sorted(set(getattr(renpy.store.persistent, "picture_frames_found", set())))

        previews = []

        for entry_id in found_ids[:slot_count]:
            previews.append({
                "thumbnail": ell_collectible_thumbnail_path(collectible_id, entry_id),
                "full": ell_collectible_full_path(collectible_id, entry_id),
            })

        while len(previews) < slot_count:
            previews.append(None)

        return previews

    def ell_inventory_character_portrait(*candidates):
        for candidate in candidates:
            if renpy.loadable(candidate):
                return candidate
        return pref_window_icon_path() if "pref_window_icon_path" in globals() else "gui/window_icon.png"

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
                "portrait": ell_inventory_character_portrait("gui/characters/Akari.png"),
                "accent": "#ff88d8",
                "accent_soft": "#ff88d824",
                "card_bg": "#3b1d4f4a",
                "card_bg_2": "#20163766",
                "frame_glow": "#ff9be2",
                "role_icon": "*",
                "affinity_icon": "o",
                "meta_icon": "-",
                "meta_left": "Year 3",
                "meta_right": "Route Lead",
                "subtitle": "The Quiet Light",
                "year": "3",
                "route_status": "Route Active",
                "traits": ["Determined", "Warm", "Observant", "Stubborn"],
                "personality": "Determined, warm, observant, quietly stubborn.",
                "description_long": "A calm and determined soul who guides the story with quiet strength.",
                "overview": "A calm and determined soul who guides the story with quiet strength. Akari carries the lighter emotional cadence of the route and keeps other people anchored when the world starts to lean toward the uncanny.",
                "lore": "Akari stands at the center of the Kuzunoha route and is closely tied to the more hopeful side of Ellrijord's mysteries. Her scenes usually frame trust, emotional warmth, and the idea that connection can be a force strong enough to push back against fear.",
                "relationships": [
                    {
                        "name": "Tsuki",
                        "role": "Younger Sister",
                        "summary": "Protective but teasing",
                        "hearts": 5,
                        "portrait": ell_inventory_character_portrait("game/Ellrijord Characters/Family/MC Family/Tsuki Kuzunoha.png", "Ellrijord Characters/Family/MC Family/Tsuki Kuzunoha.png"),
                    },
                    {
                        "name": "Hana",
                        "role": "Mother",
                        "summary": "Gentle support",
                        "hearts": 5,
                        "portrait": ell_inventory_character_portrait("game/Ellrijord Characters/Family/MC Family/Hana Kuzunoha.png", "Ellrijord Characters/Family/MC Family/Hana Kuzunoha.png"),
                    },
                    {
                        "name": "Rika",
                        "role": "Family / School Link",
                        "summary": "Growing trust",
                        "hearts": 4,
                        "portrait": ell_inventory_character_portrait("game/Ellrijord Characters/Year 2s/Rika Kuzunoha.png", "game/Ellrijord Characters/Family/Aunt-Cousins/Rika Kuzunoha.png", "Ellrijord Characters/Year 2s/Rika Kuzunoha.png"),
                    },
                ],
                "routine_locations": [
                    {"time": "Morning", "place": "Home bedroom"},
                    {"time": "After Classes", "place": "School grounds"},
                    {"time": "Evening", "place": "Family living room"},
                ],
                "favorite_spots": ["Home bedroom in the morning", "School grounds after classes"],
                "storyline": "Her route focuses on connection, trust, and the brighter side of Ellrijord's mysteries.",
                "default_tab": "relationships",
            },
            {
                "id": "kaito",
                "name": male_name,
                "role": "Protagonist",
                "affinity": "Void",
                "desc": "Male player route lead.",
                "portrait": ell_inventory_character_portrait("gui/characters/Kaito.png"),
                "accent": "#b57cff",
                "accent_soft": "#b57cff24",
                "card_bg": "#24184e4a",
                "card_bg_2": "#17123366",
                "frame_glow": "#ca99ff",
                "role_icon": "*",
                "affinity_icon": "o",
                "meta_icon": "-",
                "meta_left": "Year 3",
                "meta_right": "Route Lead",
                "subtitle": "The Quiet Shadow",
                "year": "3",
                "route_status": "Route Active",
                "traits": ["Dry", "Resilient", "Introspective", "Protective"],
                "personality": "Dry, resilient, introspective, quietly protective.",
                "description_long": "A stoic and mysterious figure who walks the path of shadows and questions.",
                "overview": "A stoic and mysterious figure who walks the path of shadows and questions. Kaito's route leans harder into suspicion, guarded emotion, and the unsettling edges of Ellrijord's hidden systems.",
                "lore": "Kaito is positioned closer to the stranger and more dangerous branches of the setting. His interactions tend to stress distance, survival, and the cost of understanding things that are easier to leave buried.",
                "relationships": [
                    {
                        "name": "Tsuki",
                        "role": "Younger Sister",
                        "summary": "Protective, sarcastic, dependable",
                        "hearts": 5,
                        "portrait": ell_inventory_character_portrait("game/Ellrijord Characters/Family/MC Family/Tsuki Kuzunoha.png", "Ellrijord Characters/Family/MC Family/Tsuki Kuzunoha.png"),
                    },
                    {
                        "name": "Hana",
                        "role": "Mother",
                        "summary": "Quiet care beneath the tension",
                        "hearts": 4,
                        "portrait": ell_inventory_character_portrait("game/Ellrijord Characters/Family/MC Family/Hana Kuzunoha.png", "Ellrijord Characters/Family/MC Family/Hana Kuzunoha.png"),
                    },
                    {
                        "name": "Rika",
                        "role": "School Connection",
                        "summary": "Measured trust and curiosity",
                        "hearts": 3,
                        "portrait": ell_inventory_character_portrait("game/Ellrijord Characters/Year 2s/Rika Kuzunoha.png", "game/Ellrijord Characters/Family/Aunt-Cousins/Rika Kuzunoha.png", "Ellrijord Characters/Year 2s/Rika Kuzunoha.png"),
                    },
                ],
                "routine_locations": [
                    {"time": "Morning", "place": "Home bedroom"},
                    {"time": "Late Afternoon", "place": "School rooftop edge"},
                    {"time": "Night", "place": "Any place tied to the unknown"},
                ],
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
                "accent": "#ffb14f",
                "accent_soft": "#ffb14f24",
                "card_bg": "#4f2b2a4a",
                "card_bg_2": "#2e1d2466",
                "frame_glow": "#ffc97a",
                "role_icon": "*",
                "affinity_icon": "o",
                "meta_icon": "-",
                "meta_left": "Year 1",
                "meta_right": "Family",
                "subtitle": "The Bright Spark",
                "year": "1",
                "route_status": "Always Present",
                "traits": ["Teasing", "Energetic", "Affectionate", "Honest"],
                "personality": "Teasing, energetic, affectionate, impossible to ignore.",
                "description_long": "Central to the plushie collection quest. Bright, energetic, and full of warmth.",
                "overview": "Bright, energetic, and impossible to ignore, Tsuki brings constant movement into scenes that might otherwise stay too quiet. She often acts like a pressure release valve for the heavier parts of the story.",
                "lore": "Tsuki sits close to the emotional center of the family dynamic and doubles as a recurring link to side discoveries like the plushie hunt. Even when the story turns serious, she keeps the world feeling lived in and personal.",
                "relationships": [
                    {
                        "name": female_name,
                        "role": "Older Sibling",
                        "summary": "Constant banter with real warmth",
                        "hearts": 5,
                        "portrait": ell_inventory_character_portrait("gui/characters/Akari.png"),
                    },
                    {
                        "name": "Hana",
                        "role": "Mother",
                        "summary": "Comfort and structure at home",
                        "hearts": 5,
                        "portrait": ell_inventory_character_portrait("game/Ellrijord Characters/Family/MC Family/Hana Kuzunoha.png", "Ellrijord Characters/Family/MC Family/Hana Kuzunoha.png"),
                    },
                    {
                        "name": male_name,
                        "role": "Older Sibling",
                        "summary": "Reliable even when distant",
                        "hearts": 4,
                        "portrait": ell_inventory_character_portrait("gui/characters/Kaito.png"),
                    },
                ],
                "routine_locations": [
                    {"time": "Before School", "place": "Home kitchen"},
                    {"time": "Afternoon", "place": "Shared family spaces"},
                    {"time": "Evening", "place": "Wherever attention is easiest to steal"},
                ],
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
                "accent": "#72c8ff",
                "accent_soft": "#72c8ff24",
                "card_bg": "#172c5a4a",
                "card_bg_2": "#131d3e66",
                "frame_glow": "#93d8ff",
                "role_icon": "*",
                "affinity_icon": "o",
                "meta_icon": "-",
                "meta_left": "Year 2",
                "meta_right": "School",
                "subtitle": "The Distant Echo",
                "year": "2",
                "route_status": "Side Presence",
                "traits": ["Reserved", "Observant", "Intriguing", "Guarded"],
                "personality": "Reserved, intriguing, hard to place at first glance.",
                "description_long": "Mentioned in the opening school route. Intelligent, reserved, and always observant.",
                "overview": "Rika reads like someone who notices more than she says. She enters the story with a deliberate distance that makes every small piece of trust feel important.",
                "lore": "She currently works best as a mystery-forward school connection. Rika's scenes imply wider family ties, careful judgment, and a role that will matter more once the story starts exposing deeper layers of Ellrijord.",
                "relationships": [
                    {
                        "name": female_name,
                        "role": "School Connection",
                        "summary": "Respect built through observation",
                        "hearts": 3,
                        "portrait": ell_inventory_character_portrait("gui/characters/Akari.png"),
                    },
                    {
                        "name": male_name,
                        "role": "School Connection",
                        "summary": "Tension mixed with curiosity",
                        "hearts": 3,
                        "portrait": ell_inventory_character_portrait("gui/characters/Kaito.png"),
                    },
                    {
                        "name": "Tsuki",
                        "role": "Family Link",
                        "summary": "Warmth that cuts through distance",
                        "hearts": 2,
                        "portrait": ell_inventory_character_portrait("game/Ellrijord Characters/Family/MC Family/Tsuki Kuzunoha.png", "Ellrijord Characters/Family/MC Family/Tsuki Kuzunoha.png"),
                    },
                ],
                "routine_locations": [
                    {"time": "Morning", "place": "School corridors"},
                    {"time": "After Classes", "place": "Quiet campus corners"},
                    {"time": "Late Day", "place": "Anywhere secrets start surfacing"},
                ],
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
    background "#07111d55"
    xpadding 28
    ypadding 28

style inv_sidebar_frame:
    background "#ffffff06"
    xpadding 18
    ypadding 18

style inv_main_frame is inv_sidebar_frame:
    background "#ffffff06"

style inv_tab_button:
    background "#00000000"
    hover_background "#ffffff10"
    xfill True
    ypadding 14
    xpadding 18

style inv_quest_mode_button is inv_tab_button:
    xfill False
    background "#00000033"
    hover_background "#0000004f"
    ysize 52

style inv_quest_mode_button_text is inv_body_text:
    size 18
    color "#d8d1ea"
    hover_color "#f5dfab"
    selected_color "#fff5da"

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
    background "#ffffff06"
    xpadding 22
    ypadding 18

style inv_card_frame_achievement:
    background "#ffffff06"
    xpadding 0
    ypadding 0

style inv_card_button:
    background "#ffffff06"
    hover_background "#ffffff0d"
    xpadding 0
    ypadding 0

style inv_char_display_name is text:
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
    size 42
    color "#f6e7d4"

style inv_char_card_name is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 24
    color "#f8ead7"
    textalign 0.5

style inv_char_card_meta is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 18
    color "#ead9ca"
    textalign 0.5

style inv_char_subtitle is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 24
    color "#dfc8d6"
    italic True

style inv_char_chip_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 18
    color "#fff4ea"

style inv_char_tab_text is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 18
    color "#d9c9dd"
    selected_color "#fff3eb"

style inv_char_small_label is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 16
    color "#e2bfd2"

style inv_char_small_body is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 16
    color "#efe6f4"

style inv_char_heart is text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 24
    color "#ff92ba"

screen inventory_character_detail(character=None):

    modal True
    zorder 200

    if character:
        default detail_tab = character.get("default_tab", "overview")
        default detail_relationship_page = 0

        $ detail_accent = character.get("frame_glow", ELL_INVENTORY_TAB_COLORS["characters"]["accent"])
        $ detail_soft = character.get("accent_soft", ELL_INVENTORY_TAB_COLORS["characters"]["accent_soft"])
        $ detail_name = character.get("name", "Unknown").upper()
        $ detail_subtitle = character.get("subtitle", character.get("desc", "Character Entry"))
        $ detail_traits = character.get("traits", []) or [t.strip().title() for t in character.get("personality", "").split(",") if t.strip()]
        $ detail_relationships = character.get("relationships", [])
        $ detail_routine = character.get("routine_locations", [])
        $ relation_page_size = 3
        $ relation_page_count = max(1, (len(detail_relationships) + relation_page_size - 1) // relation_page_size)
        $ relation_page = min(detail_relationship_page, relation_page_count - 1)
        $ visible_relationships = detail_relationships[relation_page * relation_page_size:(relation_page + 1) * relation_page_size]

        add Solid("#04030ddd")

        key "game_menu" action Hide("inventory_character_detail")
        key "dismiss" action Hide("inventory_character_detail")

        fixed:
            xfill True
            yfill True

            frame:
                background "#0d0a18f2"
                xalign 0.5
                yalign 0.5
                xsize 1680
                ysize 930
                xpadding 0
                ypadding 0

                fixed:
                    xfill True
                    yfill True

                    add Solid("#c49a74") xpos 0 ypos 0 xsize 1680 ysize 2
                    add Solid("#c49a74") xpos 0 ypos 928 xsize 1680 ysize 2
                    add Solid("#c49a74") xpos 0 ypos 0 xsize 2 ysize 930
                    add Solid("#c49a74") xpos 1678 ypos 0 xsize 2 ysize 930
                    add Transform("gui/inventory_system/gui/inventory_bg.png", xsize=1680, ysize=930, alpha=0.18)

                    hbox:
                        xpos 28
                        ypos 26
                        spacing 26

                        frame:
                            background "#1a1329ee"
                            xsize 690
                            ysize 878
                            xpadding 18
                            ypadding 18

                            fixed:
                                xfill True
                                yfill True

                                add Solid("#c49a74") xpos 0 ypos 0 xsize 654 ysize 2
                                add Solid("#c49a74") xpos 0 ypos 838 xsize 654 ysize 2
                                add Solid("#c49a74") xpos 0 ypos 0 xsize 2 ysize 840
                                add Solid("#c49a74") xpos 652 ypos 0 xsize 2 ysize 840
                                add Solid(character.get("card_bg", "#2a1d42")) xpos 2 ypos 2 xsize 650 ysize 836
                                add Solid("#ffffff08") xpos 24 ypos 24 xsize 606 ysize 652
                                add Solid(detail_soft) xpos 24 ypos 24 xsize 606 ysize 652

                                if renpy.loadable(character.get("portrait", "")):
                                    add Transform(character["portrait"], xalign=0.5, ypos=54, xsize=520, ysize=640, fit="contain", xoffset=-6, alpha=0.14, matrixcolor=TintMatrix(detail_accent))
                                    add Transform(character["portrait"], xalign=0.5, ypos=54, xsize=520, ysize=640, fit="contain", xoffset=6, alpha=0.14, matrixcolor=TintMatrix(detail_accent))
                                    add Transform(character["portrait"], xalign=0.5, ypos=54, xsize=520, ysize=640, fit="contain", yoffset=-6, alpha=0.14, matrixcolor=TintMatrix(detail_accent))
                                    add Transform(character["portrait"], xalign=0.5, ypos=54, xsize=520, ysize=640, fit="contain", yoffset=6, alpha=0.14, matrixcolor=TintMatrix(detail_accent))
                                    add Transform(character["portrait"], xalign=0.5, ypos=54, xsize=520, ysize=640, fit="contain")
                                else:
                                    add Transform(pref_window_icon_path(), xalign=0.5, ypos=210, xsize=240, ysize=240)

                                frame:
                                    background "#120d1ff0"
                                    xpos 22
                                    ypos 694
                                    xsize 610
                                    ysize 124
                                    xpadding 24
                                    ypadding 14

                                    vbox:
                                        xalign 0.5
                                        spacing 8
                                        text detail_name style "inv_char_card_name" size 26 xalign 0.5
                                        text "Role: {}   *   Affinity: {}   *   Year: {}".format(character.get("role", "Unknown"), character.get("affinity", "Unknown"), character.get("year", "?")) style "inv_char_card_meta" xalign 0.5
                                        text character.get("route_status", "Profile Active") style "inv_char_card_meta" color detail_accent xalign 0.5

                        fixed:
                            xsize 908
                            ysize 878

                            vbox:
                                xfill True
                                spacing 18

                                frame:
                                    background "#171028ee"
                                    xfill True
                                    xpadding 34
                                    ypadding 26

                                    vbox:
                                        spacing 6
                                        text detail_name style "inv_char_display_name"
                                        text detail_subtitle style "inv_char_subtitle"

                                hbox:
                                    spacing 14

                                    for idx, trait in enumerate(detail_traits[:4]):
                                        $ chip_colors = ["#7a5a3b", "#69507c", "#8a5475", "#8d6b31"]

                                        frame:
                                            background chip_colors[idx % len(chip_colors)] + "dd"
                                            xpadding 22
                                            ypadding 10

                                            text trait style "inv_char_chip_text"

                                frame:
                                    background "#171028cc"
                                    xfill True
                                    xpadding 0
                                    ypadding 0

                                    fixed:
                                        xfill True
                                        ysize 64

                                        hbox:
                                            xpos 18
                                            ypos 11
                                            spacing 8

                                            for tab_id, tab_label in ELL_CHARACTER_DETAIL_TABS:
                                                button:
                                                    action [SetScreenVariable("detail_tab", tab_id), SetScreenVariable("detail_relationship_page", 0)]
                                                    background ("#6b3f6fe8" if detail_tab == tab_id else "#21172fcc")
                                                    hover_background ("#7a4a7fde" if detail_tab == tab_id else "#2d203fcc")
                                                    xpadding 18
                                                    ypadding 10

                                                    text tab_label style "inv_char_tab_text" color ("#fff4e9" if detail_tab == tab_id else "#d9c9dd")

                                        add ell_inventory_masked_divider(872, color="#c49a74", height=4) xpos 18 ypos 58

                                frame:
                                    background "#161022d8"
                                    xfill True
                                    ysize 610
                                    xpadding 18
                                    ypadding 18

                                    if detail_tab == "overview":
                                        vbox:
                                            spacing 18

                                            frame:
                                                background "#ffffff08"
                                                xfill True
                                                xpadding 24
                                                ypadding 20

                                                vbox:
                                                    spacing 8
                                                    text "Overview" style "inv_section_title" color detail_accent
                                                    text character.get("overview", character.get("description_long", character.get("desc", ""))) style "inv_muted_text" color "#f1e8f6" size 20

                                            hbox:
                                                spacing 18

                                                frame:
                                                    background detail_soft
                                                    xsize 417
                                                    ysize 160
                                                    xpadding 22
                                                    ypadding 18

                                                    vbox:
                                                        spacing 8
                                                        text "Profile" style "inv_body_text" color detail_accent
                                                        text "Role: {}".format(character.get("role", "Unknown")) style "inv_muted_text" color "#f4e7f1" size 19
                                                        text "Affinity: {}".format(character.get("affinity", "Unknown")) style "inv_muted_text" color "#f4e7f1" size 19
                                                        text "Year: {}".format(character.get("year", "?")) style "inv_muted_text" color "#f4e7f1" size 19

                                                frame:
                                                    background "#ffffff08"
                                                    xsize 417
                                                    ysize 160
                                                    xpadding 22
                                                    ypadding 18

                                                    vbox:
                                                        spacing 8
                                                        text "Current Status" style "inv_body_text" color detail_accent
                                                        text character.get("route_status", "Profile Active") style "inv_muted_text" color "#f4e7f1" size 19
                                                        text character.get("personality", "Unknown.") style "inv_muted_text" color "#d9cddf" size 18

                                            frame:
                                                background "#ffffff08"
                                                xfill True
                                                xpadding 24
                                                ypadding 20

                                                vbox:
                                                    spacing 8
                                                    text "Storyline" style "inv_body_text" color detail_accent
                                                    text character.get("storyline", "No details yet.") style "inv_muted_text" color "#f1e8f6" size 20

                                    elif detail_tab == "lore":
                                        vbox:
                                            spacing 18

                                            frame:
                                                background "#ffffff08"
                                                xfill True
                                                xpadding 24
                                                ypadding 20

                                                vbox:
                                                    spacing 8
                                                    text "Lore" style "inv_section_title" color detail_accent
                                                    text character.get("lore", character.get("storyline", "No lore written yet.")) style "inv_muted_text" color "#f1e8f6" size 20

                                            frame:
                                                background detail_soft
                                                xfill True
                                                xpadding 24
                                                ypadding 20

                                                vbox:
                                                    spacing 8
                                                    text "Favorite Spots" style "inv_body_text" color detail_accent
                                                    for spot in character.get("favorite_spots", []):
                                                        text spot style "inv_muted_text" color "#f1e8f6" size 19

                                            frame:
                                                background "#ffffff08"
                                                xfill True
                                                xpadding 24
                                                ypadding 20

                                                vbox:
                                                    spacing 8
                                                    text "Route Notes" style "inv_body_text" color detail_accent
                                                    text character.get("description_long", character.get("desc", "")) style "inv_muted_text" color "#f1e8f6" size 20

                                    elif detail_tab == "relationships":
                                        if visible_relationships:
                                            vbox:
                                                spacing 14

                                                for rel in visible_relationships:
                                                    frame:
                                                        background "#211631d8"
                                                        xfill True
                                                        ysize 154
                                                        xpadding 16
                                                        ypadding 12

                                                        fixed:
                                                            xfill True
                                                            yfill True

                                                            add Solid("#c49a74") xpos 0 ypos 0 xsize 840 ysize 2
                                                            add Solid("#c49a74") xpos 0 ypos 128 xsize 840 ysize 2
                                                            add Solid("#c49a74") xpos 0 ypos 0 xsize 2 ysize 130
                                                            add Solid("#c49a74") xpos 838 ypos 0 xsize 2 ysize 130

                                                            hbox:
                                                                xpos 14
                                                                ypos 12
                                                                spacing 16

                                                                frame:
                                                                    background "#ffffff08"
                                                                    xsize 128
                                                                    ysize 106
                                                                    xpadding 0
                                                                    ypadding 0

                                                                    if renpy.loadable(rel.get("portrait", "")):
                                                                        add Transform(rel["portrait"], xalign=0.5, yalign=1.0, xsize=122, ysize=102, fit="contain")
                                                                    else:
                                                                        add Transform(pref_window_icon_path(), xalign=0.5, yalign=0.5, xsize=64, ysize=64)

                                                                fixed:
                                                                    xsize 664
                                                                    ysize 108

                                                                    vbox:
                                                                        spacing 6
                                                                        text rel.get("name", "Unknown") style "inv_section_title" color "#f6e2d0" size 24
                                                                        text rel.get("role", "Connection") style "inv_muted_text" color "#cfbdd0" size 18
                                                                        text rel.get("summary", "No relationship notes yet.") style "inv_muted_text" color "#f3e9f5" size 18

                                                                    hbox:
                                                                        xpos 474
                                                                        ypos 0
                                                                        spacing 3

                                                                        for heart_idx in range(5):
                                                                            text "♥" style "inv_char_heart" color ("#ff92ba" if heart_idx < rel.get("hearts", 0) else "#7e647b")

                                                                    add ell_inventory_masked_divider(214, color="#8d6679", height=3) xpos 448 ypos 36

                                                hbox:
                                                    xalign 0.5
                                                    spacing 18

                                                    textbutton "<":
                                                        action SetScreenVariable("detail_relationship_page", max(0, relation_page - 1))
                                                        sensitive relation_page > 0
                                                        background "#00000000"
                                                        hover_background "#ffffff12"
                                                        text_style "inv_body_text"
                                                        text_color "#d8bfd0"

                                                    hbox:
                                                        spacing 10
                                                        for page_idx in range(relation_page_count):
                                                            text ("●" if page_idx == relation_page else "•") style "inv_char_small_body" color ("#f0cfe1" if page_idx == relation_page else "#7f6b82")

                                                    textbutton ">":
                                                        action SetScreenVariable("detail_relationship_page", min(relation_page_count - 1, relation_page + 1))
                                                        sensitive relation_page < (relation_page_count - 1)
                                                        background "#00000000"
                                                        hover_background "#ffffff12"
                                                        text_style "inv_body_text"
                                                        text_color "#d8bfd0"
                                        else:
                                            vbox:
                                                xfill True
                                                yfill True
                                                spacing 12
                                                xalign 0.5
                                                yalign 0.5
                                                text "No Relationship Entries Yet" style "inv_section_title" color detail_accent xalign 0.5
                                                text "Relationship notes will appear here once this character is documented further." style "inv_muted_text" color "#d8cddb" size 20 xalign 0.5

                                    else:
                                        vbox:
                                            spacing 16

                                            for stop_idx, stop in enumerate(detail_routine):
                                                frame:
                                                    background ("#ffffff08" if (stop_idx % 2 == 0) else detail_soft)
                                                    xfill True
                                                    ysize 120
                                                    xpadding 24
                                                    ypadding 18

                                                    hbox:
                                                        spacing 20
                                                        xfill True

                                                        text stop.get("time", "Any Time") style "inv_section_title" color detail_accent size 24 xsize 220
                                                        text stop.get("place", "Unknown Location") style "inv_muted_text" color "#f2e9f5" size 20 xmaximum 560

                                            if not detail_routine:
                                                text "No routine or location notes yet." style "inv_muted_text" color "#d8cddb" size 20

                                hbox:
                                    xalign 0.5
                                    spacing 20

                                    use ui_png_button(_("Back"), Hide("inventory_character_detail"), xsize=290, ysize=62, text_style="ui_btn_text_small")


screen inventory_menu():

    tag menu

    default inv_tab = "quests"
    default inv_quest_view = "active"
    default inv_scroll = ui.adjustment()
    default inv_inventory_scroll = ui.adjustment()
    default inv_collectible_id = None
    default inv_side_tab_hovered = False
    default inv_collectible_last_tab_hovered = False

    if "ell_sync_collectible_quests" in globals():
        on "show" action Function(ell_sync_collectible_quests)
    if "inventory" in globals():
        on "show" action Function(inventory.ensure_shape, 28, 7, False)

    $ bag_idle = "gui/hud/Player_male_btn.png" if getattr(store, "mc_gender", "male") == "male" else "gui/hud/Player_female_btn.png"
    $ summary_rows = ell_inventory_summary_rows()
    $ tab_items = ell_inventory_tab_items(inv_tab)
    $ quest_view_items = ell_inventory_filter_quests(tab_items, inv_quest_view) if inv_tab == "quests" else []
    $ tab_label = next((t["label"] for t in ELL_INVENTORY_TABS if t["id"] == inv_tab), "Inventory")
    $ tab_header_label = next((t["id"].replace("_", " ").title() for t in ELL_INVENTORY_TABS if t["id"] == inv_tab), "Inventory")
    $ tab_colors = ELL_INVENTORY_TAB_COLORS.get(inv_tab, ELL_INVENTORY_TAB_COLORS["quests"])
    $ inv_content_height = 727
    $ inventory_obj = getattr(store, "inventory", None)
    $ inventory_has_items = bool(inventory_obj and any(inventory_obj.get_items()))
    $ inventory_entry_count = (inventory_obj.total_item_count() if inventory_obj else 0)
    $ selected_collectible = next((c for c in ell_inventory_collectible_items() if c["id"] == inv_collectible_id), None)
    $ current_collectible = (selected_collectible if selected_collectible else (tab_items[0] if (inv_tab == "collectibles" and tab_items) else None))
    $ featured_character = next((c for c in tab_items if c.get("id") == "tsuki"), (tab_items[-1] if (inv_tab == "characters" and tab_items) else None))
    $ selected_collectible_status = current_collectible["status"] if current_collectible else ""
    $ selected_collectible_previews = ell_collectible_preview_slots(current_collectible["id"], 15) if current_collectible else []
    $ selected_collectible_art_xsize = 300
    $ selected_collectible_art_ysize = 420
    $ selected_collectible_art_xpos = 1288
    $ selected_collectible_art_ypos = 650
    if current_collectible and current_collectible["id"] == "plushies":
        $ selected_collectible_art_xsize = 335
        $ selected_collectible_art_ysize = 500
        $ selected_collectible_art_xpos = 1330
        $ selected_collectible_art_ypos = 636
    elif current_collectible and current_collectible["id"] == "picture_frames":
        $ selected_collectible_art_xsize = 335
        $ selected_collectible_art_ysize = 500
        $ selected_collectible_art_xpos = 1330
        $ selected_collectible_art_ypos = 636
    elif current_collectible and current_collectible["id"] == "foxfire_paw_prints":
        $ selected_collectible_art_xsize = 335
        $ selected_collectible_art_ysize = 500
        $ selected_collectible_art_xpos = 1330
        $ selected_collectible_art_ypos = 636
    elif current_collectible and current_collectible["id"] == "dream_fragments":
        $ selected_collectible_art_xsize = 335
        $ selected_collectible_art_ysize = 500
        $ selected_collectible_art_xpos = 1330
        $ selected_collectible_art_ypos = 636

    add Transform("gui/inventory_system/gui/inventory_bg.png", xsize=config.screen_width, ysize=config.screen_height)
    add Solid("#02061704")
    add Solid("#8f6dff10")

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
                        add Transform(bag_idle, xsize=110, ysize=110)
                        vbox:
                            spacing 2
                            text _("Player Hub") style "inv_section_title"
                            text _("Your in-game systems menu.") style "inv_label_text"

                    null height 8

                    for tab in ELL_INVENTORY_TABS:
                        $ sidebar_tab_colors = ELL_INVENTORY_TAB_COLORS.get(tab["id"], tab_colors)
                        textbutton _(tab["label"]):
                            style "inv_tab_button"
                            text_style "inv_tab_button_text"
                            action (
                                [SetScreenVariable("inv_tab", tab["id"]), SetScreenVariable("inv_quest_view", "active"), SetScreenVariable("inv_collectible_id", None)]
                                if tab["id"] == "quests"
                                else [SetScreenVariable("inv_tab", tab["id"]), SetScreenVariable("inv_collectible_id", None)]
                                if tab["id"] == "collectibles"
                                else SetScreenVariable("inv_tab", tab["id"])
                            )
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

                        frame:
                            background "#241d4358"
                            xfill True
                            ysize 120
                            xpadding 18
                            ypadding 14

                            vbox:
                                spacing 5
                                text _(tab_header_label) style "inv_title" color tab_colors["accent"]
                                if inv_tab == "quests":
                                    text _("Active and completed story progress.") style "inv_subtitle"
                                elif inv_tab == "achievements":
                                    text _("Unlocked milestones and hidden rewards.") style "inv_subtitle"
                                elif inv_tab == "collectibles":
                                    text _("Exploration progress and secret finds.") style "inv_subtitle"
                                elif inv_tab == "characters":
                                    text _("Key cast members currently surfaced by the story.") style "inv_subtitle"
                                else:
                                    text _("Tracked items and future pickups.") style "inv_subtitle"

                    if inv_tab == "inventory":
                        fixed:
                            xsize 1328
                            clipping True

                            if inventory_obj:
                                vbox:
                                    spacing 16
                                    xfill True

                                    frame:
                                        style "inv_card_frame"
                                        xfill True
                                        background tab_colors["accent_soft"][:-2] + "18"

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
                                        cols 8
                                        xspacing 5
                                        yspacing 45
                                        mousewheel True
                                        draggable True
                                        pagekeys True
                                        yadjustment inv_inventory_scroll
                                        scrollbars None
                                        xsize 1328
                                        ysize 620

                                        for slot in range(inventory_obj.slot_count):
                                            $ slot_data = inventory_obj.slots[slot]
                                            $ slot_unlocked = inventory_obj.is_slot_unlocked(slot)
                                            frame:
                                                background ("gui/inventory_system/gui/slot_bg.png" if slot_unlocked else "gui/inventory_system/gui/locked_slot_bg.png")
                                                xsize 163
                                                ysize 163
                                                xpadding 10
                                                ypadding 10

                                                if slot_unlocked and slot_data:
                                                    $ slot_item, slot_qty = list(slot_data.items())[0]
                                                    $ slot_icon = inventory_obj._icon_path(slot_item)
                                                    fixed:
                                                        xfill True
                                                        yfill True

                                                        if renpy.loadable(slot_icon):
                                                            add Transform(slot_icon, xsize=125, ysize=125)
                                                        else:
                                                            text inventory_obj._display_name(slot_item) style "inv_muted_text":
                                                                xalign 0.5
                                                                text_align 0.5
                                                                ypos 140

                                                        text inventory_obj._display_name(slot_item) style "inv_muted_text":
                                                            xalign 0.5
                                                            text_align 0.5
                                                            ypos 140

                                                elif slot_unlocked:
                                                    text _("Empty") style "inv_muted_text":
                                                        text_align 0.5
                                                        xalign 0.5
                                                        ypos 140
                                                else:
                                                    text _("Locked") style "inv_muted_text":
                                                        text_align 0.5
                                                        xalign 0.5
                                                        ypos 140

                            else:
                                frame:
                                    style "inv_card_frame"
                                    xfill True
                                    ysize 220
                                    background tab_colors["accent_soft"][:-2] + "18"

                                    vbox:
                                        spacing 10
                                        xalign 0.5
                                        yalign 0.5
                                        text _("Inventory system failed to initialize.") style "inv_section_title" color tab_colors["accent"] xalign 0.5
                                        text _("Check `inventory_core.rpy` for startup errors.") style "inv_muted_text" xalign 0.5

                    else:
                        fixed:
                            xsize 1328
                            ysize inv_content_height
                            clipping True

                            vbox:
                                spacing 0
                                xfill True

                                if inv_tab == "quests":
                                    frame:
                                        background "#241d435e"
                                        xfill True
                                        ysize 52
                                        xpadding 0
                                        ypadding 0

                                        hbox:
                                            spacing 0

                                            textbutton _("Active Quests"):
                                                style "inv_quest_mode_button"
                                                text_style "inv_body_text"
                                                action SetScreenVariable("inv_quest_view", "active")
                                                selected (inv_quest_view == "active")
                                                xsize 220
                                                selected_background "#6e587f88"
                                                text_selected_color "#f4d892"
                                                text_hover_color "#f4d892"

                                            textbutton _("Completed Quests"):
                                                style "inv_quest_mode_button"
                                                text_style "inv_body_text"
                                                action SetScreenVariable("inv_quest_view", "completed")
                                                selected (inv_quest_view == "completed")
                                                xsize 280
                                                selected_background "#6e587f88"
                                                text_selected_color "#f4d892"
                                                text_hover_color "#f4d892"

                                            textbutton _("Main Quests"):
                                                style "inv_quest_mode_button"
                                                text_style "inv_body_text"
                                                action SetScreenVariable("inv_quest_view", "main")
                                                selected (inv_quest_view == "main")
                                                xsize 210
                                                selected_background "#6e587f88"
                                                text_selected_color "#f4d892"
                                                text_hover_color "#f4d892"

                                            textbutton _("Side Quests"):
                                                style "inv_quest_mode_button"
                                                text_style "inv_body_text"
                                                action SetScreenVariable("inv_quest_view", "side")
                                                hovered SetScreenVariable("inv_side_tab_hovered", True)
                                                unhovered SetScreenVariable("inv_side_tab_hovered", False)
                                                selected (inv_quest_view == "side")
                                                xsize 206
                                                selected_background "#6e587f88"
                                                text_selected_color "#f4d892"
                                                text_hover_color "#f4d892"

                                        fixed:
                                            xsize 1328
                                            ysize 52

                                            add ell_inventory_fade_right(96, 52, ("#6e587f88" if inv_quest_view == "side" else ("#0000004f" if inv_side_tab_hovered else "#00000033"))):
                                                xpos 916
                                                ypos 0

                                            if inv_quest_view == "active":
                                                add ell_inventory_tab_shadow():
                                                    xpos 220
                                                    ypos 0
                                            elif inv_quest_view == "completed":
                                                add ell_inventory_tab_shadow():
                                                    xpos 500
                                                    ypos 0
                                                add ell_inventory_tab_shadow(flip=True):
                                                    xpos 124
                                                    ypos 0
                                            elif inv_quest_view == "main":
                                                add ell_inventory_tab_shadow():
                                                    xpos 710
                                                    ypos 0
                                                add ell_inventory_tab_shadow(flip=True):
                                                    xpos 404
                                                    ypos 0
                                            else:
                                                add ell_inventory_tab_shadow(flip=True):
                                                    xpos 614
                                                    ypos 0

                                    fixed:
                                        xsize 1328
                                        ysize 5

                                        add Solid(tab_colors["accent_soft"]):
                                            xsize 916
                                            ysize 5

                                        add ell_inventory_fade_right(96, 5, tab_colors["accent_soft"]):
                                            xpos 916
                                            ypos 0

                                        if inv_quest_view == "active":
                                            add ell_inventory_masked_divider(220):
                                                xpos 0
                                                ypos 0
                                        elif inv_quest_view == "completed":
                                            add ell_inventory_masked_divider(280):
                                                xpos 220
                                                ypos 0
                                        elif inv_quest_view == "main":
                                            add ell_inventory_masked_divider(210):
                                                xpos 500
                                                ypos 0
                                        else:
                                            add ell_inventory_masked_divider(206):
                                                xpos 710
                                                ypos 0

                                viewport:
                                    mousewheel True
                                    draggable True
                                    pagekeys True
                                    yadjustment inv_scroll
                                    scrollbars None
                                    xsize 1328
                                    ysize (inv_content_height - 60 if inv_tab == "quests" else inv_content_height)

                                    vbox:
                                        spacing 0

                                        if not tab_items and inv_tab != "quests":
                                            frame:
                                                style "inv_card_frame"
                                                xfill True
                                                ysize 260
                                                background tab_colors["accent_soft"][:-2] + "16"

                                                vbox:
                                                    spacing 14
                                                    xalign 0.5
                                                    yalign 0.5
                                                    if inv_tab == "inventory":
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

                                        elif inv_tab == "quests":
                                                frame:
                                                    background "#241d435e"
                                                    xfill True
                                                    ysize 690
                                                    xpadding 24
                                                    ypadding 24

                                                    if quest_view_items:
                                                        vbox:
                                                            spacing 14

                                                            for q in quest_view_items:
                                                                frame:
                                                                    background "#ffffff08"
                                                                    xfill True
                                                                    xpadding 18
                                                                    ypadding 14

                                                                    vbox:
                                                                        spacing 8

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
                                                    else:
                                                        vbox:
                                                            spacing 14
                                                            xalign 0.5
                                                            yalign 0.28

                                                            if inv_quest_view == "active":
                                                                text _("No Active Quests") style "inv_section_title" color "#d8cbe8" xalign 0.5
                                                                text _("New quests will appear here as you progress through the story.") style "inv_muted_text" xalign 0.5
                                                            elif inv_quest_view == "completed":
                                                                text _("No Completed Quests") style "inv_section_title" color "#d8cbe8" xalign 0.5
                                                                text _("Completed quests will be archived here.") style "inv_muted_text" xalign 0.5
                                                            elif inv_quest_view == "main":
                                                                text _("No Main Quests") style "inv_section_title" color "#d8cbe8" xalign 0.5
                                                                text _("Main story quests will appear here.") style "inv_muted_text" xalign 0.5
                                                            else:
                                                                text _("No Side Quests") style "inv_section_title" color "#d8cbe8" xalign 0.5
                                                                text _("Optional quests and collections will appear here.") style "inv_muted_text" xalign 0.5

                                        elif inv_tab == "achievements":
                                            vbox:
                                                spacing 20

                                                for a in tab_items:
                                                    frame:
                                                        style "inv_card_frame_achievement"
                                                        xfill True
                                                        background (a["card_bg"][:-2] + "52")

                                                        fixed:
                                                            xfill True
                                                            ysize 110

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
                                            fixed:
                                                xfill True
                                                ysize 690

                                                $ overall_found = sum(c["found_count"] for c in tab_items)
                                                $ overall_total = sum(c["total_count"] for c in tab_items)
                                                $ overall_progress_width = int((566 * overall_found) / max(1, overall_total))
                                                $ collectible_tab_glow_soft = ELL_INVENTORY_TAB_COLORS["quests"]["accent_soft"]

                                                frame:
                                                    background "#241d435e"
                                                    xfill True
                                                    ysize 52
                                                    xpadding 0
                                                    ypadding 0

                                                    hbox:
                                                        spacing 0

                                                        textbutton _("{} {}".format(tab_items[0].get("tab_icon", ""), tab_items[0].get("tab_label", tab_items[0]["title"])).strip()):
                                                            style "inv_quest_mode_button"
                                                            text_style "inv_body_text"
                                                            action SetScreenVariable("inv_collectible_id", tab_items[0]["id"])
                                                            selected (current_collectible and current_collectible["id"] == tab_items[0]["id"])
                                                            xsize 180
                                                            selected_background "#6e587f88"
                                                            text_selected_color "#f4d892"
                                                            text_hover_color "#f4d892"

                                                        textbutton _("{} {}".format(tab_items[1].get("tab_icon", ""), tab_items[1].get("tab_label", tab_items[1]["title"])).strip()):
                                                            style "inv_quest_mode_button"
                                                            text_style "inv_body_text"
                                                            action SetScreenVariable("inv_collectible_id", tab_items[1]["id"])
                                                            selected (current_collectible and current_collectible["id"] == tab_items[1]["id"])
                                                            xsize 170
                                                            selected_background "#6e587f88"
                                                            text_selected_color "#f4d892"
                                                            text_hover_color "#f4d892"

                                                        textbutton _("{} {}".format(tab_items[2].get("tab_icon", ""), tab_items[2].get("tab_label", tab_items[2]["title"])).strip()):
                                                            style "inv_quest_mode_button"
                                                            text_style "inv_body_text"
                                                            action SetScreenVariable("inv_collectible_id", tab_items[2]["id"])
                                                            selected (current_collectible and current_collectible["id"] == tab_items[2]["id"])
                                                            xsize 200
                                                            selected_background "#6e587f88"
                                                            text_selected_color "#f4d892"
                                                            text_hover_color "#f4d892"

                                                        textbutton _("{} {}".format(tab_items[3].get("tab_icon", ""), tab_items[3].get("tab_label", tab_items[3]["title"])).strip()):
                                                            style "inv_quest_mode_button"
                                                            text_style "inv_body_text"
                                                            action SetScreenVariable("inv_collectible_id", tab_items[3]["id"])
                                                            selected (current_collectible and current_collectible["id"] == tab_items[3]["id"])
                                                            xsize 170
                                                            selected_background "#6e587f88"
                                                            text_selected_color "#f4d892"
                                                            text_hover_color "#f4d892"

                                                        textbutton _("{} {}".format(tab_items[4].get("tab_icon", ""), tab_items[4].get("tab_label", tab_items[4]["title"])).strip()):
                                                            style "inv_quest_mode_button"
                                                            text_style "inv_body_text"
                                                            action SetScreenVariable("inv_collectible_id", tab_items[4]["id"])
                                                            hovered SetScreenVariable("inv_collectible_last_tab_hovered", True)
                                                            unhovered SetScreenVariable("inv_collectible_last_tab_hovered", False)
                                                            selected (current_collectible and current_collectible["id"] == tab_items[4]["id"])
                                                            xsize 196
                                                            selected_background "#6e587f88"
                                                            text_selected_color "#f4d892"
                                                            text_hover_color "#f4d892"

                                                fixed:
                                                    xsize 1328
                                                    ysize 52

                                                    add ell_inventory_fade_right(96, 52, ("#6e587f88" if (current_collectible and current_collectible["id"] == tab_items[4]["id"]) else ("#0000004f" if inv_collectible_last_tab_hovered else "#00000033"))):
                                                        xpos 916
                                                        ypos 0

                                                    if current_collectible and current_collectible["id"] == tab_items[0]["id"]:
                                                        add ell_inventory_tab_shadow():
                                                            xpos 180
                                                            ypos 0
                                                    elif current_collectible and current_collectible["id"] == tab_items[1]["id"]:
                                                        add ell_inventory_tab_shadow():
                                                            xpos 350
                                                            ypos 0
                                                        add ell_inventory_tab_shadow(flip=True):
                                                            xpos 84
                                                            ypos 0
                                                    elif current_collectible and current_collectible["id"] == tab_items[2]["id"]:
                                                        add ell_inventory_tab_shadow():
                                                            xpos 550
                                                            ypos 0
                                                        add ell_inventory_tab_shadow(flip=True):
                                                            xpos 254
                                                            ypos 0
                                                    elif current_collectible and current_collectible["id"] == tab_items[3]["id"]:
                                                        add ell_inventory_tab_shadow():
                                                            xpos 720
                                                            ypos 0
                                                        add ell_inventory_tab_shadow(flip=True):
                                                            xpos 454
                                                            ypos 0
                                                    elif current_collectible and current_collectible["id"] == tab_items[4]["id"]:
                                                        add ell_inventory_tab_shadow(flip=True):
                                                            xpos 624
                                                            ypos 0

                                                fixed:
                                                    xsize 1328
                                                    ysize 5
                                                    ypos 52

                                                    add Solid(collectible_tab_glow_soft):
                                                        xsize 916
                                                        ysize 5

                                                    add ell_inventory_fade_right(96, 5, collectible_tab_glow_soft):
                                                        xpos 916
                                                        ypos 0

                                                    if current_collectible and current_collectible["id"] == tab_items[0]["id"]:
                                                        add ell_inventory_masked_divider(180):
                                                            xpos 0
                                                            ypos 0
                                                    elif current_collectible and current_collectible["id"] == tab_items[1]["id"]:
                                                        add ell_inventory_masked_divider(170):
                                                            xpos 180
                                                            ypos 0
                                                    elif current_collectible and current_collectible["id"] == tab_items[2]["id"]:
                                                        add ell_inventory_masked_divider(200):
                                                            xpos 350
                                                            ypos 0
                                                    elif current_collectible and current_collectible["id"] == tab_items[3]["id"]:
                                                        add ell_inventory_masked_divider(170):
                                                            xpos 550
                                                            ypos 0
                                                    elif current_collectible and current_collectible["id"] == tab_items[4]["id"]:
                                                        add ell_inventory_masked_divider(196):
                                                            xpos 720
                                                            ypos 0

                                                frame:
                                                    background "#103a3f5e"
                                                    xpos 0
                                                    ypos 0
                                                    xfill True
                                                    ysize 654 + 86
                                                    xpadding 24
                                                    ypadding 24

                                                    fixed:
                                                        xfill True
                                                        yfill True

                                                        if current_collectible:
                                                            button:
                                                                style "inv_card_button"
                                                                action NullAction()
                                                                xpos 154
                                                                ypos 40
                                                                xsize 860
                                                                ysize 168

                                                                fixed:
                                                                    xsize 860
                                                                    ysize 168

                                                                    $ featured_icon_path = ell_collectible_icon_path(current_collectible["id"])
                                                                    $ featured_icon_fallback = current_collectible.get("tab_icon", "?")

                                                                    add Solid("#4a2c3e70")
                                                                    add Solid("#ffca63") xpos 0 ypos 0 xsize 860 ysize 2
                                                                    add Solid("#ffca63") xpos 0 ypos 166 xsize 860 ysize 2
                                                                    add Solid("#ffca63") xpos 0 ypos 0 xsize 2 ysize 168
                                                                    add Solid("#ffca63") xpos 858 ypos 0 xsize 2 ysize 168
                                                                    add Solid("#fff2b818") xpos 6 ypos 6 xsize 848 ysize 156
                                                                    add Solid("#ffb347") xpos 16 ypos 0 xsize 210 ysize 2
                                                                    add Solid("#ffb347") xpos 650 ypos 166 xsize 184 ysize 2

                                                                    frame:
                                                                        background Transform("gui/button/Plain_btn.png", xsize=136, ysize=136)
                                                                        xpos 16
                                                                        ypos 16
                                                                        xsize 136
                                                                        ysize 136
                                                                        xpadding 8
                                                                        ypadding 8

                                                                        if featured_icon_path:
                                                                            add Transform(featured_icon_path, xalign=0.5, yalign=0.5, fit="contain", xsize=116, ysize=116)
                                                                        else:
                                                                            text featured_icon_fallback style "inv_title" color "#ffe39a" size 56:
                                                                                xalign 0.5
                                                                                yalign 0.5

                                                                    vbox:
                                                                        xpos 176
                                                                        ypos 22
                                                                        spacing 6
                                                                        xsize 450

                                                                        text current_collectible["title"] style "inv_title" color "#ffe39a" size 30
                                                                        text current_collectible["desc"] style "inv_body_text" color "#f2e7f4" size 17 xmaximum 430

                                                                    text current_collectible["status"] style "inv_title" color "#ffe39a" size 28:
                                                                        xpos 620
                                                                        ypos 24
                                                                        xsize 202
                                                                        text_align 1.0

                                                                    fixed:
                                                                        xpos 174
                                                                        ypos 116
                                                                        xsize 648
                                                                        ysize 18

                                                                        add Solid("#140d20d8") xpos 0 ypos 4 xsize 648 ysize 10
                                                                        add Solid("#ffffff20") xpos 1 ypos 5 xsize 646 ysize 1
                                                                        $ featured_progress_width = int((648 * current_collectible["found_count"]) / max(1, current_collectible["total_count"]))
                                                                        add Solid("#ffc64d") xpos 0 ypos 4 xsize featured_progress_width ysize 10
                                                                        add Solid("#fff4c850") xpos 0 ypos 5 xsize max(0, featured_progress_width - 12) ysize 2

                                                        fixed:
                                                            xpos 184
                                                            ypos 242
                                                            xsize 800
                                                            ysize 270

                                                            grid 5 3:
                                                                xpos 0
                                                                ypos 0
                                                                xspacing 10
                                                                yspacing 12

                                                                for preview_item in selected_collectible_previews[:15]:
                                                                    if preview_item and renpy.loadable(preview_item.get("thumbnail", "")):
                                                                        button:
                                                                            style "inv_card_button"
                                                                            action Show("extra_gallery_lightbox", image_path=preview_item.get("full", preview_item.get("thumbnail")), image_list=[preview_item.get("full", preview_item.get("thumbnail"))], image_index=0)
                                                                            xsize 152
                                                                            ysize 82

                                                                            add Transform(preview_item.get("thumbnail", ""), xalign=0.5, yalign=0.5, fit="cover", xsize=152, ysize=82)
                                                                    else:
                                                                        fixed:
                                                                            xsize 152
                                                                            ysize 82
                                                                            clipping True

                                                                            add Transform("gui/inventory_system/gui/collectible_preview_box.png", xsize=152, ysize=82)

                                                        if renpy.loadable(current_collectible["display_image"]):
                                                            add Transform(
                                                                current_collectible["display_image"],
                                                                xanchor=1.0,
                                                                yanchor=1.0,
                                                                xpos=(selected_collectible_art_xpos - 24),
                                                                ypos=(selected_collectible_art_ypos - 86),
                                                                xsize=selected_collectible_art_xsize,
                                                                ysize=selected_collectible_art_ysize
                                                            )

                                                        vbox:
                                                            xalign 0.5
                                                            ypos 574
                                                            spacing 14
                                                            xsize 640

                                                            text "Overall Completion: {}/{}".format(overall_found, overall_total) style "inv_section_title" color "#f0e8ff" size 28 xalign 0.5

                                                            fixed:
                                                                xsize 640
                                                                ysize 28

                                                                $ overall_progress_width = int((640 * overall_found) / max(1, overall_total))
                                                                add Solid("#160f22de") xpos 0 ypos 7 xsize 640 ysize 14
                                                                add Solid("#ffffff18") xpos 1 ypos 8 xsize 638 ysize 1
                                                                add Solid("#e59cff") xpos 0 ypos 7 xsize overall_progress_width ysize 14
                                                                add Solid("#ffffff32") xpos 0 ypos 8 xsize max(0, overall_progress_width - 12) ysize 3

                                        elif inv_tab == "characters":
                                            fixed:
                                                xfill True
                                                ysize 740

                                                vbox:
                                                    xpos 0
                                                    ypos 0
                                                    spacing 12
                                                    xsize 1060

                                                    for ch in tab_items:
                                                        button:
                                                            style "inv_card_button"
                                                            xsize 1060
                                                            ysize 150
                                                            action Show("inventory_character_detail", character=ch)

                                                            fixed:
                                                                xsize 1060
                                                                ysize 150

                                                                add Solid(ch.get("card_bg", "#23173dca"))
                                                                add Solid(ch.get("card_bg_2", "#17132bd8")) xpos 3 ypos 3 xsize 1054 ysize 144
                                                                add Solid(ch.get("frame_glow", "#f2a4ff")) xpos 0 ypos 0 xsize 1060 ysize 2
                                                                add Solid(ch.get("frame_glow", "#f2a4ff")) xpos 0 ypos 148 xsize 1060 ysize 2
                                                                add Solid(ch.get("frame_glow", "#f2a4ff")) xpos 0 ypos 0 xsize 2 ysize 150
                                                                add Solid(ch.get("frame_glow", "#f2a4ff")) xpos 1058 ypos 0 xsize 2 ysize 150
                                                                add Solid(ch.get("accent_soft", "#ffffff10")) xpos 16 ypos 16 xsize 1028 ysize 118
                                                                add Solid(ch.get("frame_glow", "#f2a4ff") + "22") xpos 14 ypos 14 xsize 1032 ysize 122

                                                                fixed:
                                                                    xpos 18
                                                                    ypos 15
                                                                    xsize 148
                                                                    ysize 120

                                                                    add Transform("gui/inventory_system/gui/slot_bg.png", xsize=148, ysize=120)

                                                                vbox:
                                                                    xpos 172
                                                                    ypos 14
                                                                    spacing 4
                                                                    xsize 392

                                                                    text ch["name"] style "inv_title" color ch.get("frame_glow", "#f2a4ff") size 30
                                                                    text ch["desc"] style "inv_body_text" color "#fff6f9" size 16
                                                                    text ch.get("description_long", "") style "inv_muted_text" color "#f1e8ff" size 15 xmaximum 372

                                                                hbox:
                                                                    xpos 640
                                                                    ypos 24
                                                                    spacing 14

                                                                    frame:
                                                                        background "#ffffff08"
                                                                        xpadding 18
                                                                        ypadding 8

                                                                        hbox:
                                                                            spacing 8
                                                                            text ch.get("role_icon", "•") style "inv_body_text" color ch.get("frame_glow", "#f2a4ff") size 18
                                                                            text ch["role"] style "inv_body_text" color "#ffe7fb" size 15

                                                                    frame:
                                                                        background "#ffffff08"
                                                                        xpadding 18
                                                                        ypadding 8

                                                                        hbox:
                                                                            spacing 8
                                                                            text ch.get("affinity_icon", "•") style "inv_body_text" color ch.get("frame_glow", "#f2a4ff") size 18
                                                                            text ch["affinity"] style "inv_body_text" color "#ffe7fb" size 15

                                                                hbox:
                                                                    xpos 640
                                                                    ypos 84
                                                                    spacing 10

                                                                    text ch.get("meta_icon", "•") style "inv_label_text" color ch.get("frame_glow", "#f2a4ff") size 18
                                                                    text ch.get("meta_left", "") style "inv_body_text" color "#efe4ff" size 16
                                                                    text "•" style "inv_body_text" color ch.get("frame_glow", "#f2a4ff") size 16
                                                                    text ch.get("meta_right", "") style "inv_body_text" color "#efe4ff" size 16

                                        else:
                                            for item in tab_items:
                                                frame:
                                                    style "inv_card_frame"
                                                    xfill True
                                                    background tab_colors["accent_soft"][:-2] + "18"

                                                    vbox:
                                                        spacing 8
                                                        text item.get("name", _("Unknown Item")) style "inv_section_title"
                                                        text item.get("description", _("No description yet.")) style "inv_muted_text"

    hbox:
        xalign 0.5
        yalign 0.975
        spacing 20

        if main_menu:
            use ui_png_button(_("Back"), ShowMenu("main_menu"), xsize=220, ysize=56, text_style="ui_btn_text_small")
        else:
            use ui_png_button(_("Back"), Return(), xsize=220, ysize=56, text_style="ui_btn_text_small")
