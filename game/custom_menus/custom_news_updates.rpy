# custom_news_updates.rpy
# News / Updates screen.
# Uses existing GUI assets to avoid missing-file errors.

init -2 python:
    NEWS_PANEL_W = 1600
    NEWS_PANEL_H = 720
    NEWS_TILE_W = 275
    NEWS_TILE_H = 275
    NEWS_HERO_W = 520
    NEWS_HERO_H = 260

    NEWS_CLOUD_ZOOM = 0.22

    # News tile image tuning (global defaults; can be overridden per item).
    NEWS_TILE_IMAGE_XPAD = 4
    NEWS_TILE_IMAGE_YPAD = 4
    NEWS_TILE_IMAGE_MODE = "fit"  # "manual" or "fit"
    NEWS_TILE_IMAGE_X = 0
    NEWS_TILE_IMAGE_Y = 0
    NEWS_TILE_IMAGE_ZOOM = 1.0
    NEWS_TILE_IMAGE_W = NEWS_TILE_W - 8  # used only when mode is "fit"
    NEWS_TILE_IMAGE_H = NEWS_TILE_H - 8  # used only when mode is "fit"
    NEWS_TILE_IMAGE_FIT = "contain"  # used only when mode is "fit"
    NEWS_TILE_IMAGE_XALIGN = 0.5
    NEWS_TILE_IMAGE_YALIGN = 0.52
    NEWS_TILE_LABEL_BAND_H = 42
    NEWS_TILE_LABEL_BAND_BG = "#00000000"

    # Top-right hero image tuning (global defaults; can be overridden per item).
    NEWS_HERO_IMAGE_X = 0
    NEWS_HERO_IMAGE_Y = 30
    NEWS_HERO_IMAGE_ZOOM = 1.0
    NEWS_HERO_IMAGE_XALIGN = 0.5
    NEWS_HERO_IMAGE_YALIGN = 0.5
    NEWS_HERO_RENDER_MODE = "cover"  # "full" (show all) or "cover" (crop fill)

    def _image_cover_zoom(image_path, target_w, target_h):
        """
        Returns a scale factor that fills target area without stretching.
        """
        try:
            iw, ih = renpy.image_size(image_path)
        except Exception:
            return 1.0
        if not iw or not ih:
            return 1.0
        return max(float(target_w) / float(iw), float(target_h) / float(ih))

    NEWS_ITEMS = [
        {
            "id": "main_story",
            "title": "Main Story",
            "body": "Main Story updates and release notes go here.\nAdd more detail for this entry.",
            "image": "gui/news/main_story.png",
            "update_image": "gui/news/update_image.png",
        },
        {
            "id": "side_story",
            "title": "Side Story",
            "body": "Side Story announcements and patch notes go here.\nAdd more detail for this entry.",
            "image": "gui/news/side_story.png",
            "update_image": "gui/news/side_story_update.png",
        },
        {
            "id": "bug_fixes",
            "title": "Bug Fixes",
            "body": "Bug fixes and stability improvements go here.\nAdd more detail for this entry.",
            "image": "gui/news/bug_fixes.png",
            "update_image": "gui/news/bug_fixes_update.png",
        },
        {
            "id": "future_characters",
            "title": "Future Characters",
            "body": "Future Characters news and release notes go here.\nAdd more detail for this entry.",
            "image": "gui/news/future_characters.png",
            "update_image": "gui/news/future_characters_update.png",
        },
        {
            "id": "roadmap",
            "title": "Roadmap",
            "body": "Roadmap updates and future plans go here.\nAdd more detail for this entry.",
            "image": "gui/news/roadmap.png",
            "update_image": "gui/news/roadmap.png",
        },
    ]

    def _news_item(news_id):
        for item in NEWS_ITEMS:
            if item["id"] == news_id:
                return item
        return NEWS_ITEMS[0]

    def _news_item_text(item, field):
        key = "news_{0}_{1}".format(item.get("id", ""), field)
        txt = L(key)
        return txt if txt != key else item.get(field, "")


style news_title is text:
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
    size 34
    color "#f7e9ff"
    outlines [(3, "#6b3aa8", 0, 0)]

style news_body is text:
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
    size 22
    color "#e8d9ff"
    outlines [(2, "#3a274f", 0, 0)]
    line_spacing 4

style news_tile_text is text:
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
    size 22
    color "#ffffff"
    outlines [(3, "#6b3aa8", 0, 0)]
    xalign 0.5
    yalign 0.85

style news_cloud_text is text:
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
    size 18
    color "#ffffff"
    outlines [(2, "#6b3aa8", 0, 0)]
    xalign 0.5
    yalign 0.5


