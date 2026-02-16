# custom_extra_menu.rpy
# Extra menu hub + destination pages.

init -2 python:
    import os
    LOCKED_GALLERY_TILE = "gui/gallery/locked_tile.png"
    LOCKED_GALLERY_TILE_FALLBACK = "gui/window_icon.png"
    CHARACTER_GALLERY_DEV_UNLOCK_ALL = False

    def _extra_panel(title, subtitle=""):
        return {"title": title, "subtitle": subtitle}

    def _gallery_items(folder_prefix):
        exts = (".png", ".jpg", ".jpeg", ".webp")
        items = []
        for f in renpy.list_files():
            if not f.startswith(folder_prefix + "/"):
                continue
            if os.path.splitext(f)[1].lower() not in exts:
                continue
            name = os.path.splitext(os.path.basename(f))[0].replace("_", " ")
            items.append({"name": name, "path": f})
        items.sort(key=lambda i: i["name"].lower())
        return items

    def _gallery_with_placeholders(folder_prefix, label_prefix, count=12):
        items = _gallery_items(folder_prefix)
        if items:
            return items
        ph = "gui/mainmenu_bg.png"
        if not renpy.loadable(ph):
            ph = "gui/mainmenu_bg2.png" if renpy.loadable("gui/mainmenu_bg2.png") else "gui/window_icon.png"
        return [{"name": "{} {}".format(label_prefix, i + 1), "path": ph} for i in range(count)]

    def _gallery_items_from_list(paths):
        items = []
        for p in paths:
            if renpy.loadable(p):
                name = os.path.splitext(os.path.basename(p))[0].replace("_", " ")
                items.append({"name": name, "path": p})
        return items

    def _gallery_unlock_key(path):
        return path.lower()

    def _gallery_unlock_set():
        raw = getattr(persistent, "gallery_unlocked_images", None)
        if raw is None:
            s = set()
        else:
            try:
                s = set(raw)
            except Exception:
                s = set()
        persistent.gallery_unlocked_images = s
        return s

    def gallery_image_unlocked(path):
        if CHARACTER_GALLERY_DEV_UNLOCK_ALL:
            return True
        return _gallery_unlock_key(path) in _gallery_unlock_set()

    def unlock_gallery_image(path):
        s = _gallery_unlock_set()
        k = _gallery_unlock_key(path)
        if k not in s:
            s.add(k)
            persistent.gallery_unlocked_images = s
            renpy.save_persistent()

    def reset_gallery_unlocks():
        persistent.gallery_unlocked_images = set()
        renpy.save_persistent()

    def _character_name_for_path(path):
        # Preferred: folder-per-character, e.g. gui/gallery/characters/Aurora/img01.png
        parent = os.path.basename(os.path.dirname(path))
        if parent and parent.lower() not in ("characters", "gallery", "gui"):
            return parent.replace("_", " ")

        # Fallback: prefix before first "_" in filename.
        base = os.path.splitext(os.path.basename(path))[0]
        if "_" in base:
            return base.split("_", 1)[0].replace("-", " ")
        if "-" in base:
            return base.split("-", 1)[0].replace("_", " ")
        return base.replace("_", " ")

    def _character_gallery_map(paths):
        out = {}
        for p in paths:
            if not renpy.loadable(p):
                continue
            cname = _character_name_for_path(p).strip()
            if cname not in out:
                out[cname] = []
            out[cname].append({
                "name": os.path.splitext(os.path.basename(p))[0].replace("_", " "),
                "path": p,
                "unlocked": gallery_image_unlocked(p),
            })

        for cname in out.keys():
            out[cname].sort(key=lambda x: x["name"].lower())
        return dict(sorted(out.items(), key=lambda kv: kv[0].lower()))

    def _character_thumb_for_name(cname, items):
        thumb_map = globals().get("gallery_character_thumbs", {}) or {}
        mapped = thumb_map.get(cname)
        if mapped and renpy.loadable(mapped):
            return mapped

        # Prefer any unlocked image as a thumbnail, otherwise fallback to first.
        for it in items:
            if it.get("unlocked") and renpy.loadable(it.get("path", "")):
                return it["path"]
        if items:
            return items[0].get("path")
        return None


style extra_title is text:
    font "fonts/trotes/Trotes.ttf"
    size 72
    color "#ffffff"
    outlines [(4, "#6b3aa8", 0, 0)]

style extra_subtitle is text:
    font "fonts/trotes/Trotes.ttf"
    size 30
    color "#efe5ff"
    outlines [(3, "#5a3192", 0, 0)]

