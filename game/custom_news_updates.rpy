# custom_news_updates.rpy
# News / Updates screen and main-menu cloud button.
# Uses existing GUI assets to avoid missing-file errors.

init -2 python:
    NEWS_PANEL_W = 1600
    NEWS_PANEL_H = 720
    NEWS_TILE_W = 300
    NEWS_TILE_H = 180
    NEWS_HERO_W = 520
    NEWS_HERO_H = 260

    NEWS_CLOUD_ZOOM = 0.22

    NEWS_ITEMS = [
        {
            "id": "main_story",
            "title": "Main Story",
            "body": "Main Story updates and release notes go here.\nAdd more detail for this entry.",
        },
        {
            "id": "side_story",
            "title": "Side Story",
            "body": "Side Story announcements and patch notes go here.\nAdd more detail for this entry.",
        },
        {
            "id": "bug_fixes",
            "title": "Bug Fixes",
            "body": "Bug fixes and stability improvements go here.\nAdd more detail for this entry.",
        },
        {
            "id": "future_characters",
            "title": "Future Characters",
            "body": "Future Characters news and release notes go here.\nAdd more detail for this entry.",
        },
    ]

    def _news_item(news_id):
        for item in NEWS_ITEMS:
            if item["id"] == news_id:
                return item
        return NEWS_ITEMS[0]


style news_title is text:
    font "fonts/trotes/Trotes.ttf"
    size 34
    color "#f7e9ff"
    outlines [(3, "#6b3aa8", 0, 0)]

style news_body is text:
    font "fonts/trotes/Trotes.ttf"
    size 22
    color "#e8d9ff"
    outlines [(2, "#3a274f", 0, 0)]
    line_spacing 4

style news_tile_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 22
    color "#ffffff"
    outlines [(3, "#6b3aa8", 0, 0)]
    xalign 0.5
    yalign 0.85

style news_cloud_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 18
    color "#ffffff"
    outlines [(2, "#6b3aa8", 0, 0)]
    xalign 0.5
    yalign 0.5


screen news_menu_button(bg_action=None, bg_label="BG", bg_use_alt=False):
    # Small cloud icon on main menu to open News/Updates.
    zorder 20

    fixed:
        xalign 0.06
        yalign 0.95
        xsize 240
        ysize 80

        hbox:
            spacing 8
            use ui_png_button("NEWS", ShowMenu("news_updates"), zoom=0.35, text_style="ui_btn_text_small")
            if bg_action is not None:
                use ui_png_button(bg_label, bg_action, zoom=0.35, text_style="ui_btn_text_small", use_alt=bg_use_alt)


screen news_updates():
    tag menu

    add "gui/news_background.png"

    # Main panel
    fixed:
        xalign 0.5
        yalign 0.52
        xsize NEWS_PANEL_W
        ysize NEWS_PANEL_H

        add Solid("#6b3aa8") xsize NEWS_PANEL_W ysize NEWS_PANEL_H
        add Solid("#2b2440cc") xpos 6 ypos 6 xsize (NEWS_PANEL_W - 12) ysize (NEWS_PANEL_H - 12)

        # Header / body text (left)
        text "News" style "news_title":
            xpos 40
            ypos 26

        text "The Version 1.0 release is available now!\nMain Story, AU Story, and new content have been added.\nLimited-time updates will be listed here." style "news_body":
            xpos 40
            ypos 80
            xsize 900

        # Hero image (right)
        fixed:
            xpos 1020
            ypos 40
            xsize NEWS_HERO_W
            ysize NEWS_HERO_H
            add Solid("#ffffff20") xsize NEWS_HERO_W ysize NEWS_HERO_H
            text "HERO IMAGE" style "news_body":
                xalign 0.5
                yalign 0.5

        # Bottom tiles
        hbox:
            xpos 60
            ypos 420
            spacing 24

            for item in NEWS_ITEMS:
                use news_tile(item)

    # Back button
    hbox:
        xalign 0.5
        yalign 0.93
        spacing 16
        use ui_png_button("BACK", ShowMenu("main_menu"), zoom=0.55, text_style="ui_btn_text_small")


screen news_tile(item):
    button:
        xsize NEWS_TILE_W
        ysize NEWS_TILE_H
        background Solid("#3a3152")
        hover_background Solid("#4a3a6a")
        action Show("news_updates_detail", news_id=item["id"])

        add Solid("#ffffff18") xsize (NEWS_TILE_W - 40) ysize (NEWS_TILE_H - 60) xalign 0.5 yalign 0.35
        text item["title"] style "news_tile_text"


screen news_updates_detail(news_id):
    modal True
    zorder 200
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
            text item["title"] style "news_title"
            text item["body"] style "news_body"

            null height 10

            hbox:
                xalign 1.0
                use ui_png_button("CLOSE", Hide("news_updates_detail"), zoom=0.55, text_style="ui_btn_text_small")