screen news_updates():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))
    default news_selected = NEWS_ITEMS[0]["id"]
    $ hero_item = NEWS_ITEMS[0]
    $ update_image = hero_item.get("update_image", hero_item.get("image"))
    $ hero_image_x = hero_item.get("hero_image_x", NEWS_HERO_IMAGE_X)
    $ hero_image_y = hero_item.get("hero_image_y", NEWS_HERO_IMAGE_Y)
    $ hero_image_zoom = hero_item.get("hero_image_zoom", NEWS_HERO_IMAGE_ZOOM)
    $ hero_image_xalign = hero_item.get("hero_image_xalign", NEWS_HERO_IMAGE_XALIGN)
    $ hero_image_yalign = hero_item.get("hero_image_yalign", NEWS_HERO_IMAGE_YALIGN)
    $ hero_render_mode = hero_item.get("hero_render_mode", NEWS_HERO_RENDER_MODE)
    $ hero_base_zoom = _image_cover_zoom(update_image, NEWS_HERO_W, NEWS_HERO_H) if (update_image and renpy.loadable(update_image)) else 1.0
    $ hero_draw_zoom = hero_base_zoom * hero_image_zoom
    $ news_bg = "gui/news/new_background.png" if renpy.loadable("gui/news/new_background.png") else "gui/news/news_background.png"

    add im.Scale(news_bg, config.screen_width, config.screen_height)

    # Main panel
    fixed:
        xalign 0.5
        yalign 0.52
        xsize NEWS_PANEL_W
        ysize NEWS_PANEL_H

        add Solid("#6b3aa8") xsize NEWS_PANEL_W ysize NEWS_PANEL_H
        add Solid("#2b2440cc") xpos 6 ypos 6 xsize (NEWS_PANEL_W - 12) ysize (NEWS_PANEL_H - 12)

        # Header / body text (left)
        text L("news_title") style "news_title":
            xpos 40
            ypos 26

        text L("news_summary") style "news_body":
            xpos 40
            ypos 80
            xsize 900

        # Update image (right) - click to open full-size lightbox.
        button:
            background None
            hover_background None
            action If(
                (update_image and renpy.loadable(update_image)),
                Show("extra_gallery_lightbox", image_path=update_image, image_list=[update_image], image_index=0),
                NullAction()
            )
            xpos 1020
            ypos 40
            xsize NEWS_HERO_W
            ysize NEWS_HERO_H
            fixed:
                xsize NEWS_HERO_W
                ysize NEWS_HERO_H
                clipping True
                add Solid("#ffffff20") xsize NEWS_HERO_W ysize NEWS_HERO_H
                if update_image and renpy.loadable(update_image):
                    if hero_render_mode == "full":
                        # Background fill + foreground contain keeps all faces visible.
                        add Transform(update_image, fit="cover", xsize=NEWS_HERO_W, ysize=NEWS_HERO_H, xalign=0.5, yalign=0.5, alpha=0.30)
                        add Solid("#00000033") xsize NEWS_HERO_W ysize NEWS_HERO_H
                        add Transform(
                            update_image,
                            fit="contain",
                            xsize=NEWS_HERO_W,
                            ysize=NEWS_HERO_H,
                            xoffset=hero_image_x,
                            yoffset=hero_image_y,
                            zoom=hero_image_zoom,
                            xalign=hero_image_xalign,
                            yalign=hero_image_yalign
                        )
                    else:
                        add Transform(
                            update_image,
                            xoffset=hero_image_x,
                            yoffset=hero_image_y,
                            zoom=hero_draw_zoom,
                            xalign=hero_image_xalign,
                            yalign=hero_image_yalign
                        )
                else:
                    text L("news_hero_placeholder") style "news_body":
                        xalign 0.5
                        yalign 0.5

        # Bottom tiles
        hbox:
            xpos 60
            ypos 372
            spacing 24

            for item_i, item in enumerate(NEWS_ITEMS):
                use news_tile(item, news_selected, item_i)

    # Back button
    hbox:
        xalign 0.5
        yalign 0.93
        spacing 16
        use ui_png_button(L("pref_button_back"), ShowMenu("main_menu"), zoom=0.55, text_style="ui_btn_text_small", use_alt=mm_alt)


screen news_tile(item, news_selected, tile_index=0):
    vbox at gentle_float(tile_index * 0.12, amp=4):
        spacing 8
        use ui_news_tile_button(
            "",
            [SetScreenVariable("news_selected", item["id"]), If(item["id"] == "roadmap", Show("roadmap_updates_detail"), Show("news_updates_detail", news_id=item["id"]))],
            image=item.get("image"),
            width=NEWS_TILE_W,
            height=NEWS_TILE_H,
            selected=(news_selected == item["id"]),
            bg="#00000000",
            hover_bg="#00000000",
            text_style="news_tile_text",
            image_xpad=item.get("tile_image_xpad", NEWS_TILE_IMAGE_XPAD),
            image_ypad=item.get("tile_image_ypad", NEWS_TILE_IMAGE_YPAD),
            image_mode=item.get("tile_image_mode", NEWS_TILE_IMAGE_MODE),
            image_x=item.get("tile_image_x", NEWS_TILE_IMAGE_X),
            image_y=item.get("tile_image_y", NEWS_TILE_IMAGE_Y),
            image_zoom=item.get("tile_image_zoom", NEWS_TILE_IMAGE_ZOOM),
            image_width=item.get("tile_image_w", NEWS_TILE_IMAGE_W),
            image_height=item.get("tile_image_h", NEWS_TILE_IMAGE_H),
            image_fit=item.get("tile_image_fit", NEWS_TILE_IMAGE_FIT),
            image_xalign=item.get("tile_image_xalign", NEWS_TILE_IMAGE_XALIGN),
            image_yalign=item.get("tile_image_yalign", NEWS_TILE_IMAGE_YALIGN),
            label_band_h=0,
            label_bg="#00000000",
            use_hover_anim=True
        )

        text _news_item_text(item, "title") style "news_tile_text" xalign 0.5


screen news_updates_detail(news_id):
    modal True
    zorder 200
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))
    $ item = _news_item(news_id)

    add Solid("#0008")

    frame:
        background Solid("#2b2440")
        xalign 0.5
        yalign 0.5
        xsize 980
        ysize 560
        padding (30, 24)

        vbox:
            spacing 18
            text _news_item_text(item, "title") style "news_title"
            text _news_item_text(item, "body") style "news_body"

            null height 10

            hbox:
                xalign 1.0
                use ui_png_button(L("news_close"), Hide("news_updates_detail"), zoom=0.55, text_style="ui_btn_text_small", use_alt=mm_alt)