style extra_card_title is text:
    font "fonts/trotes/Trotes.ttf"
    size 38
    color "#ffffff"
    outlines [(3, "#5a3192", 0, 0)]

style extra_body is text:
    font "fonts/trotes/Trotes.ttf"
    size 28
    color "#f3ecff"
    outlines [(2, "#47286f", 0, 0)]

style extra_tab_button is button:
    background Solid("#2b2140ee")
    hover_background Solid("#6b3aa8ee")
    selected_background Solid("#8f50d6ff")
    xpadding 26
    ypadding 10

style extra_tab_button_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 34
    color "#f3ecff"
    outlines [(2, "#47286f", 0, 0)]

style extra_gallery_card is button:
    background Solid("#2a2140ee")
    hover_background Solid("#3a2e57ee")
    xsize 510
    ysize 280
    xpadding 10
    ypadding 10

style extra_gallery_name is text:
    font "fonts/trotes/Trotes.ttf"
    size 26
    color "#f3ecff"
    outlines [(2, "#47286f", 0, 0)]

style extra_page_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 28
    color "#efe5ff"
    outlines [(2, "#47286f", 0, 0)]

style extra_gallery_thumb is fixed:
    xsize 360
    ysize 215

style extra_gallery_hub_card is button:
    background None
    hover_background None
    xsize 420
    ysize 710
    xpadding 0
    ypadding 0

style extra_gallery_hub_title is text:
    font "fonts/trotes/Trotes.ttf"
    size 32
    color "#2c2c32"
    outlines []

style char_gallery_title is text:
    font "fonts/trotes/Trotes.ttf"
    size 42
    color "#d6ebff"
    outlines [(2, "#1a3159", 0, 0)]

style char_gallery_name is text:
    font "fonts/trotes/Trotes.ttf"
    size 26
    color "#eaf3ff"
    outlines [(2, "#27406d", 0, 0)]

style char_gallery_btn is button:
    background Solid("#1e2e50cc")
    hover_background Solid("#2d4777dd")
    selected_background Solid("#3b619eea")
    xpadding 12
    ypadding 8

style char_gallery_btn_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 24
    color "#e9f0ff"
    outlines [(1, "#162845", 0, 0)]

style char_gallery_card is button:
    background Solid("#233559cc")
    hover_background Solid("#2f4a7bdd")
    xsize 410
    ysize 330
    xpadding 10
    ypadding 10

style char_gallery_list_card is button:
    background Solid("#1a2b4acc")
    hover_background Solid("#27406ddd")
    selected_background Solid("#3d66a8f0")
    xsize 106
    ysize 132
    xpadding 4
    ypadding 4

style char_gallery_list_name is text:
    font "fonts/trotes/Trotes.ttf"
    size 20
    color "#e9f0ff"
    outlines [(1, "#162845", 0, 0)]

style char_gallery_hover_name is text:
    font "fonts/trotes/Trotes.ttf"
    size 36
    color "#e9f5ff"
    outlines [(2, "#142745", 0, 0)]

style extra_hub_chip_card is button:
    background None
    hover_background None
    xsize 300
    ysize 470
    xpadding 0
    ypadding 0

style extra_hub_chip_card_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 30
    color "#ffffff"
    outlines [(3, "#5a3192", 0, 0)]


screen extra_menu():
    tag menu
    $ char_cfg_items = _gallery_items_from_list(gallery_character_images)
    $ gameplay_cfg_items = _gallery_items_from_list(gallery_gameplay_images)
    $ secret_cfg_items = _gallery_items_from_list(gallery_secret_images)
    $ extra_cfg_items = _gallery_items_from_list(gallery_extra_images)
    $ char_preview = (char_cfg_items[0]["path"] if char_cfg_items else _gallery_with_placeholders("gui/gallery/characters", "Character", 1)[0]["path"])
    $ gameplay_preview = (gameplay_cfg_items[0]["path"] if gameplay_cfg_items else _gallery_with_placeholders("gui/gallery/gameplay", "Gameplay", 1)[0]["path"])
    $ secret_preview = (secret_cfg_items[0]["path"] if secret_cfg_items else _gallery_with_placeholders("gui/gallery/secret", "Secret", 1)[0]["path"])
    $ extra_preview = (extra_cfg_items[0]["path"] if extra_cfg_items else _gallery_with_placeholders("gui/gallery/extra", "Extra", 1)[0]["path"])
    $ music_preview = "gui/music_room/cover_art.webp" if renpy.loadable("gui/music_room/cover_art.webp") else gameplay_preview

    add Solid("#d7e6f2")

    # Simple geometric background accents.
    add Transform(Solid("#b8d1e655"), rotate=22, xpos=-140, ypos=130, xsize=980, ysize=5)
    add Transform(Solid("#b8d1e655"), rotate=-16, xpos=500, ypos=32, xsize=1260, ysize=5)
    add Transform(Solid("#b8d1e655"), rotate=13, xpos=980, ypos=420, xsize=880, ysize=5)
    add Transform(Solid("#b8d1e655"), rotate=-28, xpos=120, ypos=780, xsize=760, ysize=5)

    fixed:
        xalign 0.5
        yalign 0.40
        xsize 1880
        ysize 760

        hbox:
            xalign 0.5
            yalign 0.5
            spacing 48

            button:
                action ShowMenu("extra_image_gallery")
                background None
                hover_background None
                xsize 330
                ysize 700
                fixed:
                    xysize (330, 700)
                    add Solid("#6d58e5") xpos 37 ypos 120 xsize 256 ysize 432
                    add Transform(Solid("#6d58e5"), rotate=45, xsize=170, ysize=170, xalign=0.5, ypos=43)
                    add Transform(Solid("#6d58e5"), rotate=45, xsize=170, ysize=170, xalign=0.5, ypos=458)
                    add Solid("#f7f8ff") xpos 45 ypos 128 xsize 240 ysize 416
                    add Transform(Solid("#f7f8ff"), rotate=45, xsize=154, ysize=154, xalign=0.5, ypos=51)
                    add Transform(Solid("#f7f8ff"), rotate=45, xsize=154, ysize=154, xalign=0.5, ypos=466)
                    fixed:
                        xpos 53
                        ypos 136
                        xysize (224, 400)
                        clipping True
                        add Transform(char_preview, fit="cover", xysize=(224, 400), xalign=0.5, yalign=0.5)

            button:
                action ShowMenu("music_room", mr=music_room)
                background None
                hover_background None
                xsize 330
                ysize 700
                fixed:
                    xysize (330, 700)
                    add Solid("#6d58e5") xpos 37 ypos 120 xsize 256 ysize 432
                    add Transform(Solid("#6d58e5"), rotate=45, xsize=170, ysize=170, xalign=0.5, ypos=43)
                    add Transform(Solid("#6d58e5"), rotate=45, xsize=170, ysize=170, xalign=0.5, ypos=458)
                    add Solid("#f7f8ff") xpos 45 ypos 128 xsize 240 ysize 416
                    add Transform(Solid("#f7f8ff"), rotate=45, xsize=154, ysize=154, xalign=0.5, ypos=51)
                    add Transform(Solid("#f7f8ff"), rotate=45, xsize=154, ysize=154, xalign=0.5, ypos=466)
                    fixed:
                        xpos 53
                        ypos 136
                        xysize (224, 400)
                        clipping True
                        add Transform(music_preview, fit="cover", xysize=(224, 400), xalign=0.5, yalign=0.5)

            button:
                action ShowMenu("achievement_gallery")
                background None
                hover_background None
                xsize 330
                ysize 700
                fixed:
                    xysize (330, 700)
                    add Solid("#6d58e5") xpos 37 ypos 120 xsize 256 ysize 432
                    add Transform(Solid("#6d58e5"), rotate=45, xsize=170, ysize=170, xalign=0.5, ypos=43)
                    add Transform(Solid("#6d58e5"), rotate=45, xsize=170, ysize=170, xalign=0.5, ypos=458)
                    add Solid("#f7f8ff") xpos 45 ypos 128 xsize 240 ysize 416
                    add Transform(Solid("#f7f8ff"), rotate=45, xsize=154, ysize=154, xalign=0.5, ypos=51)
                    add Transform(Solid("#f7f8ff"), rotate=45, xsize=154, ysize=154, xalign=0.5, ypos=466)
                    fixed:
                        xpos 53
                        ypos 136
                        xysize (224, 400)
                        clipping True
                        add Transform(gameplay_preview, fit="cover", xysize=(224, 400), xalign=0.5, yalign=0.5)

            button:
                action ShowMenu("extra_credits")
                background None
                hover_background None
                xsize 330
                ysize 700
                fixed:
                    xysize (330, 700)
                    add Solid("#6d58e5") xpos 37 ypos 120 xsize 256 ysize 432
                    add Transform(Solid("#6d58e5"), rotate=45, xsize=170, ysize=170, xalign=0.5, ypos=43)
                    add Transform(Solid("#6d58e5"), rotate=45, xsize=170, ysize=170, xalign=0.5, ypos=458)
                    add Solid("#f7f8ff") xpos 45 ypos 128 xsize 240 ysize 416
                    add Transform(Solid("#f7f8ff"), rotate=45, xsize=154, ysize=154, xalign=0.5, ypos=51)
                    add Transform(Solid("#f7f8ff"), rotate=45, xsize=154, ysize=154, xalign=0.5, ypos=466)
                    fixed:
                        xpos 53
                        ypos 136
                        xysize (224, 400)
                        clipping True
                        add Transform(extra_preview, fit="cover", xysize=(224, 400), xalign=0.5, yalign=0.5)

    # 5th card underneath, horizontal, for Secrets.
    button:
        action ShowMenu("extra_image_gallery_grid", initial_tab="secret")
        xalign 0.5
        ypos 760
        xsize 640
        ysize 210
        background None
        hover_background None
        fixed:
            xysize (640, 210)
            add Solid("#6d58e5") xysize (640, 210)
            add Solid("#f7f8ff") xpos 8 ypos 8 xysize (624, 194)
            fixed:
                xpos 14
                ypos 14
                xysize (612, 182)
                clipping True
                add Transform(secret_preview, fit="cover", xysize=(612, 182), xalign=0.5, yalign=0.5)
            add Solid("#291f53aa") xpos 14 ypos 141 xsize 612 ysize 55
            text "Secrets" style "extra_hub_chip_card_text" xalign 0.5 yalign 0.92

    textbutton "<-":
        action ShowMenu("main_menu")
        xpos 1820
        ypos 38
        xsize 90
        ysize 90
        background Frame(Solid("#000000"), 45, 45)
        text_size 42
        text_color "#ffffff"
        text_xalign 0.5
        text_yalign 0.5


screen extra_image_gallery():
    tag menu
    $ char_cfg_items = _gallery_items_from_list(gallery_character_images)
    $ gameplay_cfg_items = _gallery_items_from_list(gallery_gameplay_images)
    $ secret_cfg_items = _gallery_items_from_list(gallery_secret_images)
    $ extra_cfg_items = _gallery_items_from_list(gallery_extra_images)
    $ chars_preview = (char_cfg_items[0]["path"] if char_cfg_items else _gallery_with_placeholders("gui/gallery/characters", "Character", 1)[0]["path"])
    $ gameplay_preview = (gameplay_cfg_items[0]["path"] if gameplay_cfg_items else _gallery_with_placeholders("gui/gallery/gameplay", "Gameplay", 1)[0]["path"])
    $ secret_preview = (secret_cfg_items[0]["path"] if secret_cfg_items else _gallery_with_placeholders("gui/gallery/secret", "Secret", 1)[0]["path"])
    $ extra_preview = (extra_cfg_items[0]["path"] if extra_cfg_items else _gallery_with_placeholders("gui/gallery/extra", "Extra", 1)[0]["path"])

    add Solid("#e8d4dd")

    textbutton "GALLERY  >":
        action NullAction()
        xpos 48
        ypos 40
        background Frame(Solid("#ead8df"), 8, 8)
        xminimum 320
        yminimum 76
        text_size 48
        text_color "#2b2b31"
        text_xalign 0.5
        text_yalign 0.5

    textbutton "<-":
        action ShowMenu("extra_menu")
        xpos 1820
        ypos 40
        xsize 90
        ysize 90
        background Frame(Solid("#000000"), 45, 45)
        text_size 42
        text_color "#ffffff"
        text_xalign 0.5
        text_yalign 0.5

    hbox:
        xalign 0.5
        ypos 220
        spacing 60

        button style "extra_gallery_hub_card" action ShowMenu("extra_character_gallery"):
            fixed:
                xysize (420, 710)
                add Solid("#111111") xysize (420, 710)
                add Solid("#ead8df") xpos 3 ypos 3 xysize (414, 704)
                add chars_preview fit "contain" xpos 6 ypos 6 xysize (408, 698)

        button style "extra_gallery_hub_card" action ShowMenu("extra_image_gallery_grid", initial_tab="gameplay"):
            fixed:
                xysize (420, 710)
                add Solid("#111111") xysize (420, 710)
                add Solid("#ead8df") xpos 3 ypos 3 xysize (414, 704)
                if gameplay_cfg_items:
                    add gameplay_preview fit "contain" xpos 6 ypos 6 xysize (408, 698)
                else:
                    add (LOCKED_GALLERY_TILE if renpy.loadable(LOCKED_GALLERY_TILE) else LOCKED_GALLERY_TILE_FALLBACK) fit "contain" xpos 6 ypos 6 xysize (408, 698)

        button style "extra_gallery_hub_card" action ShowMenu("extra_image_gallery_grid", initial_tab="secret"):
            fixed:
                xysize (420, 710)
                add Solid("#111111") xysize (420, 710)
                add Solid("#ead8df") xpos 3 ypos 3 xysize (414, 704)
                if secret_cfg_items:
                    add secret_preview fit "contain" xpos 6 ypos 6 xysize (408, 698)
                else:
                    add (LOCKED_GALLERY_TILE if renpy.loadable(LOCKED_GALLERY_TILE) else LOCKED_GALLERY_TILE_FALLBACK) fit "contain" xpos 6 ypos 6 xysize (408, 698)

        button style "extra_gallery_hub_card" action ShowMenu("extra_image_gallery_grid", initial_tab="extra"):
            fixed:
                xysize (420, 710)
                add Solid("#111111") xysize (420, 710)
                add Solid("#ead8df") xpos 3 ypos 3 xysize (414, 704)
                if extra_cfg_items:
                    add extra_preview fit "contain" xpos 6 ypos 6 xysize (408, 698)
                else:
                    add (LOCKED_GALLERY_TILE if renpy.loadable(LOCKED_GALLERY_TILE) else LOCKED_GALLERY_TILE_FALLBACK) fit "contain" xpos 6 ypos 6 xysize (408, 698)


screen extra_character_gallery():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))
    $ raw_items = _gallery_items_from_list(gallery_character_images)
    $ char_map = _character_gallery_map([x["path"] for x in raw_items])
    $ char_names = list(char_map.keys())
    default cg_selected = (char_names[0] if char_names else "Character")
    default cg_page = 0
    default cg_hover_name = ""

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    add Solid("#0f1830d6")

    if cg_selected not in char_names:
        $ cg_selected = (char_names[0] if char_names else "Character")
        $ cg_page = 0

    $ selected_items = char_map.get(cg_selected, [])
    $ items_per_page = 6
    $ total_pages = max(1, (len(selected_items) + items_per_page - 1) // items_per_page)
    $ cg_page = min(cg_page, total_pages - 1)
    $ page_start = cg_page * items_per_page
    $ page_items = selected_items[page_start:page_start + items_per_page]
    $ selected_open_paths = [x["path"] for x in selected_items if x.get("unlocked")]
    $ locked_tile = (LOCKED_GALLERY_TILE if renpy.loadable(LOCKED_GALLERY_TILE) else LOCKED_GALLERY_TILE_FALLBACK)
    $ char_slots = 12
    $ left_cards = list(char_names[:char_slots])
    $ left_cards.extend([None] * max(0, char_slots - len(left_cards)))

    # Left character list panel (click a character card).
    frame:
        background Solid("#101b33ee")
        xpos 45
        ypos 120
        xsize 490
        ysize 860
        padding (16, 14)

        vbox:
            spacing 8
            text "Character List" style "char_gallery_title" xalign 0.5
            viewport:
                mousewheel True
                draggable True
                scrollbars None
                xsize 452
                ysize 640
                has vpgrid
                cols 4
                rows 3
                xspacing 6
                yspacing 6
                for slot_i, cname in enumerate(left_cards):
                    if cname:
                        $ citems = char_map.get(cname, [])
                        $ thumb = _character_thumb_for_name(cname, citems)
                        $ any_unlocked = any([ci.get("unlocked", False) for ci in citems])
                        button style "char_gallery_list_card":
                            selected (cname == cg_selected)
                            action [SetScreenVariable("cg_selected", cname), SetScreenVariable("cg_page", 0)]
                            hovered SetScreenVariable("cg_hover_name", cname)
                            unhovered SetScreenVariable("cg_hover_name", "")
                            fixed:
                                xysize (98, 124)
                                add Solid("#8cb5ff") xysize (98, 124)
                                add Solid("#162544") xpos 2 ypos 2 xysize (94, 120)
                                if any_unlocked and thumb:
                                    add thumb fit "cover" xpos 4 ypos 4 xysize (90, 116)
                                else:
                                    if thumb:
                                        add thumb fit "cover" xpos 4 ypos 4 xysize (90, 116)
                                    else:
                                        add Solid("#0d162b") xpos 4 ypos 4 xysize (90, 116)
                                    add Solid("#0d1526cc") xpos 4 ypos 4 xysize (90, 116)
                    else:
                        button style "char_gallery_list_card" action NullAction():
                            hovered SetScreenVariable("cg_hover_name", "Empty Slot")
                            unhovered SetScreenVariable("cg_hover_name", "")
                            fixed:
                                xysize (98, 124)
                                add Solid("#8cb5ff") xysize (98, 124)
                                add Solid("#162544") xpos 2 ypos 2 xysize (94, 120)
                                add Solid("#0d162b") xpos 4 ypos 4 xysize (90, 116)

            fixed:
                xfill True
                ysize 92
                add Solid("#8cb5ff66") xpos 8 ypos 8 xsize 436 ysize 2
                text (cg_hover_name if cg_hover_name else cg_selected) style "char_gallery_hover_name" xalign 0.5 ypos 24

    # Right selected character gallery.
    frame:
        background None
        xpos 565
        ypos 120
        xsize 1300
        ysize 860
        padding (22, 16)

        vbox:
            spacing 16
            text "OSHI DECK" style "char_gallery_title" xalign 0.5

            vpgrid:
                cols 3
                rows 2
                xspacing 12
                yspacing 8
                xalign 0.5
                yalign 0.5

                for item in page_items:
                    button style "char_gallery_card" action If(item["unlocked"], Show("extra_gallery_lightbox", image_path=item["path"], image_list=selected_open_paths, image_index=(selected_open_paths.index(item["path"]) if item["path"] in selected_open_paths else 0)), NullAction()):
                        vbox:
                            spacing 8
                            fixed:
                                xysize (400, 272)
                                add Solid("#8cb5ff") xysize (400, 272)
                                add Solid("#162544") xpos 2 ypos 2 xysize (396, 268)
                                if item["unlocked"]:
                                    add item["path"] fit "contain" xpos 6 ypos 6 xysize (388, 240)
                                else:
                                    add locked_tile fit "contain" xpos 6 ypos 6 xysize (388, 240)
                                    add Solid("#111826b8") xpos 6 ypos 6 xysize (388, 240)
                                    text "LOCKED" style "char_gallery_title" size 34 xalign 0.5 yalign 0.5
                            if item["unlocked"]:
                                text item["name"] style "char_gallery_name" xalign 0.5
                            else:
                                text "Locked Slot" style "char_gallery_name" xalign 0.5

                # Fill empty grid slots so layout doesn't shift on last page.
                for _i in range(items_per_page - len(page_items)):
                    fixed:
                        xysize (410, 330)
                        add Solid("#8cb5ff") xpos 5 ypos 5 xsize 400 ysize 272
                        add Solid("#162544") xpos 7 ypos 7 xsize 396 ysize 268
                        add Solid("#0d162b") xpos 11 ypos 11 xsize 388 ysize 240
                        text "EMPTY" style "char_gallery_name" xalign 0.5 ypos 292

            hbox:
                spacing 18
                xalign 0.5
                textbutton "<" style "extra_tab_button":
                    sensitive cg_page > 0
                    action SetScreenVariable("cg_page", cg_page - 1)
                text ("Page [cg_page + 1] / [total_pages]") style "extra_page_text"
                textbutton ">" style "extra_tab_button":
                    sensitive cg_page < (total_pages - 1)
                    action SetScreenVariable("cg_page", cg_page + 1)

    hbox:
        xalign 0.5
        yalign 0.95
        spacing 16
        use ui_png_button(L("pref_button_back"), ShowMenu("extra_image_gallery"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)


screen extra_image_gallery_grid(initial_tab="gameplay"):
    tag menu
    default ig_tab = initial_tab
    default ig_gameplay_page = 0
    default ig_secret_page = 0
    default ig_extra_page = 0
    default ig_hover_name = ""

    $ mm_alt = bool(getattr(persistent, "mm_alt", False))
    $ gameplay_cfg_items = _gallery_items_from_list(gallery_gameplay_images)
    $ secret_cfg_items = _gallery_items_from_list(gallery_secret_images)
    $ extra_cfg_items = _gallery_items_from_list(gallery_extra_images)
    $ gameplay_items = (gameplay_cfg_items if gameplay_cfg_items else _gallery_with_placeholders("gui/gallery/gameplay", "Gameplay"))
    $ secret_items = (secret_cfg_items if secret_cfg_items else _gallery_with_placeholders("gui/gallery/secret", "Secret"))
    $ extra_items = (extra_cfg_items if extra_cfg_items else _gallery_with_placeholders("gui/gallery/extra", "Extra"))
    $ items_per_page = 6

    if ig_tab == "gameplay":
        $ active_items = gameplay_items
        $ active_page = ig_gameplay_page
        $ list_title = "Gameplay List"
    elif ig_tab == "secret":
        $ active_items = secret_items
        $ active_page = ig_secret_page
        $ list_title = "Secret List"
    else:
        $ active_items = extra_items
        $ active_page = ig_extra_page
        $ list_title = "Extra List"

    $ total_pages = max(1, (len(active_items) + items_per_page - 1) // items_per_page)
    $ active_page = min(active_page, total_pages - 1)
    $ page_start = active_page * items_per_page
    $ page_items = active_items[page_start:page_start + items_per_page]
    $ left_slots = list(active_items)
    $ left_slots.extend([None] * max(0, 12 - len(left_slots)))

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    add Solid("#0f1830d6")

    # Left list panel (same style as character gallery).
    frame:
        background Solid("#101b33ee")
        xpos 45
        ypos 120
        xsize 490
        ysize 860
        padding (16, 14)

        vbox:
            spacing 8
            text list_title style "char_gallery_title" xalign 0.5
            viewport:
                mousewheel True
                draggable True
                scrollbars None
                xsize 452
                ysize 640
                has vpgrid
                cols 4
                rows 3
                xspacing 6
                yspacing 6
                for idx, item in enumerate(left_slots):
                    if item:
                        button style "char_gallery_list_card":
                            selected (idx // items_per_page == active_page)
                            action If(
                                ig_tab == "gameplay",
                                SetScreenVariable("ig_gameplay_page", idx // items_per_page),
                                If(
                                    ig_tab == "secret",
                                    SetScreenVariable("ig_secret_page", idx // items_per_page),
                                    SetScreenVariable("ig_extra_page", idx // items_per_page)
                                )
                            )
                            hovered SetScreenVariable("ig_hover_name", item["name"])
                            unhovered SetScreenVariable("ig_hover_name", "")
                            fixed:
                                xysize (98, 124)
                                add Solid("#8cb5ff") xysize (98, 124)
                                add Solid("#162544") xpos 2 ypos 2 xysize (94, 120)
                                add item["path"] fit "cover" xpos 4 ypos 4 xysize (90, 116)
                    else:
                        button style "char_gallery_list_card" action NullAction():
                            hovered SetScreenVariable("ig_hover_name", "Empty Slot")
                            unhovered SetScreenVariable("ig_hover_name", "")
                            fixed:
                                xysize (98, 124)
                                add Solid("#8cb5ff") xysize (98, 124)
                                add Solid("#162544") xpos 2 ypos 2 xysize (94, 120)
                                add Solid("#0d162b") xpos 4 ypos 4 xysize (90, 116)

            fixed:
                xfill True
                ysize 92
                add Solid("#8cb5ff66") xpos 8 ypos 8 xsize 436 ysize 2
                text (ig_hover_name if ig_hover_name else list_title) style "char_gallery_hover_name" xalign 0.5 ypos 24

    # Right deck panel (same geometry as character gallery).
    frame:
        background None
        xpos 565
        ypos 120
        xsize 1300
        ysize 860
        padding (22, 16)

        vbox:
            spacing 16
            text "OSHI DECK" style "char_gallery_title" xalign 0.5

            vpgrid:
                cols 3
                rows 2
                xspacing 12
                yspacing 8
                xalign 0.5
                yalign 0.5

                for item_i, item in enumerate(page_items):
                    button style "char_gallery_card" action Show("extra_gallery_lightbox", image_path=item["path"], image_list=[x["path"] for x in active_items], image_index=page_start + item_i):
                        vbox:
                            spacing 8
                            fixed:
                                xysize (400, 272)
                                add Solid("#8cb5ff") xysize (400, 272)
                                add Solid("#162544") xpos 2 ypos 2 xysize (396, 268)
                                add item["path"] fit "contain" xpos 6 ypos 6 xysize (388, 240)
                            text item["name"] style "char_gallery_name" xalign 0.5

                for _i in range(items_per_page - len(page_items)):
                    fixed:
                        xysize (410, 330)
                        add Solid("#8cb5ff") xpos 5 ypos 5 xsize 400 ysize 272
                        add Solid("#162544") xpos 7 ypos 7 xsize 396 ysize 268
                        add Solid("#0d162b") xpos 11 ypos 11 xsize 388 ysize 240
                        text "EMPTY" style "char_gallery_name" xalign 0.5 ypos 292

            hbox:
                spacing 18
                xalign 0.5
                textbutton "<" style "extra_tab_button":
                    sensitive active_page > 0
                    action If(
                        ig_tab == "gameplay",
                        SetScreenVariable("ig_gameplay_page", active_page - 1),
                        If(
                            ig_tab == "secret",
                            SetScreenVariable("ig_secret_page", active_page - 1),
                            SetScreenVariable("ig_extra_page", active_page - 1)
                        )
                    )
                text ("Page [active_page + 1] / [total_pages]") style "extra_page_text"
                textbutton ">" style "extra_tab_button":
                    sensitive active_page < (total_pages - 1)
                    action If(
                        ig_tab == "gameplay",
                        SetScreenVariable("ig_gameplay_page", active_page + 1),
                        If(
                            ig_tab == "secret",
                            SetScreenVariable("ig_secret_page", active_page + 1),
                            SetScreenVariable("ig_extra_page", active_page + 1)
                        )
                    )

    hbox:
        xalign 0.5
        yalign 0.95
        spacing 16
        use ui_png_button(L("pref_button_back"), ShowMenu("extra_image_gallery"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)


screen extra_gallery_lightbox(image_path, image_list=None, image_index=0):
    modal True
    zorder 300
    default lb_index = image_index
    default lb_path = image_path
    $ lb_count = (len(image_list) if image_list else 0)
    $ can_cycle = (lb_count > 1)

    add Solid("#000000cc")

    key "dismiss" action Hide("extra_gallery_lightbox")
    key "game_menu" action Hide("extra_gallery_lightbox")
    key "rollback" action Hide("extra_gallery_lightbox")
    key "K_LEFT" action If(can_cycle, [SetScreenVariable("lb_index", (lb_index - 1) % lb_count), SetScreenVariable("lb_path", image_list[(lb_index - 1) % lb_count])], NullAction())
    key "K_RIGHT" action If(can_cycle, [SetScreenVariable("lb_index", (lb_index + 1) % lb_count), SetScreenVariable("lb_path", image_list[(lb_index + 1) % lb_count])], NullAction())

    button:
        background None
        xfill True
        yfill True
        action Hide("extra_gallery_lightbox")

    if lb_path and renpy.loadable(lb_path):
        add lb_path:
            fit "contain"
            xalign 0.5
            yalign 0.5
            xysize (1760, 960)
    else:
        text "Image not found" style "extra_subtitle":
            xalign 0.5
            yalign 0.5

    if can_cycle:
        textbutton "<":
            xpos 42
            yalign 0.5
            xsize 72
            ysize 96
            background Solid("#1c2b48cc")
            text_size 52
            text_color "#d7e9ff"
            text_xalign 0.5
            text_yalign 0.5
            action [SetScreenVariable("lb_index", (lb_index - 1) % lb_count), SetScreenVariable("lb_path", image_list[(lb_index - 1) % lb_count])]

        textbutton ">":
            xanchor 1.0
            xpos 1878
            yalign 0.5
            xsize 72
            ysize 96
            background Solid("#1c2b48cc")
            text_size 52
            text_color "#d7e9ff"
            text_xalign 0.5
            text_yalign 0.5
            action [SetScreenVariable("lb_index", (lb_index + 1) % lb_count), SetScreenVariable("lb_path", image_list[(lb_index + 1) % lb_count])]

    textbutton "X":
        xanchor 1.0
        xpos 1890
        ypos 26
        xsize 70
        ysize 70
        background Solid("#1c2b48cc")
        text_size 36
        text_color "#ffffff"
        text_xalign 0.5
        text_yalign 0.5
        action Hide("extra_gallery_lightbox")


screen extra_music_gallery():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    add Solid("#120d20bb")

    text L("extra_music_gallery") style "extra_title":
        xalign 0.5
        ypos 70

    frame:
        background Solid("#2b2140dd")
        xalign 0.5
        yalign 0.52
        xsize 1300
        ysize 560
        padding (40, 30)

        vbox:
            spacing 18
            text L("extra_music_gallery_subtitle") style "extra_subtitle"
            text L("extra_music_gallery_body") style "extra_body"

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22
        use ui_png_button(L("pref_button_back"), ShowMenu("extra_menu"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)


screen extra_achievements():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    add Solid("#120d20bb")

    text L("extra_achievements") style "extra_title":
        xalign 0.5
        ypos 70

    frame:
        background Solid("#2b2140dd")
        xalign 0.5
        yalign 0.52
        xsize 1300
        ysize 560
        padding (40, 30)

        vbox:
            spacing 18
            text L("extra_achievements_subtitle") style "extra_subtitle"
            text L("extra_achievements_body") style "extra_body"

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22
        use ui_png_button(L("pref_button_back"), ShowMenu("extra_menu"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)


screen extra_credits():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))

    if mm_alt and renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    else:
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    add Solid("#120d20bb")

    text L("extra_credits") style "extra_title":
        xalign 0.5
        ypos 70

    frame:
        background Solid("#2b2140dd")
        xalign 0.5
        yalign 0.52
        xsize 1300
        ysize 560
        padding (40, 30)

        vbox:
            spacing 18
            text L("extra_credits_subtitle") style "extra_subtitle"
            text L("extra_credits_body") style "extra_body"

    hbox:
        xalign 0.5
        yalign 0.93
        spacing 22
        use ui_png_button(L("pref_button_back"), ShowMenu("extra_menu"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)
